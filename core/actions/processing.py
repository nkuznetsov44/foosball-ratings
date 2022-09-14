from dataclasses import replace
from collections import defaultdict
from typing import Sequence, Type

from pytz import UTC

from common.entities.competition import Competition
from common.entities.enums import RatingType
from common.entities.match import Match, MatchSet
from common.entities.ratings_state import RatingsState
from common.utils import DatetimeWithTZ
from core.actions.abstract_action import AbstractAction
from core.actions.player_state import CreatePlayerStateAction
from core.actions.ratings_state import CreateRatingsStateAction
from core.processing.strategies import (
    AbstractCalculationStrategy,
    Pre2018RatingCalculationStrategy,
    EvksOnlyRatingCalculationStrategy,
    EvksAndCumulativeRatingCalculationStrategy,
)


DATE_2018_01_01 = DatetimeWithTZ(
    year=2018, month=1, day=1, hour=0, minute=0, second=0, tzinfo=UTC
)
DATE_2022_01_01 = DatetimeWithTZ(
    year=2022, month=1, day=1, hour=0, minute=0, second=0, tzinfo=UTC
)  # TODO: уточнить, с какого момента начали считать накопительный рейтинг и поправить


_PlayerId = int
_RatingValue = int


class ProcessCompetitionAction(AbstractAction[RatingsState]):
    def __init__(self, competition: Competition) -> None:
        self.competition = competition

    async def handle(self) -> RatingsState:
        """
        Action должен не только обсчитывать рейтинг после competition,
        но и запускать пересчет всех турниров, которые ранее посчитаны,
        но исторически были после competition. Но это потом...

        Логика должна быть примерно такая:
        1. Найти состояние RatingsState, актуальное перед категорией competition.
           Это можно сделать, пройдя в цикле while по ссылкам previous_state_id,
           собирая по пути last_competition в competitions_for_processing, пока
           не дойдем до last_competition.end_date < competition.start_date.
        2. Добавить competition в конец competitions_for_processing.
        3. Подожить в intermediate_ratings_state dirty_copy найденного состояния.
        4. Вынести код текущей верссии action'a в метод _process_single_competition,
           в ней в конце запускать CreateRatingsStateAction с правильным контекстом.
        3. Запустить _process_single_competition для всех competitions_for_processing.
        """

        strategy = self._choose_calculation_strategy()
        ratings_state = await self.storage.ratings_states.get_actual()

        intermediate_ratings_state = replace(
            ratings_state,
            player_states=ratings_state.player_states.copy(),
        )

        matches = await self.storage.matches.find_by_competition(self.competition.id)

        for match in self._prepare_matches(matches):
            match_sets = await self.storage.sets.find_by_match(match.id)

            for player_id, ratings in self._calculate_ratings_after_match(
                strategy=strategy,
                ratings_state=ratings_state,
                match=match,
                match_sets=match_sets,
            ).items():
                player = intermediate_ratings_state.player_states[player_id].player
                player_state = await self.run_subaction(
                    CreatePlayerStateAction(
                        player=player,
                        last_match=match,
                        ratings=ratings,
                    )
                )
                intermediate_ratings_state.player_states.add(player_state)

        return await self.run_subaction(
            CreateRatingsStateAction(
                player_states=intermediate_ratings_state.player_states,
                last_competition=self.competition,
            )
        )

    def _choose_calculation_strategy(self) -> Type[AbstractCalculationStrategy]:
        if self.competition.end_datetime < DATE_2018_01_01:
            return Pre2018RatingCalculationStrategy
        elif self.competition.end_datetime < DATE_2022_01_01:
            return EvksOnlyRatingCalculationStrategy
        else:
            return EvksAndCumulativeRatingCalculationStrategy

    def _prepare_matches(self, matches: Sequence[Match]) -> Sequence[Match]:
        return sorted(matches, key=lambda match: match.end_datetime)

    def _calculate_ratings_after_match(
        self,
        *,
        strategy: AbstractCalculationStrategy,
        ratings_state: RatingsState,
        match: Match,
        match_sets: Sequence[MatchSet],
    ) -> dict[_PlayerId, dict[RatingType, _RatingValue]]:
        result: dict[_PlayerId, dict[RatingType, _RatingValue]] = defaultdict(dict)
        for rating_type, calculator_cls in strategy.calculators.items():
            calculator = calculator_cls(ratings_state=ratings_state)
            calc_result_by_player = calculator.calculate(
                competition=self.competition,
                match=match,
                match_sets=match_sets,
            )
            for player, rating_value in calc_result_by_player.items():
                result[player][rating_type] = rating_value
        return result

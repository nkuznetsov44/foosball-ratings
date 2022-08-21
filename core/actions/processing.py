from typing import Sequence
from collections import defaultdict
from datetime import tzinfo
from common.utils import DatetimeWithTZ
from core.actions.abstract_action import AbstractAction, ActionContext
from core.entities.competition import Competition
from core.entities.match import Match
from core.entities.player import Player
from core.entities.state import RatingsState
from common.enums import RatingType
from core.processing import strategies
from core.actions.state import CreatePlayerStateAction, CreateRatingsStateAction


BASE_TZ = tzinfo()
DATE_2018_01_01 = DatetimeWithTZ(
    year=2018, month=1, day=1, hour=0, minute=0, second=0, tzinfo=BASE_TZ
)
DATE_2022_01_01 = DatetimeWithTZ(
    year=2022, month=1, day=1, hour=0, minute=0, second=0, tzinfo=BASE_TZ
)  # TODO: уточнить, с какого момента начали считать накопительный рейтинг и поправить


class ProcessCompetitionAction(AbstractAction):
    def __init__(
        self,
        *,
        context: ActionContext,
        competition: Competition,
    ) -> None:
        super().__init__(context)
        self._competition = competition

    async def run(self) -> RatingsState:
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
        intermediate_ratings_state = self._ratings_state.dirty_copy()

        for match in self._prepare_matches():
            for player, ratings in self._calculate_ratings_after_match(
                match, strategy
            ).items():
                player_state = await CreatePlayerStateAction(
                    context=ActionContext(
                        db_engine=self._context.db_engine,
                        ratings_state=intermediate_ratings_state,
                    ),
                    player=player,
                    last_match=match,
                    ratings=ratings,
                ).run()
                intermediate_ratings_state.player_states.add(player_state)

        return await CreateRatingsStateAction(
            context=self._context,
            player_states=intermediate_ratings_state.player_states,
            last_competition=self._competition,
        ).run()

    def _choose_calculation_strategy(self):
        if self.competition.end_datetime < DATE_2018_01_01:
            return strategies.Pre2018RatingCalculationStrategy
        elif self.competition.end_datetime < DATE_2022_01_01:
            return strategies.EvksOnlyRatingCalculationStrategy
        else:
            return strategies.EvksAndCumulativeRatingCalculationStrategy

    def _prepare_matches(self) -> Sequence[Match]:
        return sorted(self.competition.matches, key=lambda match: match.end_datetime)

    def _calculate_ratings_after_match(
        self, match: Match, strategy: strategies.AbstractCalculationStrategy
    ) -> dict[Player, dict[RatingType, int]]:
        ratings_calculation_results: dict[Player, dict[RatingType, int]] = defaultdict(
            {}
        )
        for rating_type, calculator in strategy.calculators.items():
            calc_result_by_player = calculator.calculate(
                self._ratings_state, match, self._competition
            )
            for player, rating_value in calc_result_by_player.items():
                ratings_calculation_results[player][rating_type] = rating_value
        return ratings_calculation_results

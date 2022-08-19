from typing import Sequence
from collections import defaultdict
from datetime import tzinfo
from common.utils import DatetimeWithTZ
from core.actions.abstract_action import AbstractAction, ActionContext
from core.entities.competition import Competition
from core.entities.match import Match
from core.entities.player import Player
from core.entities.state import PlayerState, RatingsState
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
        Action должен не только обсчитывать этот рейтинг, но и
        запускать пересчет всех турниров, которые были после.
        """

        player_states_after_competition: set[PlayerState] = set()

        strategy = self._choose_calculation_strategy()

        for match in self._prepare_matches():
            ratings_calculation_result: dict[RatingType, dict[Player, int]] = {}
            for rating_type, calculator in strategy.calculators.items():
                ratings_calculation_result[rating_type] = calculator.calculate(
                    self._ratings_state, match, self._competition
                )
            player_states = await self._create_player_states(ratings_calculation_result)
            player_states_after_competition.update(player_states)

        # TODO: вот тут на самом деле надо еще пересчитывать турниры после competition
        return await CreateRatingsStateAction(
            context=self._context,
            player_states=player_states_after_competition,
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

    async def _create_player_states(
        self,
        ratings_calculation_result: dict[RatingType, dict[Player, int]],
        last_match: Match,
    ) -> set[PlayerState]:
        player_ratings: dict[Player, dict[RatingType, int]] = defaultdict({})
        # TODO: maybe itertools has a convinience method for this
        for rating_type, rating_result in ratings_calculation_result.items():
            for player, rating_value in rating_result.items():
                player_ratings[player][rating_type] = rating_value

        player_states: set[PlayerState] = set()
        for player, ratings in player_ratings.items():
            player_states.add(
                await CreatePlayerStateAction(
                    context=self._context,
                    player=player,
                    last_match=last_match,
                    ratings=ratings,
                ).run()
            )

        return player_states

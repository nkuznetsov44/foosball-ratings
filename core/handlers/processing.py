from datetime import tzinfo
from typing import Iterator, Sequence

from utils import DatetimeWithTZ
from core.entities.state import RatingsState
from core.handlers.abstract_handler import AbstractHandler
from core.actions.processing import ProcessPlayersAction, ProcessCompetitionAction
from core.processing.calculation import RatingsCalculation



BASE_TZ = tzinfo()
DATE_2018_01_01 = DatetimeWithTZ(
    year=2018, month=1, day=1, hour=0, minute=0, second=0, tzinfo=BASE_TZ
)
DATE_2022_01_01 = DatetimeWithTZ(
    year=2022, month=1, day=1, hour=0, minute=0, second=0, tzinfo=BASE_TZ
)  # TODO: уточнить, с какого момента начали считать накопительный рейтинг и поправить



class ProcessPlayersHandler(AbstractHandler[ProcessPlayersAction]):
    async def handle(self, action: ProcessPlayersAction) -> RatingsState:
        pass


class ProcessCompetitionHandler(AbstractHandler[ProcessCompetitionAction]):
    async def handle(self, action: ProcessCompetitionAction) -> RatingsState:
        strategy = self._choose_calculation_strategy()

        for match in self._prepare_matches():
            for calculator in strategy.calculators:
                calculation_result = calculator.calculate(self.current_state, match, self.competition)
            player_states = await dispatch(CreatePlayerStatesAction(...))  # save intermediate player states
        
        return await dispatch(CreateRatingsStateAction(...))

    def _choose_calculation_strategy(self):
        if self.competition.end_datetime < DATE_2018_01_01:
            return strategies.Pre2018RatingCalculationStrategy
        elif self.competition.end_datetime < DATE_2022_01_01:
            return strategies.EvksOnlyRatingCalculationStrategy
        else:
            return strategies.EvksAndCumulativeRatingCalculationStrategy

    def _prepare_matches(self) -> Sequence[Match]:
        return sorted(self.competition.matches, key=lambda match: match.end_datetime)

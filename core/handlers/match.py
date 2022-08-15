from abstract_handler import AbstractHandler
from core.events import ProcessMatchEvent
from core.entities import RatingState
from processing.calculators.abstract_rating_calculator import RatingCalculationResult
from processing.strategies.abstract_calculation_strategy import AbstractCalculationStrategy


class ProcessMatchHandler(AbstractHandler[ProcessMatchEvent]):
    def __init__(self, calculation_strategy: AbstractCalculationStrategy) -> None:
        self.strategy = calculation_strategy

    async def handle(self, current_state: RatingState, event: ProcessMatchEvent) -> RatingCalculationResult:
        first_player_state = current_state.lookup_player_state(event.match.first_player)
        second_player_state = current_state.lookup_player_state(event.match.second_player)
        return await self.strategy.calculator.calculate(
            first_player_state, second_player_state, event.match
        )

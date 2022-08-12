from abstract_handler import AbstractHandler
from core.events import CreateMatchEvent
from core.entities import RatingState
from ..processing.strategies.abstract_calculation_strategy import AbstractCalculationStrategy


class CreateMatchHandler(AbstractHandler[CreateMatchEvent]):
    def __init__(self, calculation_strategy: AbstractCalculationStrategy) -> None:
        self.strategy = calculation_strategy

    async def handle(self, current_state: RatingState, event: CreateMatchEvent) -> RatingState:
        first_player_state = current_state.lookup_player_state(event.match.first_player)
        second_player_state = current_state.lookup_player_state(event.match.second_player)
        return await self.strategy.calculator.calculate(first_player_state, second_player_state, event.match)

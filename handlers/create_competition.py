
from hashlib import new
from abstract_handler import AbstractHandler
from core.events import CreateCompetitionEvent, CreateCompetitionStatus, CreateMatchEvent
from core.entities import RatingState
from handlers.create_match import CreateMatchHandler
from ..processing.calculators.abstract_rating_calculator import RatingCalculationResult
from processing.strategies.abstract_calculation_strategy import AbstractCalculationStrategy


class CreateCompetitionHandler(AbstractHandler[CreateCompetitionEvent]):
    def __init__(self, calculation_strategy: AbstractCalculationStrategy) -> None:
        self.create_match_handler = CreateMatchHandler(calculation_strategy)

    async def handle(self, current_state: RatingState, event: CreateCompetitionEvent) -> RatingState:
        new_state = RatingState(
            id=current_state.id + 1,
            player_states={**current_state.player_states},
            last_competition_id=event.competition.id
        )

        try:
            for match in event.matches:
                create_match_event = CreateMatchEvent(match)
                rating_calculation_result = await self.create_match_handler.handle(current_state, create_match_event)
                new_state.player_states.add(rating_calculation_result.first_player_new_state)
                new_state.player_states.add(rating_calculation_result.second_player_new_state)
            event.status = CreateCompetitionStatus.FINISHED
            return new_state
        except Exception:
            event.status = CreateCompetitionStatus.FAILED
            raise


from core.handlers.abstract_handler import AbstractHandler
from core.events import ProcessMatchEvent, ProcessCompetitionEvent
from core.entities import RatingState
from core.handlers.match import ProcessMatchHandler
from core.processing.strategies.abstract_calculation_strategy import AbstractCalculationStrategy


class CreateCompetitionHandler(AbstractHandler[ProcessCompetitionEvent]):
    def __init__(self, calculation_strategy: AbstractCalculationStrategy) -> None:
        self.create_match_handler = ProcessMatchHandler(calculation_strategy)

    async def handle(self, current_state: RatingState, event: ProcessCompetitionEvent) -> RatingState:
        new_state = RatingState(
            player_states={*current_state.player_states},  # тут надо убедиться, что это действительно deepcopy
            last_competition_id=event.competition.id
        )
        for match in event.competition.matches:
            create_match_event = ProcessMatchEvent(match)
            # Тут если хотим обновлять рейтинги после каждой игры - передаем new_state (грязный стейт к текущему моменту)
            # Но тогда надо посортить игры правильно перед этим
            # rating_calculation_result = await self.create_match_handler.handle(new_state, create_match_event)

            # или просто передаем current_state
            rating_calculation_result = await self.create_match_handler.handle(current_state, create_match_event)

            new_state.player_states.add(rating_calculation_result.first_player_new_state)
            new_state.player_states.add(rating_calculation_result.second_player_new_state)
        return new_state
        # потом вызываем flush_state(new_state: RatingState) - обновляем текущий current_state и пишем все в базу

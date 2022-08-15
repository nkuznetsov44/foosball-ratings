from core.actions.abstract_action import AbstractAction

from core.actions.competition import CreateCompetitionAction
from core.actions.match import CreateMatchAction, CreateTeamAction
from core.actions.player import CreatePlayerAction
from core.actions.processing import ProcessCompetitionAction, ProcessPlayersAction
from core.actions.state import CreatePlayerStateAction, CreateRatingsStateAction

from core.handlers.competition import CreateCompetitionHandler
from core.handlers.processing import ProcessCompetitionHandler, ProcessPlayersHandler
from core.handlers.state import CreatePlayerStateHandler, CreateRatingsStateHandler


class ActionsDispatcher:
    handlers = {
        CreateCompetitionAction: CreateCompetitionHandler
    }

    async def dispatch(action: AbstractAction) -> Any:
        pass

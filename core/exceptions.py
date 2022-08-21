from typing import ClassVar
from core.entities.state import RatingsState
from core.entities.player import Player
from core.entities.match import Match


class CoreProcessingError(Exception):
    REASON_CODE: ClassVar[str]

    def __init__(self, current_state: RatingsState) -> None:
        self.current_state = current_state
        self.reason = self.REASON_CODE or "UNEXPECTED_PROCESSING_ERROR"
        self.params = dict()
        super().__init__()


class PlayerStateNotFound(CoreProcessingError):
    REASON_CODE = "PLAYER_STATE_NOT_FOUND"

    def __init__(self, player: Player, current_state: RatingsState) -> None:
        super().__init__(current_state)
        self.params["player"] = str(player)


class PlayerStateAlreadyExists(CoreProcessingError):
    REASON_CODE = "PLAYER_STATE_ALREADY_EXISTS"

    def __init__(self, player: Player, current_state: RatingsState) -> None:
        super().__init__(current_state)
        self.params["player"] = str(player)


class PlayerStateSequenceError(CoreProcessingError):
    REASON_CODE = "NEW_MATCH_IS_BEFORE_LAST_PROCESSED_MATCH"

    def __init__(self, match: Match, current_state: RatingsState) -> None:
        super().__init__(current_state)
        self.params["match"] = str(match)

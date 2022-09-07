from typing import Any, ClassVar

from common.entities.ratings_state import RatingsState


class CoreProcessingError(Exception):
    REASON_CODE: ClassVar[str]

    def __init__(self, current_state: RatingsState) -> None:
        self.current_state = current_state
        self.reason = self.REASON_CODE or "UNEXPECTED_PROCESSING_ERROR"
        self.params: dict[str, Any] = dict()
        super().__init__()

    def __str__(self) -> str:
        return f"{super().__str__()}reason: {self.reason} params: {self.params}"


class PlayerStateNotFound(CoreProcessingError):
    REASON_CODE = "PLAYER_STATE_NOT_FOUND"

    def __init__(self, player_id: int, current_state: RatingsState) -> None:
        super().__init__(current_state)
        self.params["player_id"] = player_id


class PlayerStateAlreadyExists(CoreProcessingError):
    REASON_CODE = "PLAYER_STATE_ALREADY_EXISTS"

    def __init__(self, player_id: int, current_state: RatingsState) -> None:
        super().__init__(current_state)
        self.params["player_id"] = player_id


class PlayerStateSequenceError(CoreProcessingError):
    REASON_CODE = "NEW_MATCH_IS_BEFORE_LAST_PROCESSED_MATCH"

    def __init__(
        self, match_id: int, last_match_id: int, current_state: RatingsState
    ) -> None:
        super().__init__(current_state)
        self.params["match_id"] = match_id
        self.params["last_match_id"] = last_match_id

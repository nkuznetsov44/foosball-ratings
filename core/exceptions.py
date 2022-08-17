from core.entities.state import RatingsState
from core.entities.player import Player


class CoreProcessingError(Exception):
    def __init__(self, message: str, current_state: RatingsState) -> None:
        self.current_state = current_state
        super().__init__()


class PlayerStateNotFound(CoreProcessingError):
    def __init__(self, player: Player, current_state: RatingsState) -> None:
        self.player = player
        super().__init__(
            f"PlayerState of player {player} not found in current ratings state",
            current_state,
        )


class PlayerStateAlreadyExists(CoreProcessingError):
    def __init__(self, player: Player, current_state: RatingsState) -> None:
        self.player = player
        super().__init__(
            f"PlayerState of player {player} already exists", current_state
        )

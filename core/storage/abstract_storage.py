from abc import ABC, abstractmethod
from core.entities import RatingState


class AbstractRatingStateStorage(ABC):
    @abstractmethod
    def get_current_state(self) -> RatingState:
        # read current state from database here
        raise NotImplementedError()

    @abstractmethod
    def flush_state(self, state: RatingState) -> None:
        # save new rating state, and all players state bound to it
        raise NotImplementedError()

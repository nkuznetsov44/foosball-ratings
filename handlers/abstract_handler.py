from typing import Generic, TypeVar
from abc import ABC, abstractmethod
from core.entities import RatingState


EventType = TypeVar('EventType')


class AbstractHandler(Generic[EventType], ABC):
    @abstractmethod
    def handle(current_state: RatingState, event: EventType) -> RatingState:
        raise NotImplementedError()

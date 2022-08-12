from typing import Generic, TypeVar, Any
from abc import ABC, abstractmethod
from core.entities import RatingState


EventType = TypeVar('EventType')


class AbstractHandler(Generic[EventType], ABC):
    @abstractmethod
    def handle(current_state: RatingState, event: EventType) -> Any:
        raise NotImplementedError()

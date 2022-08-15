from typing import Generic, TypeVar, Any
from abc import ABC, abstractmethod


ActionType = TypeVar('ActionType')


class AbstractHandler(Generic[ActionType], ABC):
    @abstractmethod
    def handle(action: ActionType) -> Any:
        raise NotImplementedError()

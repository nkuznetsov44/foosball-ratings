from aiopg.sa.engine import Engine
from typing import Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
from core.entities.state import RatingsState


@dataclass
class ActionContext:
    db: Engine
    ratings_state: RatingsState


class AbstractAction(ABC):
    def __init__(self, context: ActionContext) -> None:
        self.context = context

    @abstractmethod
    async def run(self) -> Any:
        raise NotImplementedError()

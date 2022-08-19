from typing import Any, Type
from dataclasses import dataclass
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.entities.state import RatingsState


@dataclass
class ActionContext:
    db_engine: AsyncEngine
    ratings_state: RatingsState


class AbstractAction(ABC):
    def __init__(self, context: ActionContext) -> None:
        self._context = context

    @abstractmethod
    async def run(self) -> Any:
        raise NotImplementedError()

    @property
    def _ratings_state(self) -> RatingsState:
        return self._context.ratings_state

    def _make_db_session(self) -> Type[AsyncSession]:
        return sessionmaker(
            self._context.db_engine, expire_on_commit=False, class_=AsyncSession
        )

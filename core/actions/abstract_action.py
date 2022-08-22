from aiohttp.web import Application
from typing import Any, Type
from dataclasses import dataclass
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.entities.state import RatingsState


@dataclass
class ActionContext:
    app: Application

    @property
    def ratings_state(self) -> RatingsState:
        return self.app["ratings_state"]

    @ratings_state.setter
    def ratings_state(self, new_state: RatingsState) -> None:
        self.app["ratings_state"] = new_state

    @property
    def db_engine(self) -> AsyncEngine:
        return self.app["db"]


class AbstractAction(ABC):
    def __init__(self, context: ActionContext) -> None:
        self._context = context

    @abstractmethod
    async def run(self) -> Any:
        raise NotImplementedError()

    @property
    def ratings_state(self) -> RatingsState:
        return self._context.ratings_state

    def make_db_session(self) -> Type[AsyncSession]:
        return sessionmaker(
            self._context.db_engine, expire_on_commit=False, class_=AsyncSession
        )

    async def run_action(
        self, action_cls: Type["AbstractAction"], **kwargs: Any
    ) -> Any:
        return await action_cls(context=self._context, **kwargs).run()

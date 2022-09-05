from lib2to3.pytree import Base
from types import TracebackType
from typing import ClassVar, Type
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, AsyncSessionTransaction
from sqlalchemy.orm import sessionmaker

from common.entities.player import Player
from common.entities.state import PlayerState
from storage.entity_storage.base import BaseEntityStorage
from storage.entity_storage.state import RatingsStateStorage


# TODO:
# с сохранением нескольких сейчас вроде все ок, можно делать через context manager.
# а вот с получением одного или с сохранением одного хотелось бы так:
# ratings_state = await self.storage.ratings_states.get(id=1)
# Видимо, нужно как-то разделять transactional использование, тогда открывать
# сессию через context manager, и one-off использование, и спрятать логику с 
# открытием и закрытием сессии.


class Storage:
    def __init__(self, session: AsyncSessionTransaction) -> None:
        self._session = session

        self.players: BaseEntityStorage[Player] = BaseEntityStorage.for_entity(Player, session)
        self.ratings_states = RatingsStateStorage(session)
        self.player_states: BaseEntityStorage[PlayerState] = BaseEntityStorage.for_entity(PlayerState, session)

    @property
    def session(self) -> AsyncSessionTransaction:
        return self._session


class StorageContext:
    db_engine: ClassVar[AsyncEngine]

    @classmethod
    def setup_db_engine(cls, db_engine: AsyncEngine):
        cls.db_engine = db_engine

    @classmethod
    def get_sessionmaker(cls) -> Type[AsyncSession]:
        assert cls.db_engine is not None, "DB Engine is not set up"
        return sessionmaker(
            cls.db_engine, expire_on_commit=False, class_=AsyncSession,
        )

    def __init__(self) -> None:
        self._session_context = None

    async def __aenter__(self) -> Storage:
        self._session_context = self.get_sessionmaker().begin()
        session = await self._session_context.__aenter__()
        return Storage(session)

    async def __aexit__(self, exc_type: Type[Exception], exc: Exception, tb: TracebackType) -> None:
        await self._session_context.__aexit__(exc_type, exc, tb)

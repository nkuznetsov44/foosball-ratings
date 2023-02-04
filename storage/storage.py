from types import TracebackType
from typing import Optional, Type
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, AsyncSessionTransaction
from sqlalchemy.orm import sessionmaker

from common.entities.player import Player
from common.entities.player_state import PlayerState
from common.entities.tournament import Tournament
from common.entities.match import Team
from storage.entity_storage.base import BaseEntityStorage
from storage.entity_storage.match import MatchStorage
from storage.entity_storage.match_with_related import MatchWithRelatedStorage
from storage.entity_storage.sets import MatchSetStorage
from storage.entity_storage.ratings_state import RatingsStateStorage
from storage.entity_storage.competition import CompetitionStorage


class Storage:
    def __init__(self, session: AsyncSessionTransaction) -> None:
        self._session = session

        self.players: BaseEntityStorage[Player] = BaseEntityStorage.for_entity(Player, session)
        self.player_states: BaseEntityStorage[PlayerState] = BaseEntityStorage.for_entity(
            PlayerState, session
        )
        self.tournaments: BaseEntityStorage[Tournament] = BaseEntityStorage.for_entity(
            Tournament, session
        )
        self.teams: BaseEntityStorage[Team] = BaseEntityStorage.for_entity(Team, session)
        self.competitions = CompetitionStorage(session)
        self.matches = MatchStorage(session)
        self.matches_with_related = MatchWithRelatedStorage(session)
        self.sets = MatchSetStorage(session)
        self.ratings_states = RatingsStateStorage(session)

    @property
    def session(self) -> AsyncSessionTransaction:
        return self._session

    async def commit(self) -> None:
        await self._session.commit()


class StorageContext:
    db_engine: Optional[AsyncEngine] = None

    @classmethod
    def setup_db_engine(cls, db_engine: AsyncEngine) -> None:
        cls.db_engine = db_engine

    @classmethod
    def get_sessionmaker(cls) -> Type[AsyncSession]:
        assert cls.db_engine is not None, "DB Engine is not set up"
        return sessionmaker(
            cls.db_engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    def __init__(self) -> None:
        self._session_context = None

    async def __aenter__(self) -> Storage:
        self._session_context = self.get_sessionmaker().begin()
        session = await self._session_context.__aenter__()
        return Storage(session)

    async def __aexit__(self, exc_type: Type[Exception], exc: Exception, tb: TracebackType) -> None:
        await self._session_context.__aexit__(exc_type, exc, tb)

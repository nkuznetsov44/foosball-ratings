from typing import ClassVar, Type, TypeVar, Generic, Any, Optional
from sqlalchemy.sql.selectable import Select
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


Entity = TypeVar("Entity")


class BaseEntityStorage(Generic[Entity]):
    entity_cls: ClassVar[Type[Entity]]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _select_entity_query(self) -> Select:
        """Override if need to select with related"""
        return select(self.entity_cls)

    async def get(self, id: Any) -> Entity:
        result = await self._session.execute(
            self._select_entity_query().where(self.entity_cls.id == id)
        )
        return result.one()

    async def lst(self, limit: Optional[int] = None) -> list[Entity]:
        query = select(self.entity_cls)
        if limit:
            query = query.limit(limit)
        query = query.options(selectinload("*"))
        result = await self._session.execute(query)
        return result.scalars().all()

    async def create(self, entity: Entity) -> Entity:
        self._session.add(entity)
        await self._session.flush()
        assert entity.id is not None, f"{entity} id is None after creating"
        return entity

    @staticmethod
    def for_entity(
        entity_cls: Type[Entity], session: AsyncSession
    ) -> "BaseEntityStorage":
        storage = BaseEntityStorage(session)
        storage.entity_cls = entity_cls
        return storage

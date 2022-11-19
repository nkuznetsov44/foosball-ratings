from sqlalchemy import select

from common.entities.match import MatchSet
from storage.entity_storage.base import BaseEntityStorage


class MatchSetStorage(BaseEntityStorage):
    entity_cls = MatchSet

    async def find_by_match(self, match_id: int) -> list[MatchSet]:
        result = await self._session.execute(
            select(MatchSet)
            .filter(MatchSet.match_id == match_id)
        )
        return result.scalars().all()

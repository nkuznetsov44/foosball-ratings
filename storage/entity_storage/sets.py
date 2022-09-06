from sqlalchemy import select
from sqlalchemy.orm import selectinload

from common.entities.match import MatchSet, Match
from storage.entity_storage.base import BaseEntityStorage


class MatchSetStorage(BaseEntityStorage):
    entity_cls = MatchSet

    async def find_by_match(self, match_id: int) -> list[MatchSet]:
        result = await self._session.execute(
            select(MatchSet)
            .filter(MatchSet.match.has(Match.id == match_id))
            .options(selectinload(MatchSet.match))
        )
        return result.scalars().all()

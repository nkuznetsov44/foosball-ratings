from sqlalchemy import select
from sqlalchemy.orm import selectinload

from common.entities.match import Match
from common.entities.competition import Competition
from storage.entity_storage.base import BaseEntityStorage


class MatchStorage(BaseEntityStorage):
    entity_cls = Match

    async def find_by_competition(self, competition_id: int) -> list[Match]:
        result = await self._session.execute(
            select(Match)
            .filter(Match.competition.has(Competition.id == competition_id))
            .options(selectinload(Match.competition))
        )
        return result.scalars().all()

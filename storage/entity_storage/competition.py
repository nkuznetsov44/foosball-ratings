from common.entities.competition import Competition
from common.entities.tournament import Tournament
from storage.entity_storage.base import BaseEntityStorage


class CompetitionStorage(BaseEntityStorage):
    entity_cls = Competition

    async def find_by_player(self, player_id: int) -> list[Competition]:
        raise NotImplementedError

    async def find_by_tournament(self, tournament_id: int) -> list[Competition]:
        result = await self._session.execute(
            self._select_entity_query().filter(
                Competition.tournament.has(Tournament.id == tournament_id)
            )
        )
        return result.scalars().all()

from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.selectable import Select

from common.entities.competition import Competition
from common.entities.tournament import Tournament
from common.entities.team import Team
from common.entities.player import Player
from storage.entity_storage.base import BaseEntityStorage


class CompetitionStorage(BaseEntityStorage):
    entity_cls = Competition

    def _select_entity_query(self) -> Select:
        return select(Competition).options(joinedload(Competition.tournament))

    async def find_by_player(self, player_id: int) -> list[Competition]:
        result = await self._session.execute(
            self._select_entity_query()
            .join(Team)
            .filter(
                or_(
                    Team.first_player.has(Player.id == player_id),
                    Team.second_player.has(Player.id == player_id),
                )
            )
        )
        return result.scalars().all()

    async def find_by_tournament(self, tournament_id: int) -> list[Competition]:
        result = await self._session.execute(
            self._select_entity_query().filter(
                Competition.tournament.has(Tournament.id == tournament_id)
            )
        )
        return result.scalars().all()

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.selectable import Select

from common.entities.match import Match
from common.entities.team import Team
from common.entities.player import Player
from storage.entity_storage.base import BaseEntityStorage


class MatchStorage(BaseEntityStorage):
    entity_cls = Match

    def _select_entity_query(self) -> Select:
        return select(Match).options(
            joinedload(Match.first_team).options(
                joinedload(Team.first_player),
                joinedload(Team.second_player),
            ),
            joinedload(Match.second_team).options(
                joinedload(Team.first_player),
                joinedload(Team.second_player),
            ),
        )

    async def find_by_competition(self, competition_id: int) -> list[Match]:
        result = await self._session.execute(
            self._select_entity_query().filter(Match.competition_id == competition_id)
        )
        return result.scalars().all()

    async def find_by_player_and_competition(
        self, player_id: int, competition_id: int
    ) -> list[Match]:
        result = await self._session.execute(
            self._select_entity_query()
            .filter(Match.competition_id == competition_id)
            .filter(
                (Match.first_team.has(Team.first_player.has(Player.id == player_id)))
                | (Match.first_team.has(Team.second_player.has(Player.id == player_id)))
                | (Match.second_team.has(Team.first_player.has(Player.id == player_id)))
                | (Match.second_team.has(Team.first_player.has(Player.id == player_id)))
            )
        )
        return result.scalars().all()

from sqlalchemy import select
from sqlalchemy.orm import joinedload, subqueryload
from sqlalchemy.sql.selectable import Select

from common.entities.match import MatchWithRelated
from common.entities.team import Team
from common.entities.player import Player
from common.entities.player_state import PlayerState
from storage.entity_storage.base import BaseEntityStorage


class MatchWithRelatedStorage(BaseEntityStorage):
    entity_cls = MatchWithRelated

    def _select_entity_query(self) -> Select:
        return select(MatchWithRelated).options(
            joinedload(MatchWithRelated.first_team).options(
                joinedload(Team.first_player),
                joinedload(Team.second_player),
            ),
            joinedload(MatchWithRelated.second_team).options(
                joinedload(Team.first_player),
                joinedload(Team.second_player),
            ),
            subqueryload(MatchWithRelated.sets),
            subqueryload(MatchWithRelated.player_states).options(
                joinedload(PlayerState.player),
            ),
        )

    async def find_by_player_and_competition(
        self, player_id: int, competition_id: int
    ) -> list[MatchWithRelated]:
        result = await self._session.execute(
            self._select_entity_query()
            .filter(MatchWithRelated.competition_id == competition_id)
            .filter(
                (MatchWithRelated.first_team.has(Team.first_player.has(Player.id == player_id)))
                | (MatchWithRelated.first_team.has(Team.second_player.has(Player.id == player_id)))
                | (MatchWithRelated.second_team.has(Team.first_player.has(Player.id == player_id)))
                | (MatchWithRelated.second_team.has(Team.first_player.has(Player.id == player_id)))
            )
        )
        return result.scalars().all()

from sqlalchemy import select
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy.sql.selectable import Select

from common.entities.player_state import PlayerState
from common.entities.ratings_state import RatingsState
from storage.entity_storage.base import BaseEntityStorage


class RatingsStateStorage(BaseEntityStorage):
    entity_cls = RatingsState

    def _select_entity_query(self) -> Select:
        return select(RatingsState).options(
            subqueryload(RatingsState.player_states).options(
                joinedload(PlayerState.last_match).options(
                    # joinedload(Match.competition).options(
                    #    joinedload(Competition.tournament),
                    # ),
                    # joinedload(Match.first_team).options(
                    #    joinedload(Team.first_player),
                    #    joinedload(Team.second_player),
                    #    joinedload(Team.competition).options(
                    #        joinedload(Competition.tournament),
                    #    ),
                    # ),
                    # joinedload(Match.second_team).options(
                    #    joinedload(Team.first_player),
                    #    joinedload(Team.second_player),
                    #    joinedload(Team.competition).options(
                    #        joinedload(Competition.tournament),
                    #    ),
                    # ),
                ),
                joinedload(PlayerState.player),
            ),
            joinedload(RatingsState.last_competition),
            # joinedload(RatingsState.last_competition).options(
            #    joinedload(Competition.tournament),
            # ),
        )

    async def get_actual(self) -> RatingsState:
        # TODO: order_by, limit 1, subqueryload
        result = await self._session.execute(
            self._select_entity_query()
            # .filter(RatingsState.status==RatingsStateStatus.PUBLISHED)  # FIXME
            .order_by(RatingsState.id.desc())  # TODO: fixme
        )
        return result.scalars().first()

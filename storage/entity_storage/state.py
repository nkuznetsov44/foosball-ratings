from sqlalchemy import select
from sqlalchemy.orm import subqueryload, selectinload
from sqlalchemy.sql.selectable import Select

from common.entities.state import PlayerState, RatingsState
from common.entities.match import Match
from common.entities.competition import Competition
from storage.entity_storage.base import BaseEntityStorage


class RatingsStateStorage(BaseEntityStorage):
    entity_cls = RatingsState

    def _select_query_with_related(self) -> Select:
        return select(RatingsState).options(
            subqueryload(RatingsState.player_states).options(
                selectinload(PlayerState.last_match).options(
                    selectinload(Match.competition).options(
                        selectinload(Competition.tournament),
                    ),
                    selectinload(Match.first_team),
                    selectinload(Match.second_team),
                ),
                selectinload(PlayerState.player),
            ),
            selectinload(RatingsState.last_competition).options(
                selectinload(Competition.tournament),
            ),
        )

    async def get(self, id: int) -> RatingsState:
        result = await self._session.execute(
            self._select_query_with_related().where(RatingsState.id == id)
        )
        # TODO: raise EntityNotFoundError if not found
        return result.scalars().first()

    async def get_actual(self) -> RatingsState:
        # TODO: order_by, limit 1, subqueryload
        result = await self._session.execute(
            self._select_query_with_related().order_by(
                RatingsState.id.desc()
            )  # TODO: fixme
        )
        return result.scalars().first()

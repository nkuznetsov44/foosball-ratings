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
                joinedload(PlayerState.player),
            ),
        )

    async def get_actual(self) -> RatingsState:
        # TODO: maybe cache RS by id
        result = await self._session.execute(
            self._select_entity_query().order_by(RatingsState.id.desc()).limit(1)
        )
        return result.one()[0]

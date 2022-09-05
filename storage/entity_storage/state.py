from sqlalchemy import select
from sqlalchemy.orm import subqueryload, selectinload

from common.entities.state import PlayerState, RatingsState
from storage.entity_storage.base import BaseEntityStorage


class RatingsStateStorage(BaseEntityStorage):
    entity_cls = RatingsState

    async def get(self, id: int) -> RatingsState:
        result = await self._session.execute(
            select(RatingsState)
            .options(
                subqueryload(RatingsState.player_states)
                .options(
                    selectinload(PlayerState.last_match),
                    selectinload(PlayerState.player)
                )
            )
            .where(RatingsState.id == id)   
        )
        # TODO: raise EntityNotFoundError if not found
        return result.scalars().first()

    async def get_actual(self) -> RatingsState:
        # TODO: order_by, limit 1, then subqueryload
        result = await self._session.execute(
            select(RatingsState)
            .options(
                subqueryload(RatingsState.player_states)
                .options(
                    selectinload(PlayerState.last_match),
                    selectinload(PlayerState.player)
                )
            )
            .order_by(RatingsState.id.desc())  # TODO: fixme
        )
        # TODO: raise EntityNotFoundError if not found
        r = result.scalars().first()
        # print(r)
        return r

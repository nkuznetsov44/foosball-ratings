from typing import Type, Any
from sqlalchemy.ext.asyncio import AsyncEngine
from common.handlers.abstract_handler import AbstractHandler
from core.actions.abstract_action import AbstractAction, ActionContext
from core.entities.state import RatingsState


class AbstractDbHandler(AbstractHandler):
    @property
    def db_engine(self) -> AsyncEngine:
        return self.app["db"]

    def _get_action_context(self) -> ActionContext:
        return ActionContext(
            db_engine=self.db_engine,
            ratings_state=RatingsState(  # TODO: fixme
                previous_state_id=0,
                player_states=set(),
                player_evks_ranks=dict(),
                last_competition=None,
            ),
        )

    async def run_action(self, action_cls: Type[AbstractAction], **kwargs: Any) -> Any:
        return await action_cls(context=self._get_action_context(), **kwargs).run()

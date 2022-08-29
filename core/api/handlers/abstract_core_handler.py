from typing import Any, Type

from common.handlers import AbstractHandler
from core.actions.abstract_action import AbstractAction, ActionContext


class AbstractCoreHandler(AbstractHandler):
    def _get_action_context(self) -> ActionContext:
        return ActionContext(app=self.app)

    async def run_action(self, action_cls: Type[AbstractAction], **kwargs: Any) -> Any:
        return await action_cls(context=self._get_action_context(), **kwargs).run()

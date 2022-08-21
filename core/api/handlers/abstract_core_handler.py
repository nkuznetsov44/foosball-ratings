from aiohttp import web
from typing import Type, Any
from common.handlers import AbstractHandler
from core.actions.abstract_action import AbstractAction, ActionContext
from core.exceptions import CoreProcessingError


class AbstractCoreHandler(AbstractHandler):
    def _get_action_context(self) -> ActionContext:
        return ActionContext(app=self.app)

    def make_error_response(self, error: CoreProcessingError) -> web.Response:
        # TODO: logger.exception
        return web.json_response({"reason": error.reason, "params": error.params})

    async def run_action(self, action_cls: Type[AbstractAction], **kwargs: Any) -> Any:
        return await action_cls(context=self._get_action_context(), **kwargs).run()

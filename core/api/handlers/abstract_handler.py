from typing import Any
from aiohttp import web
from core.actions.abstract_action import AbstractAction


class AbstractHandler(web.view):
    @property
    def app(self) -> web.Application:
        return self.request.app

    async def run_action(self, action: AbstractAction) -> Any:
        # TODO: handle action errors here
        return await action.run()

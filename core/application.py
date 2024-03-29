from typing import Any
import logging
from aiohttp import web

from common.middlewares import malformed_request_400_middleware
from core.api.middlewares import core_processing_error_500_middleware
from core.routes import setup_routes
from core.settings import config
from storage.db import setup_storage


logging.basicConfig(level=logging.DEBUG)


async def make_app(cfg: dict[str, Any]) -> web.Application:
    app = web.Application(
        middlewares=[
            malformed_request_400_middleware,  # type: ignore
            core_processing_error_500_middleware,  # type: ignore
        ]
    )
    setup_routes(app)
    setup_storage(cfg, echo=False)
    return app


if __name__ == "__main__":
    web.run_app(make_app(config), port=8080)  # TODO: to settings

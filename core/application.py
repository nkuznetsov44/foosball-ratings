from logging import getLogger
from aiohttp import web

from common.middlewares import malformed_request_400_middleware
from core.api.middlewares import core_processing_error_500_middleware
from core.routes import setup_routes
from settings import config
from storage.db import setup_storage


logger = getLogger(__name__)


async def make_app() -> web.Application:
    app = web.Application(
        middlewares=[
            malformed_request_400_middleware,  # type: ignore
            core_processing_error_500_middleware,  # type: ignore
        ]
    )
    setup_routes(app)
    setup_storage(config, echo=True)
    return app


if __name__ == "__main__":
    web.run_app(make_app(), port=8080)  # TODO: to settings

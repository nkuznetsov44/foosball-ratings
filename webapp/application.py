from logging import getLogger

from aiohttp import web

from common.middlewares import malformed_request_400_middleware
from settings import config
from storage.db import setup_db_engine
from webapp.routes import setup_routes

logger = getLogger(__name__)


async def make_app() -> web.Application:
    app = web.Application(
        middlewares=[
            malformed_request_400_middleware,  # type: ignore
        ]
    )
    setup_routes(app)
    app["config"] = config
    setup_db_engine(app, echo=True)
    return app


if __name__ == "__main__":
    web.run_app(make_app())

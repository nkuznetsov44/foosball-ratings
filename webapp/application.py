from logging import getLogger
from aiohttp import web

from common.middlewares import malformed_request_400_middleware
from webapp.routes import setup_routes


logger = getLogger(__name__)


async def make_app() -> web.Application:
    app = web.Application(
        middlewares=[
            malformed_request_400_middleware,  # type: ignore
        ]
    )
    setup_routes(app)
    return app


if __name__ == "__main__":
    web.run_app(make_app(), port=8081)  # TODO: to settings

from aiohttp import web
from core.api.handlers.player import PlayersHandler


def setup_routes(app: web.Application) -> None:
    app.router.add_view("/players", PlayersHandler)

from aiohttp import web
from core.api.handlers.player import PlayersHandler
from core.api.handlers.competition import CompetitionHandler


def setup_routes(app: web.Application) -> None:
    app.router.add_view("/players", PlayersHandler)
    app.router.add_view("/competitions", CompetitionHandler)

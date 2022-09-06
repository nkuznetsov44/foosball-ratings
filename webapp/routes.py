from aiohttp import web

from webapp.handlers import PlayerCompetitionsHandler, PlayersHandler


def setup_routes(app: web.Application) -> None:
    app.router.add_view("/players", PlayersHandler)
    app.router.add_view("/players/{player_id}/competitions", PlayerCompetitionsHandler),
    # app.router.add_view(
    #     "/players/{player_id}/competitions/{competition_id}/matches",
    #     GetPlayerCompetitionMatchesHandler,
    # )

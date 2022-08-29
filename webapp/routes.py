from aiohttp import web

from webapp.handlers import GetPlayerCompetitionsHandler, GetPlayersHandler


def setup_routes(app: web.Application) -> None:
    app.router.add_view("/players", GetPlayersHandler)
    app.router.add_view(
        "/players/{player_id}/competitions", GetPlayerCompetitionsHandler
    ),
    # app.router.add_view(
    #     "/players/{player_id}/competitions/{competition_id}/matches",
    #     GetPlayerCompetitionMatchesHandler,
    # )

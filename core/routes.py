from aiohttp import web

from core.api.handlers.player import (
    PlayersHandler,
    PlayerHandler,
    PlayerCompetitionsHandler,
    PlayerCompetitionMatchesHandler,
)
from core.api.handlers.state import RatingsStateHandler
from core.api.handlers.tournament import TournamentHandler


def uri_v1(uri: str) -> str:
    return f"/api/v1/{uri}"


def setup_routes(app: web.Application) -> None:
    app.router.add_view(uri_v1("players/{player_id}"), PlayerHandler)
    app.router.add_view(uri_v1("players"), PlayersHandler)
    app.router.add_view(
        uri_v1("players/{player_id}/competitions"), PlayerCompetitionsHandler
    )
    app.router.add_view(
        uri_v1("players/{player_id}/competitions/{competition_id}/matches"),
        PlayerCompetitionMatchesHandler,
    )
    app.router.add_view(uri_v1("tournaments"), TournamentHandler)
    app.router.add_view(uri_v1("ratings_state"), RatingsStateHandler)

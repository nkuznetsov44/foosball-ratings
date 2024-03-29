from aiohttp import web

from webapp.handlers import (
    PlayersHandler,
    PlayerCompetitionsHandler,
    PlayerCompetitionMatchesHandler,
    RatingsStateHandler,
    RefereesHandler,
    TournamentsHandler,
    TournamentCompetitionsHandler,
    ExternalRatingsStateHandler,
)


def setup_routes(app: web.Application) -> None:
    app.router.add_view("/players", PlayersHandler)
    app.router.add_view("/players/{player_id}/competitions", PlayerCompetitionsHandler),
    app.router.add_view(
        "/players/{player_id}/competitions/{competition_id}/matches",
        PlayerCompetitionMatchesHandler,
    )
    app.router.add_view("/tournaments", TournamentsHandler)
    app.router.add_view(
        "/tournaments/{tournament_id}/competitions",
        TournamentCompetitionsHandler,
    )
    app.router.add_view("/ratings_state", RatingsStateHandler)
    app.router.add_view("/referees", RefereesHandler)

    app.router.add_view("/external/v1/ratings_state", ExternalRatingsStateHandler)

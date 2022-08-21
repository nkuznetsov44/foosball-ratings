from aiohttp import web
from common.middlewares import malformed_request_400_middleware
from core.api.middlewares import core_processing_error_500_middleware
from core.settings import config
from core.routes import setup_routes
from core.storage.db import setup_db_engine
from core.entities.state import RatingsState


app = web.Application(
    middlewares=[malformed_request_400_middleware, core_processing_error_500_middleware]
)
setup_routes(app)
app["config"] = config
setup_db_engine(app, echo=True)


# TODO: fixme
app["ratings_state"] = RatingsState(
    previous_state_id=None,
    last_competition=None,
    player_states=set(),
    evks_player_ranks=dict(),
)


if __name__ == "__main__":
    web.run_app(app)

from logging import getLogger

from aiohttp import web
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, sessionmaker

from common.entities.state import RatingsState
from common.middlewares import malformed_request_400_middleware
from core.api.middlewares import core_processing_error_500_middleware
from core.routes import setup_routes
from settings import config
from storage.db import setup_db_engine

logger = getLogger(__name__)


_initial_ratings_state = RatingsState(
    previous_state_id=None,
    last_competition=None,
    player_states={},
    evks_player_ranks={},
)


async def init_ratings_state(app: web.Application) -> None:
    db_engine = app.get("db")
    if not db_engine:
        raise KeyError("Set app['db'] before calling init_ratings_state")

    async with sessionmaker(
        db_engine, expire_on_commit=False, class_=AsyncSession
    )() as session:
        exists_result = await session.execute(select(RatingsState))
        exists = exists_result.scalars().first() is not None

        if not exists:
            ratings_state = _initial_ratings_state
            session.add(ratings_state)
            await session.commit()

        # TODO: order by timestamp_created, not id
        result = await session.execute(
            select(RatingsState)
            .options(selectinload("*"))
            .order_by(RatingsState.id.desc())  # type: ignore
        )
        ratings_state = result.scalars().first()

        app["ratings_state"] = ratings_state
        logger.info(f"Initialized app with ratings state {ratings_state}")


async def make_app() -> web.Application:
    app = web.Application(
        middlewares=[
            malformed_request_400_middleware,  # type: ignore
            core_processing_error_500_middleware,  # type: ignore
        ]
    )
    setup_routes(app)
    app["config"] = config
    setup_db_engine(app, echo=True)
    await init_ratings_state(app)
    return app


if __name__ == "__main__":
    web.run_app(make_app())

from typing import Optional
from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine

from storage.mapping import mapper_registry


def setup_db_engine(app: web.Application, echo: Optional[bool] = False) -> None:
    db_cfg = app["config"]["postgres"]
    connection_string = (
        "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **db_cfg
        )
    )
    app["db"] = create_async_engine(connection_string, echo=echo)
    mapper_registry.configure()

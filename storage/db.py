from typing import Optional, Any
from sqlalchemy.ext.asyncio import create_async_engine

from storage.mapping import mapper_registry
from storage.storage import StorageContext


def setup_storage(config: dict[str, Any], echo: Optional[bool] = False) -> None:
    db_cfg = config["postgres"]
    connection_string = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
        **db_cfg
    )
    engine = create_async_engine(connection_string, echo=echo)
    mapper_registry.configure()
    StorageContext.setup_db_engine(engine)

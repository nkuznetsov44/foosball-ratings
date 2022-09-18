import uuid

from sqlalchemy import create_engine

import pytest
import pytest_asyncio
from sqlalchemy_utils.functions import create_database, drop_database

from storage.storage import StorageContext
from storage.db import setup_storage
from storage.schema.create_schema import create_schema

from core.tests.stored_entities import *  # noqa


@pytest.fixture
def tempdb() -> str:
    name = ".".join([uuid.uuid4().hex, "pytest"])
    url = f"postgresql://ratings:ratings@localhost:5432/{name}"

    create_database(url)
    try:
        engine = create_engine(url)
        create_schema(engine)
        yield name
    finally:
        drop_database(url)


@pytest.fixture
def storage_context(tempdb) -> StorageContext:
    config = {
        "postgres": {
            "user": "ratings",
            "password": "ratings",
            "host": "localhost",
            "port": 5432,
            "database": tempdb,
        }
    }
    setup_storage(config)
    return StorageContext


@pytest_asyncio.fixture
async def storage(storage_context):
    async with storage_context() as storage:
        yield storage

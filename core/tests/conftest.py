from typing import Any
import uuid

from sqlalchemy import create_engine

import pytest
import pytest_asyncio
from sqlalchemy_utils.functions import create_database, drop_database

from storage.storage import StorageContext
from storage.db import setup_storage
from storage.schema.create_schema import create_schema

from core.application import make_app

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
def app_config(tempdb) -> dict[str, Any]:
    return {
        "postgres": {
            "user": "ratings",
            "password": "ratings",
            "host": "localhost",
            "port": 5432,
            "database": tempdb,
        }
    }


@pytest.fixture
def storage_context(app_config) -> StorageContext:
    setup_storage(app_config)
    return StorageContext


@pytest_asyncio.fixture
async def storage(storage_context):
    async with storage_context() as storage:
        yield storage


@pytest_asyncio.fixture
async def core_client(aiohttp_client, app_config):
    return await aiohttp_client(await make_app(app_config))


@pytest.fixture
def mock_action(mocker, storage_context):
    def _mocker(action, action_result):
        init_mock = mocker.Mock(return_value=None)
        mocker.patch.object(action, "__init__", init_mock)
        handle_mock = mocker.AsyncMock(return_value=action_result)
        mocker.patch.object(action, "handle", handle_mock)
        return init_mock

    return _mocker

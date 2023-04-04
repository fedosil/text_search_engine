import asyncio
import datetime
import time

from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.database import get_async_session, es_base_client
from src.models import metadata, document
from src.config import (DB_TEST_HOST, DB_TEST_NAME, DB_TEST_PASS, DB_TEST_PORT, DB_TEST_USER)
from src.main import app

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_TEST_USER}:{DB_TEST_PASS}@{DB_TEST_HOST}:{DB_TEST_PORT}/{DB_TEST_NAME}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test

test_index_name = 'test_document'


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_elasticsearch():
    es_base_client.create(index=test_index_name, id=1, document={
        'id': 1,
        'text': 'test',
    })
    time.sleep(1)
    yield
    es_base_client.indices.delete(index=test_index_name)


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
        stmt = insert(document).values(id=1, text='test', created_date=datetime.datetime(2019, 1, 20, 14, 9, 2),
                                       rubrics=['VK-1603736028819866', 'VK-75740592382', 'VK-34023136930'])
        await conn.execute(stmt)
        await conn.commit()
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)

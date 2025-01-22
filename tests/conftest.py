import pytest
import pytest_asyncio

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from core.db import Base, get_async_session
from core.config import test_database_settings


engine_test = create_async_engine(test_database_settings.database_url, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False, autoflush=False)

Base.metadata.bind = engine_test

pytest_plugins = [
    "fixtures.user",
]


async def override_db():
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    yield
    async with engine_test.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())
        conn.commit()

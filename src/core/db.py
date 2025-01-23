from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeMeta,
    Mapped,
    declarative_base,
    declared_attr,
    mapped_column,
    sessionmaker,
)

from core.config import settings


class PreBase:
    """Base model."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Autocreate tablename."""
        cls.__name__: str
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="Номер в базе данных",
    )


Base: DeclarativeMeta = declarative_base(cls=PreBase)

engine: AsyncEngine = create_async_engine(
    settings.database_url, pool_pre_ping=True
)

AsyncSessionLocal: AsyncSession = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    """Async sessionmaker."""
    async with AsyncSessionLocal() as async_session:
        yield async_session

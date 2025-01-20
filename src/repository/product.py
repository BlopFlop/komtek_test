from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from repository.base import RepositoryBase
from models.product import Product


async def get_product_repository(
    session: AsyncSession = Depends(get_async_session),
) -> RepositoryBase:
    """Create product repository."""
    return RepositoryBase(Product, session=session)

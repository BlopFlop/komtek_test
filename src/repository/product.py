from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from repository.base import RepositoryBase
from models.product import Product
from schemas import ProductSchemaDB, ProductSchemaCreate


class ProductRepository(RepositoryBase):

    async def create_or_update(
        self,
        product_in: ProductSchemaCreate
    ) -> ProductSchemaDB:
        product_db = await self.get_obj_for_field_arg(
            field="article",
            arg=product_in.article,
            many=False
        )
        if product_db:
            return await self.update(product_db, product_in)
        return await self.create(product_in)


async def get_product_repository(
    session: AsyncSession = Depends(get_async_session),
) -> ProductRepository:
    """Create product repository."""
    return ProductRepository(Product, session=session)

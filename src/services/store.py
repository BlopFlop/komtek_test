from typing import Any
import aiohttp

from fastapi import Depends

from schemas import ProductSchemaGetFromStore, ProductSchemaCreate, ProductSchemaUpadate, ProductSchemaDB
from sqlalchemy.ext.asyncio import AsyncSession
from repository import RepositoryBase
from core.config import settings
from core.constants import STORE_URL_GET_PRODUCT


async def get_product_from_store(
    session: AsyncSession,
    url: str
) -> dict[str, Any]:
    async with session.get(url) as response:
        data: dict[str: Any] = await response.json()
        return data


async def create_or_update_product_from_store(
    get_schema_product: ProductSchemaGetFromStore,
    product_repository: RepositoryBase,
) -> ProductSchemaDB:
    url = STORE_URL_GET_PRODUCT.format(
        settings.key_store,
        get_schema_product.artikul
    )
    session = product_repository.session

    data_product = await get_product_from_store(session, url)

    project_db: ProductSchemaDB = await product_repository.get_obj_for_field_arg(
        field="artikul",
        arg=get_schema_product.artikul,
        many=False
    )
    if project_db:
        project_update = ProductSchemaUpadate(
            pass
        )
        project_db = await product_repository.update(
            project_db,
            project_update
        )
    else:
        project_create = ProductSchemaCreate(
            pass
        )
        project_db = await product_repository.create(project_create)
    return project_db


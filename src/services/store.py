from typing import Any, Coroutine
import logging

import aiohttp

from fastapi.exceptions import HTTPException
from schemas import ProductSchemaGetFromStore, ProductSchemaCreate, ProductSchemaUpadate, ProductSchemaDB
from sqlalchemy.ext.asyncio import AsyncSession
from repository import RepositoryBase
from core.config import settings
from core.constants import STORE_URL_GET_PRODUCT, STORE_KEY_RATING, STORE_KEY_PRICE, STORE_KEY_NAME, STORE_KEY_TOTAL


async def get_product_from_store(url: str) -> dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json_response: dict[str, Any] = await response.json()
            data: dict[str: Any] = json_response.get("data")
            data_products: dict[str: Any] = data.get("products")[0]
            return data_products


async def create_or_update_product_from_store(
    article: int,
    repository_product: RepositoryBase,
) -> ProductSchemaDB:
    """Create or update product from db by article."""
    url = STORE_URL_GET_PRODUCT.format(settings.key_store, article)

    data_product: dict[str, Any] = await get_product_from_store(url)

    project_db: ProductSchemaDB = (
        await repository_product.get_obj_for_field_arg(
            field="article",
            arg=article,
            many=False
        )
    )

    name = data_product.get(STORE_KEY_NAME)
    price = data_product.get(STORE_KEY_PRICE)
    rating = data_product.get(STORE_KEY_RATING)
    total = data_product.get(STORE_KEY_TOTAL)

    if not all((name, price, rating, total)):
        except_message = (
            "При получении данных о товаре в магазине "
            "через API, произошла ошибка."
        )
        logging.error(except_message)
        if project_db:
            return project_db
        raise HTTPException(status_code=500, detail=except_message)

    price = float(price / 100)

    if project_db:
        project_update = ProductSchemaUpadate(
            name=name,
            price=price,
            rating=rating,
            total=total
        )
        project_db = await repository_product.update(
            project_db,
            project_update
        )
        logging.info(f"Обновлен товар в базе данных {project_db}.")
    else:
        project_create = ProductSchemaCreate(
            name=name,
            article=article,
            price=price,
            rating=rating,
            total=total
        )
        project_db = await repository_product.create(project_create)
        logging.info(f"Создан товар в базе данных {project_db}.")
    return project_db

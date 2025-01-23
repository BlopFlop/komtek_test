import contextlib
import logging
from typing import Any

import aiohttp
from fastapi.exceptions import HTTPException

from core.config import settings
from core.constants import (
    STORE_KEY_ARTICLE,
    STORE_KEY_DATA,
    STORE_KEY_NAME,
    STORE_KEY_PRICE,
    STORE_KEY_PRODUCT,
    STORE_KEY_RATING,
    STORE_KEY_TOTAL,
    STORE_URL_GET_PRODUCT,
)
from core.db import get_async_session
from repository import ProductRepository, get_product_repository
from schemas import ProductSchemaCreate, ProductSchemaDB

get_async_session_context = contextlib.asynccontextmanager(get_async_session)


def get_store_url(article: int) -> str:
    url = STORE_URL_GET_PRODUCT.format(settings.key_store, article)
    logging.info(f"Адрес магазина {url}")
    return url


def _get_field_from_api(data: dict[str, Any]):
    fields = {
        STORE_KEY_ARTICLE: "article",
        STORE_KEY_NAME: "name",
        STORE_KEY_PRICE: "price",
        STORE_KEY_RATING: "rating",
        STORE_KEY_TOTAL: "total",
    }

    if STORE_KEY_DATA not in data:
        except_message = (
            "API магазина отдает неккоректные данные. "
            "Возможности получить товар по артикулу нет"
        )
        logging.error(except_message)
        raise HTTPException(500, detail=except_message)

    data = data.get(STORE_KEY_DATA)

    if STORE_KEY_PRODUCT not in data:
        except_message = (
            "API магазина отдает неккоректные данные. "
            "Возможности получить товар по артикулу нет"
        )
        logging.error(except_message)
        raise HTTPException(500, detail=except_message)

    data = data.get(STORE_KEY_PRODUCT)

    if not data:
        except_message = "Передан несуществующий артикль в магазине."
        logging.warning(except_message)
        raise HTTPException(400, detail=except_message)

    data = data[0]

    product_values = {}
    for key, field in fields.items():
        if key not in data:
            except_message = (
                f"API магазина отдает неккоректные данные. Поля {key}"
                "Больше не существует. Возможности получить товар по "
                "артикулу нет"
            )
            logging.error(except_message)
            raise HTTPException(500, detail=except_message)

        value = data.get(key)

        if STORE_KEY_PRICE == key:
            value = float(value / 100)

        product_values[field] = value
    return product_values


async def get_data_from_store(url: str) -> dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                except_message = (
                    "Сервис магазина недоступен, данные не доступны."
                )
                logging.error(except_message)
                raise HTTPException(500, detail=except_message)
            data: dict[str, Any] = await response.json()
    data_product = _get_field_from_api(data)
    logging.info(f"Получен товар со значениями {data_product}")
    return data_product


async def create_or_update_product_from_store(
    article: int, repository: ProductRepository, perform_update: bool = False
) -> ProductSchemaDB:
    store_url = get_store_url(article)
    product_values = await get_data_from_store(url=store_url)
    if perform_update:
        product_values["perform_update"] = perform_update
    product_in = ProductSchemaCreate(**product_values)
    return await repository.create_or_update(product_in)


async def perform_update_products_from_store() -> None:
    async with get_async_session_context() as session:
        repository_product: ProductRepository = await get_product_repository(
            session
        )
        products: list[ProductSchemaDB] = (
            await repository_product.get_obj_for_field_arg(
                field="perform_update", arg=True, many=True
            )
        )
        for product in products:
            update_product = await create_or_update_product_from_store(
                product.article, repository_product
            )
            logging.info(
                f"Товар артикль {update_product.article} "
                "будет обновляться каждые 30 минут."
            )

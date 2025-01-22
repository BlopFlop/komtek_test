from typing import Any

import pytest

from conftest import async_session_maker
from fastapi.testclient import TestClient

from repository import get_product_repository, ProductRepository
from schemas import ProductSchemaDB

from fixtures.products import (
    product_1,
    product_2,
    product_3,

    valid_article_1,
    valid_article_2,
    valid_article_3,

    invalid_article_1,
    invalid_article_2,
    invalid_article_3,
    invalid_article_4,
    invalid_article_5,
)

PRODUCT_URL = "/api/v1/products"

import asyncio # noqa


pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "article, json_data",
    (
        (valid_article_1, product_1),
        (valid_article_2, product_2),
        (valid_article_3, product_3),
    )
)
async def test_load_product(
    test_client: TestClient,
    article: dict[str, int],
    json_data: dict[str, Any]
):
    response = test_client.post(PRODUCT_URL, json=article)
    article_value = article.get("article")
    assert response.status_code == 200, (
        "Проверьте статус ответа API: при создании / обновлении продукта"
        f"корректный POST-запрос к эндпоинту {PRODUCT_URL} "
        f"с артиклем {article_value} должен вернуть ответ со статусом 200."
    )
    data = response.json()

    for field, value in json_data.items():
        assert field in data, (
            f"Тело корректного POST-запроса к эндпоинту {PRODUCT_URL}"
            f" должно содержать поле {field}."
        )
        if field in ("article", "name"):
            assert value == data[field], (
                f"Тело корректного POST-запроса к эндпоинту {PRODUCT_URL} "
                f"в поле article должно быть равно значению {value}, "
                f"а не {data[field]}."
            )

    data_schema = ProductSchemaDB(**data)

    async with async_session_maker() as session:
        repository: ProductRepository = await get_product_repository(session)
        product = await repository.get_obj_for_field_arg(
            "article",
            arg=article_value,
            many=False
        )
    assert product, (
        f"Корректный POST-запрос к эндпоинту {PRODUCT_URL} "
        f"В базе данных должен создаться продукт с артиклем {article_value}."
    )
    assert data_schema.name == product.name, (
        "Поле name продукта в базе данных не равно полю в ответе."
        f"{product.name} != {data_schema.name}"
    )
    assert data_schema.article == product.article, (
        "Поле article продукта в базе данных не равно полю в ответе."
        f"{product.article} != {data_schema.article}"
    )
    assert data_schema.total == product.total, (
        "Поле total продукта в базе данных не равно полю в ответе."
        f"{product.total} != {data_schema.total}"
    )
    assert data_schema.price == product.price, (
        "Поле price продукта в базе данных не равно полю в ответе."
        f"{product.price} != {data_schema.price}"
    )
    assert data_schema.rating == product.rating, (
        "Поле rating продукта в базе данных не равно полю в ответе."
        f"{product.rating} != {data_schema.rating}"
    )


def test_load_product_empty_data(test_client: TestClient):
    response = test_client.post(PRODUCT_URL, json={})
    assert response.status_code == 422, (
        f"Корректный POST-запрос к эндпоинту {PRODUCT_URL} "
        f"с пустым телом должен вернуть ответ со статусом 422."
    )
    response = test_client.post(PRODUCT_URL)
    assert response.status_code == 422, (
        f"Корректный POST-запрос к эндпоинту {PRODUCT_URL} "
        f"с пустым телом должен вернуть ответ со статусом 422."
    )


@pytest.mark.parametrize(
    "article, status_code",
    (
        (invalid_article_1, 400),
        (invalid_article_2, 400),
        (invalid_article_3, 422),
        (invalid_article_4, 422),
        (invalid_article_5, 422)
    )
)
def test_load_product_invalid_data(
    test_client: TestClient,
    article: int,
    status_code: int
):
    response = test_client.post(PRODUCT_URL, json=article)
    assert response.status_code == status_code, (
        "Проверьте статус ответа API: при создании / обновлении продукта"
        f"корректный POST-запрос к эндпоинту {PRODUCT_URL} "
        f"с артиклем {article} должен вернуть ответ со статусом {status_code}."
    )

from typing import Any

import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from conftest import async_session_maker
from fastapi.testclient import TestClient

from repository import get_product_repository, ProductRepository
from schemas import ProductSchemaDB

from fixtures.products import (
    product_1,
    product_2,
    product_3,
    product_4,
    product_5,

    valid_article_1,
    valid_article_2,
    valid_article_3,
    valid_article_4,
    valid_article_5,

    invalid_article_1,
    invalid_article_2,
    invalid_article_3,
    invalid_article_4,
    invalid_article_5,
)

pytest_plugins = ('pytest_asyncio',)


SUBCRIBE_URL = "/api/v1/subscribe/{}"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "article, json_data",
    (
        (valid_article_1, product_1),
        (valid_article_2, product_2),
        (valid_article_3, product_3),
        (valid_article_4, product_4),
        (valid_article_5, product_5),
    )
)
async def test_start_process_product(
    test_client: TestClient,
    article: dict,
    json_data: dict
):
    article_value = article.get("article")
    response = test_client.get(SUBCRIBE_URL.format(article_value))
    assert response.status_code == 200, (
        "Проверьте статус ответа API: при создании / обновлении продукта"
        f"корректный GET-запрос к эндпоинту {SUBCRIBE_URL} "
        f"с артиклем {article_value} должен вернуть ответ со статусом 200."
    )
    data = response.json()

    for field, value in json_data.items():
        assert field in data, (
            f"Тело корректного GET-запроса к эндпоинту {SUBCRIBE_URL}"
            f" должно содержать поле {field}."
        )
        if field in ("article", "name"):
            assert value == data[field], (
                f"Тело корректного GET-запроса к эндпоинту {SUBCRIBE_URL} "
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
        f"Корректный GET-запрос к эндпоинту {SUBCRIBE_URL} "
        f"В базе данных должен создаться продукт с артиклем {article_value}."
    )
    for key in json_data:
        assert getattr(data_schema, key) == getattr(product, key), (
            f"Поле {key} продукта в базе данных не равно полю в ответе."
            f"{getattr(data_schema, key)} != {getattr(data_schema, key)}"
        )

    assert product.perform_update, (
        "Поле perform_update должно переключится"
        f" на значение true после запроса на эндпоинт {SUBCRIBE_URL}."
    )


@pytest.mark.parametrize(
    "article, status_code",
    (
        (invalid_article_1, 400),
        (invalid_article_2, 400),
        (invalid_article_3, 404),
        (invalid_article_4, 404),
        (invalid_article_5, 404)
    )
)
def test_start_process_product_invalid_params(
    test_client: TestClient,
    article: int,
    status_code: int
):
    article_value = article.get("article")
    url = SUBCRIBE_URL.format(article_value)
    response = test_client.get(url)
    assert response.status_code == status_code, (
        f"Неорректный GET-запрос к эндпоинту {url}"
        f" должен вернуть {status_code} код."
    )


def test_start_process_product_empty_params(test_client):
    response = test_client.get(SUBCRIBE_URL[:-2])
    assert response.status_code == 404, (
        f"Неорректный GET-запрос к эндпоинту {SUBCRIBE_URL[:-2]}"
        " должен вернуть 404 код"
    )

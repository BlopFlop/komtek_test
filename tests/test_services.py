import pytest

from fastapi.exceptions import HTTPException

from services import (
    get_store_url,
    get_data_from_store,
    create_or_update_product_from_store
)
from fixtures.products import (
    product_1,
    product_2,
    product_3,
    invalid_article_1,
    invalid_article_2,
    invalid_article_3,
    invalid_article_4,
    invalid_article_5,
)
from conftest import async_session_maker
from repository import get_product_repository, ProductRepository

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "json_data",
    (
        product_1,
        product_2,
        product_3,
    )
)
async def test_get_data_from_store(json_data: dict):
    url = get_store_url(json_data.get("article"))
    data = await get_data_from_store(url)

    assert isinstance(data, dict), (
        "Функция get_data_from_store должна возвращать словарь."
    )
    assert data.keys() == json_data.keys(), (
        "Все поля должны совпадать с полями запрошенного товара."
    )
    assert all(data.values()), "Результатом должны быть непустые значения."


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "article",
    (
        invalid_article_1,
        invalid_article_2,
        invalid_article_3,
        invalid_article_4,
        invalid_article_5
    )
)
async def test_get_data_from_store_invalid_params(article: dict):
    url = get_store_url(article.get("article"))

    with pytest.raises(HTTPException) as excinfo:
        await get_data_from_store(url)

    assert excinfo, (
        "При попытке получить данные передав неккоректное значение"
        f" должна возникнуть ошибка {HTTPException.__class__}."
    )


@pytest.mark.asyncio
async def test_get_data_from_store_invalid_url():
    invalid_url = (
        "https://pytest-docs-ru.readthedocs.io/pupup/latest"
    )
    url = get_store_url(invalid_url)

    with pytest.raises(HTTPException) as excinfo:
        await get_data_from_store(url)

    assert excinfo, (
        "При попытке получить данные передав неккоректный юрл"
        f" должна возникнуть ошибка {HTTPException.__class__}."
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "json_data",
    (
        product_1,
        product_2,
        product_3,
    )
)
async def test_create_product(json_data):
    article_value = json_data.get("article")
    async with async_session_maker() as session:
        repository: ProductRepository = await get_product_repository(session)
        product = await create_or_update_product_from_store(
            json_data.get("article"),
            repository
        )
        product_db = await repository.get_obj_for_field_arg(
            "article",
            arg=article_value,
            many=False
        )
        for key in json_data:
            assert getattr(product_db, key) == getattr(product, key), (
                f"Поле {key} продукта в базе данных не равно полю в ответе."
                f"{getattr(product_db, key)} != {getattr(product, key)}"
            )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "json_data",
    (
        product_1,
        product_2,
        product_3,
    )
)
async def test_perform_update(json_data):
    article_value = json_data.get("article")
    async with async_session_maker() as session:
        repository: ProductRepository = await get_product_repository(session)
        product = await create_or_update_product_from_store(
            json_data.get("article"),
            repository,
            perform_update=True
        )
        product_db = await repository.get_obj_for_field_arg(
            "article",
            arg=article_value,
            many=False
        )
        for key in json_data:
            assert getattr(product_db, key) == getattr(product, key), (
                f"Поле {key} продукта в базе данных не равно полю в ответе."
                f"{getattr(product_db, key)} != {getattr(product, key)}"
            )
        assert getattr(product_db, "perform_update"), (
            "Поле perform_update должно переключится"
            " на значение true после работы функции."
        )

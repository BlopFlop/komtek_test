from typing import Any

import pytest

from fastapi.testclient import TestClient

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

PRODUCT_URL = "/api/v1/products"


@pytest.mark.parametrize(
    "article, json_data",
    (
        (valid_article_1, product_1),
        (valid_article_2, product_2),
        (valid_article_3, product_3),
        (valid_article_4, product_4),
        (valid_article_5, product_5)
    )
)
def test_load_product(
    test_client: TestClient,
    article: dict[str, int],
    json_data: dict[str, Any]
):
    response = test_client.post(PRODUCT_URL, json=article)
    assert response.status_code == 200, (
        "Проверьте статус ответа API: при создании / обновлении продукта"
        f"корректный POST-запрос к эндпоинту {PRODUCT_URL} "
        f"с артиклем {article} должен вернуть ответ со статусом 200."
    )
    data = response.json()

    for field, value in json_data.items():
        assert field in data, (
            f"Тело корректного POST-запроса к эндпоинту {PRODUCT_URL}"
            f" должно содержать поле {field}."
        )

    # assert article == data["article"], (
    #     f"Тело корректного POST-запроса к эндпоинту {PRODUCT_URL} "
    #     f"в поле article должно быть равно значению {value}, "
    #     # f"а не {data["article"]}."
    # )
    # assert json_data["name"] == data["name"], (
    #     f"Тело корректного POST-запроса к эндпоинту {PRODUCT_URL} "
    #     f"в поле name должно быть равно значению {value}, "
    #     # f"а не {}."
    # )


# def test_load_product_invalid_data(test_client: TestClient):
#     pass


# def test_load_product_empty_data(test_client: TestClient):
#     pass

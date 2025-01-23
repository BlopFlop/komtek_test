from fastapi import APIRouter, Depends

from core.user import current_user
from repository import ProductRepository, get_product_repository
from schemas import ProductSchemaDB, ProductSchemaGetFromStore, Message
from services import create_or_update_product_from_store

router = APIRouter()


@router.post(
    "/",
    dependencies=[Depends(current_user)],
    summary="Загрузка товара в базу данных.",
    description=(
        "Получает товар из магазина по артикулу, и загружает его в базу данных"
    ),
    response_model=ProductSchemaDB,
    responses={
        400: {
            "model": Message(message=("Unautorized."))
        },
        401: {
            "model": Message(message=("Данного артикля не существует."))
        },
        404: {
            "model": Message(message=("Not found error."))
        },
        500: {
            "model": Message(
                message=("Сервис получения товаров по артиклю не доступен.")
            )
        },
    }
)
async def load_product_to_db(
    get_schema_product: ProductSchemaGetFromStore,
    repository_product: ProductRepository = Depends(get_product_repository),
) -> ProductSchemaDB:
    return await create_or_update_product_from_store(
        article=get_schema_product.article, repository=repository_product
    )

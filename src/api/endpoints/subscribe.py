from fastapi import APIRouter, Depends

from core.user import current_user
from repository import ProductRepository, get_product_repository
from schemas import ProductSchemaDB, Message
from services import create_or_update_product_from_store

router = APIRouter()


@router.get(
    "/{article:int}",
    dependencies=[Depends(current_user)],
    summary="Запускает процесс загрузки товара с периодичностю в 30 минут.",
    description=(
        "Получает товар из магазина по артикулу, и "
        "загружает его в базу данных с периодичностю в 30 минут."
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
async def load_product_to_db_polling(
    article: int,
    repository_product: ProductRepository = Depends(get_product_repository),
) -> ProductSchemaDB:
    return await create_or_update_product_from_store(
        article=article, repository=repository_product, perform_update=True
    )

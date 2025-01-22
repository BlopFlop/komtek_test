from fastapi import APIRouter, Depends

from schemas import ProductSchemaDB
from repository import get_product_repository, ProductRepository
from services import create_or_update_product_from_store

router = APIRouter()


@router.get(
    "/{article:int}",
    # dependencies=[Depends(current_user)],
    summary="Запускает процесс загрузки товара с периодичностю в 30 минут.",
    description=(
        "Получает товар из магазина по артикулу, и "
        "загружает его в базу данных с периодичностю в 30 минут."
    ),
    response_model=ProductSchemaDB,
)
async def load_product_to_db_polling(
    article: int,
    repository_product: ProductRepository = Depends(get_product_repository)
) -> ProductSchemaDB:
    return await create_or_update_product_from_store(
        article=article,
        repository=repository_product,
        perform_update=True
    )

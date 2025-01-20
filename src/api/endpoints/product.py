from fastapi import APIRouter, Depends

from schemas import ProductSchemaDB, ProductSchemaGetFromStore
from repository import get_product_repository

router = APIRouter()
# from core.user import current_superuser, current_user


@router.post(
    "/",
    # dependencies=[Depends(current_user)],
    summary="Загрузка товара в базу данных.",
    description=(
        "Получает товар из магазина по артикулу, и загружает его в базу данных"
    ),
    response_model=ProductSchemaDB,
)
async def load_product_to_db(
    product: ProductSchemaGetFromStore,
    repository_product=Depends(get_product_repository)
):
    pass


@router.get(
    "/",
    # dependencies=[Depends(current_user)],
    summary="Запускает процесс загрузки товара с периодичностю в 30 минут.",
    description=(
        "Получает товар из магазина по артикулу, и "
        "загружает его в базу данных с периодичностю в 30 минут."
    )
)
async def load_product_to_db_polling(
    repository_product=Depends()
):
    pass

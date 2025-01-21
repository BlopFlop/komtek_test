from aiogram import Router, F
from aiogram.types import Message

from core.db import get_async_session
from repository import get_product_repository
from services import create_or_update_product_from_store

from core.constants import PRODUCT_MESSAGE

router = Router()


@router.message(F.text)
async def get_product_command(message: Message):
    message_text = message.text.strip()
    if message_text.isdigit():
        article = int(message_text)
        session = await get_async_session().__anext__()
        repository = await get_product_repository(session)
        product = await create_or_update_product_from_store(
            article=article,
            repository_product=repository
        )
        product_message = PRODUCT_MESSAGE.format(
            product.name,
            product.article,
            product.price,
            product.rating,
            product.total
        )
        await message.answer(product_message)

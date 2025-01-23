import logging

from aiogram import F, Router
from aiogram.types import Message
from fastapi.exceptions import HTTPException

from core.db import get_async_session
from repository import get_product_repository
from services import create_or_update_product_from_store
from text.messages import PRODUCT_MESSAGE

router = Router()


@router.message(F.text)
async def get_product_command(message: Message):
    message_text = message.text.strip()
    if message_text.isdigit():
        article = int(message_text)

        logging.info(
            f"Пользователь {message.from_user.id} "
            f"запросил получение товара по артиклю {article}."
        )

        async with await get_async_session().__anext__() as session:
            repository = await get_product_repository(session)

            try:
                product = await create_or_update_product_from_store(
                    article=article, repository=repository
                )
            except HTTPException as ex:
                if 400 <= ex.status_code <= 499:
                    warn_message = (
                        f"Пользователь {message.from_user.id} ввел"
                        f" неккоректный артикль {article}."
                    )
                    logging.warning(warn_message)
                    except_message = (
                        "Вы ввели неккоректный артикль, попробуй еще раз."
                    )
                    await message.answer(except_message)
                elif 500 <= ex.status_code <= 599:
                    error_message = (
                        f"У пользователя {message.from_user.id} нет доступа"
                        f" к функционалу получения товара по артиклю."
                    )
                    logging.error(error_message)
                    except_message = "Сервис временно недоступен."
                    await message.answer(except_message)

            else:
                product_message = PRODUCT_MESSAGE.format(
                    product.name,
                    product.article,
                    product.price,
                    product.rating,
                    product.total,
                )
                logging.info(
                    f"Пользователь {message.from_user.id} "
                    f"получил товар {product}."
                )
                await message.answer(product_message)

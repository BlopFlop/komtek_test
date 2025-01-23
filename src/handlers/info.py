import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from text.messages import HELP_MESSAGE

router = Router()


@router.message(Command("help"))
async def cmd_start(message: Message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /help.")
    await message.answer(HELP_MESSAGE)

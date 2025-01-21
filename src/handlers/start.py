from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from core.constants import START_MESSAGE


router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(START_MESSAGE)

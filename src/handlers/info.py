from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.constants import HELP_MESSAGE


router = Router()


@router.message(Command("help"))
async def cmd_start(message: Message):
    await message.answer(HELP_MESSAGE)

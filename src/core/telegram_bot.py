import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import settings
from handlers import info_router, start_router, product_router


dp = Dispatcher(storage=MemoryStorage())
bot = Bot(
    token=settings.tg_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp.include_router(start_router)
dp.include_router(info_router)
dp.include_router(product_router)

shutdown_event = asyncio.Event()


async def start_bot() -> None:
    await bot.delete_webhook()
    dp.bot = bot
    await dp.start_polling(bot)


async def shutdown_bot():
    await shutdown_event.wait()
    dp.bot.session.close()

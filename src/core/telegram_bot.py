import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import settings
from handlers import info_router, product_router, start_router

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(
    token=settings.tg_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp.include_router(start_router)
dp.include_router(info_router)
dp.include_router(product_router)

shutdown_event = asyncio.Event()


async def start_bot() -> None:
    """Start bot event."""
    await bot.delete_webhook()
    await dp.start_polling(bot)


async def shutdown_bot():
    """Shutdown bot event."""
    await shutdown_event.wait()
    await bot.session.close()

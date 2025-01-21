import asyncio

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from api import router
from core.config import configure_logging, settings
from core.init_db import create_first_superuser
from core.constants import LOG_DIR, LOG_FILE, LOG_FORMAT
from core.telegram_bot import start_bot, shutdown_event, shutdown_bot


async def startup() -> None:
    """Start work FastApi project."""
    await create_first_superuser()


async def lifespan(app: FastAPI):
    """Event handler."""
    # scheduler = AsyncIOScheduler()
    asyncio.create_task(startup())
    bot_task = asyncio.create_task(start_bot())
    yield
    shutdown_event.set()
    await shutdown_bot()
    bot_task.cancel()


configure_logging(log_dir=LOG_DIR, log_file=LOG_FILE, log_format=LOG_FORMAT)

app = FastAPI(title=settings.name_app, lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2000)

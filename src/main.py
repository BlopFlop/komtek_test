import asyncio

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from api import router as api_v1_router
from core.config import settings
from core.constants import LOG_DIR, LOG_FILE, LOG_FORMAT, SECONDS_IN_MINUTE
from core.init_db import create_first_superuser
from core.logging_ import configure_logging
from core.telegram_bot import shutdown_bot, shutdown_event, start_bot
from services.store import perform_update_products_from_store


async def startup() -> None:
    await create_first_superuser()
    await perform_update_products_from_store()


def job() -> None:
    """Work update products after 30 minutes."""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        perform_update_products_from_store,
        "interval",
        seconds=(SECONDS_IN_MINUTE * 30),
    )
    scheduler.start()


async def lifespan(app: FastAPI):
    """Event handler."""
    job()

    asyncio.create_task(startup())
    bot_task = asyncio.create_task(start_bot())

    yield

    shutdown_event.set()
    await shutdown_bot()
    bot_task.cancel()


app = FastAPI(title=settings.name_app, lifespan=lifespan)
app.include_router(api_v1_router, prefix="/api/v1")


if __name__ == "__main__":
    configure_logging(
        log_dir=LOG_DIR, log_file=LOG_FILE, log_format=LOG_FORMAT
    )
    uvicorn.run(app, host="127.0.0.1", port=2000)

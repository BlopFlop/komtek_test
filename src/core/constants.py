from pathlib import Path
from typing import Final

#  base constants
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
ENV_PATH: Final[Path] = BASE_DIR.parent / r"infra//.env"

#  logger constants
LOG_DIR: Final[Path] = BASE_DIR / "logs"
LOG_FILE: Final[Path] = LOG_DIR / "test_project.log"
DATE_FORMAT: Final[str] = "%Y-%m-%d"
LOG_FORMAT: Final[str] = '"%(asctime)s - [%(levelname)s] - %(message)s"'

#  store constants
STORE_URL_GET_PRODUCT: Final[str] = (
    r"https://card.wb.ru/"
    r"cards/v1/detail?appType=1&curr=rub&dest={}&spp=30&nm={}"
)
STORE_KEY_NAME: Final[str] = "name"
STORE_KEY_PRICE: Final[str] = "salePriceU"
STORE_KEY_RATING: Final[str] = "reviewRating"
STORE_KEY_TOTAL: Final[str] = "totalQuantity"


# bot text
START_MESSAGE: Final[str] = (
    "Привет, ты в чат боте, с помощью которого ты можешь получить данные "
    "о товаре из Wildberries, просто введя его Артикул в чат."
)
HELP_MESSAGE: Final[str] = (
    "Ты можешь получить данные о товаре из Wildberries, просто введя"
    " его Артикул в чат, попробуй ввести в чат 211695539."
)
PRODUCT_MESSAGE: Final[str] = (
    "Ваш товар:\n"
    "Название: {}\n"
    "Артикль: {}\n"
    "Цена: {} руб.\n"
    "Рейтинг: {} звезд\n"
    "Количество на складе: {}шт.\n"
)

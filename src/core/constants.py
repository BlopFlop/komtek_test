from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

LOG_DIR: Final[Path] = BASE_DIR / "logs"
LOG_FILE: Final[Path] = LOG_DIR / "bim_web_app_logging.log"
DATE_FORMAT: Final[str] = "%Y-%m-%d"
LOG_FORMAT: Final[str] = '"%(asctime)s - [%(levelname)s] - %(message)s"'

ENV_PATH: Final[Path] = BASE_DIR.parent / r"infra//.env"

STORE_URL_GET_PRODUCT: Final[str] = (
    r"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest={}&spp=30&nm={}"
)

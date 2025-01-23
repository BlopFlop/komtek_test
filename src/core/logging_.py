import logging
from functools import wraps
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Callable


def configure_logging(log_dir: Path, log_file: Path, log_format: str) -> None:
    """Setttings logging from this project."""
    log_dir.mkdir(exist_ok=True)
    rotating_handler: RotatingFileHandler = RotatingFileHandler(
        log_file, encoding="utf-8", maxBytes=10**6, backupCount=5
    )
    rotating_handler.setFormatter(log_format)

    logging.basicConfig(
        format=log_format,
        level=logging.WARNING,
        handlers=(
            rotating_handler,
        ),
    )


def func_log_msg(start_process_msg: str, end_process_msg: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        """Decorator for logging functions."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logging.info(start_process_msg)
            logging.info(f"Переданные аргументы {args} {kwargs}.")
            result = func(*args, **kwargs)
            logging.info(end_process_msg)
            return result

        return wrapper

    return decorator


def async_func_log_msg(
    start_process_msg: str, end_process_msg: str
) -> Callable:
    def decorator(func: Callable) -> Callable:
        """Decorator for logging functions."""

        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            logging.info(start_process_msg)
            logging.info(f"Переданные аргументы {args} {kwargs}.")
            result = await func(*args, **kwargs)
            if result:
                logging.info(
                    f"Функция {func.__name__} вернула значения {result}."
                )
            logging.info(end_process_msg)
            return result

        return wrapper

    return decorator

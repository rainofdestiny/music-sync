import logging
import sys
from logging import Handler, LogRecord

from loguru import logger


class InterceptHandler(Handler):
    def emit(self, record: LogRecord) -> None:
        try:
            level: str | int = logger.level(record.levelname).name
        except Exception:
            level: int | str = record.levelno

        logger.opt(depth=6, exception=record.exc_info).log(
            level, record.getMessage()
        )


class Logger:

    def __init__(self) -> None:
        logging.basicConfig(handlers=[InterceptHandler()], level=0)

        for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
            logging.getLogger(name).handlers = [InterceptHandler()]

        logger.remove()
        self._config()

    @staticmethod
    def _config() -> None:
        logger.add(sys.stdout, level="INFO", format="{level} | {message}")

        logger.add(
            "logs/app.log",
            rotation="10 MB",
            retention="10 days",
            level="DEBUG",
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        )

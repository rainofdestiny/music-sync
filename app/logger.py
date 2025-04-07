import logging
from loguru import logger
import sys


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except Exception:
            level = record.levelno

        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


class Logger:

    def __init__(self) -> None:
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        
        for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
            logging.getLogger(name).handlers = [InterceptHandler()]

        logger.remove()
        self._config()

    def _config(self):
        logger.add(
            sys.stdout,
            level="INFO",
            format="{level} | {message}",
        )

        logger.add(
            "logs/app.log",
            rotation="10 MB",
            retention="10 days",
            level="DEBUG",
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        )

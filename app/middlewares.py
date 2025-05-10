import time

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.perf_counter()
        logger.debug(f"Start processing {request.method} {request.url}")

        response = await call_next(request)

        process_time = (time.perf_counter() - start_time) * 1000

        logger.debug(
            f"Completed {request.method} {request.url} "
            f"with status {response.status_code} in {process_time:.2f}ms"
        )

        response.headers["X-Process-Time"] = str(process_time)
        return response

from fastapi import Request, status
from fastapi.responses import JSONResponse
from httpx import HTTPStatusError, TimeoutException
from loguru import logger


async def http_status_error_handler(
    request: Request, exc: HTTPStatusError
) -> JSONResponse:
    match exc.response.status_code:
        case status.HTTP_400_BAD_REQUEST:
            return await bad_request_400_handler(request, exc)
        case status.HTTP_401_UNAUTHORIZED:
            return await unauthorized_401_handler(request, exc)
        case status.HTTP_404_NOT_FOUND:
            return await not_found_404_handler(request, exc)
        case _:
            logger.error(
                f"HTTP status error {exc.response.status_code}"
                f"in {request.method} {request.url}: {exc}. "
                f"Response body: {exc.response.text}"
            )
            return JSONResponse(
                content={"detail": "Internal Server Error"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


async def bad_request_400_handler(
    request: Request, exc: HTTPStatusError
) -> JSONResponse:
    logger.error(f"Request error in {request.method} {request.url.path}")
    return JSONResponse(
        content={"detail": exc.response.text},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


async def unauthorized_401_handler(
    request: Request, exc: HTTPStatusError
) -> JSONResponse:
    logger.error(
        f"Unauthorized (401) error in {request.method} {request.url} "
        f"Detail's: {exc.response.text}"
    )
    return JSONResponse(
        content={"detail": exc.response.text},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


async def not_found_404_handler(
    request: Request, exc: HTTPStatusError
) -> JSONResponse:
    logger.error(
        f"Not Found (404) error in {request.method} {request.url} "
        f"Detail's: {exc.response.text}"
    )
    return JSONResponse(
        content={"detail": exc.response.text},
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def timeout_exception_handler(
    request: Request, exc: TimeoutException
) -> JSONResponse:
    logger.error(f"Timeout error in {request.method} {request.url.path}")
    return JSONResponse(content="", status_code=status.HTTP_408_REQUEST_TIMEOUT)

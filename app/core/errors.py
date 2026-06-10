import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.services.exceptions import BusinessError, CertificateNotFoundError

logger = logging.getLogger(__name__)


def business_error_status_code(error: BusinessError) -> int:
    if isinstance(error, CertificateNotFoundError):
        return status.HTTP_404_NOT_FOUND

    return status.HTTP_400_BAD_REQUEST


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(BusinessError)
    async def handle_business_error(
        request: Request,
        error: BusinessError,
    ) -> JSONResponse:
        logger.warning(
            "Business error | path=%s | error=%s | message=%s",
            request.url.path,
            error.error_code,
            error.message,
        )

        return JSONResponse(
            status_code=business_error_status_code(error),
            content={
                "error": error.error_code,
                "message": error.message,
            },
        )
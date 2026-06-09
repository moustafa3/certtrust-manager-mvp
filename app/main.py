import logging

from fastapi import FastAPI

from app.api.v1.routes.health import router as health_router
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()
settings = get_settings()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="API for simulated certificate lifecycle management.",
    version=settings.app_version,
)

app.include_router(health_router, prefix="/api/v1")


@app.on_event("startup")
def on_startup() -> None:
    logger.info(
        "Application started | name=%s | version=%s | environment=%s",
        settings.app_name,
        settings.app_version,
        settings.environment,
    )


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": f"{settings.app_name} API",
        "environment": settings.environment,
    }
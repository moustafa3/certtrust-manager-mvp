from fastapi import FastAPI

from app.api.v1.routes.health import router as health_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="API for simulated certificate lifecycle management.",
    version=settings.app_version,
)

app.include_router(health_router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": f"{settings.app_name} API",
        "environment": settings.environment,
    }
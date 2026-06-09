from fastapi import FastAPI

from app.api.v1.routes.health import router as health_router

app = FastAPI(
    title="CertTrust Manager MVP",
    description="API for simulated certificate lifecycle management.",
    version="0.1.0",
)

app.include_router(health_router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "CertTrust Manager MVP API"}

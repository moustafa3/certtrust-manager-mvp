from fastapi import FastAPI

app = FastAPI(
    title="CertTrust Manager MVP",
    description="API for simulated certificate lifecycle management.",
    version="0.1.0",
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "CertTrust Manager MVP API"}
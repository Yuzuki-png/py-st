from fastapi import FastAPI
from mangum import Mangum

from src.routers import ocr

app = FastAPI()

app.include_router(ocr.router)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


handler = Mangum(app)

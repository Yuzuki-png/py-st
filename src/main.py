from fastapi import FastAPI
from mangum import Mangum

from src.routers.ocr import router

app = FastAPI()

app.include_router(router)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


handler = Mangum(app)

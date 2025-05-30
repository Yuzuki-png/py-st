from fastapi import FastAPI
from mangum import Mangum

from .ocr.receipt import process_receipt_ocr
from .routers.receipt_api import ReceiptOCRRequest, ReceiptOCRResponse

app = FastAPI(
    title="レシートOCR API",
    description="プロンプトベースのレシートOCRサービス",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# レシートOCR解析エンドポイント
@app.post(
    "/api/v1/receipt/analyze",
    response_model=ReceiptOCRResponse,
    summary="レシート画像をプロンプト解析",
)
async def analyze_receipt(request: ReceiptOCRRequest) -> ReceiptOCRResponse:
    """
    Base64エンコードされたレシート画像をプロンプトベースで解析して、
    店舗名、日付、金額、カテゴリを抽出します。
    """
    return process_receipt_ocr(image_base64=request.image_base64)


handler = Mangum(app)

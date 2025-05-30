"""
レシートOCR API 型定義
"""

from pydantic import BaseModel, Field


class ReceiptOCRRequest(BaseModel):
    """レシートOCR解析リクエスト"""

    image_base64: str = Field(..., description="Base64エンコードされた画像データ")


class ReceiptData(BaseModel):
    """レシート解析結果データ"""

    店舗名: str | None = Field(None, description="レシート発行元の店名、会社名など")
    店舗住所: str | None = Field(None, description="住所や支店名など（あれば）")
    電話番号: str | None = Field(None, description="電話番号（形式例：03-xxxx-xxxx）")
    日付: str | None = Field(None, description="購入・発行・利用日など（yyyy-MM-dd形式）")
    時刻: str | None = Field(None, description="購入時間（HH:mm形式、任意）")
    合計金額: int | None = Field(None, description="合計金額（円）")
    商品カテゴリ: str | None = Field(None, description="商品・サービスのカテゴリ")


class ReceiptOCRResponse(BaseModel):
    """レシートOCR解析レスポンス"""

    success: bool = Field(..., description="解析成功フラグ")
    receipt_data: ReceiptData | None = Field(None, description="レシート解析結果")
    raw_text: str = Field(..., description="OCR抽出テキスト")
    processing_time: float = Field(..., description="処理時間（秒）")
    timestamp: str = Field(..., description="処理実行時刻")
    engine_used: str = Field(..., description="使用したエンジン")
    confidence: float | None = Field(None, description="処理信頼度")
    error: str | None = Field(None, description="エラーメッセージ")

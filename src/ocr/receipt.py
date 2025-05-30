"""
レシートOCR処理ライブラリ（Tesseract）
"""

import base64
import io
from datetime import datetime

import pytesseract
from PIL import Image

from ..routers.receipt_api import ReceiptData, ReceiptOCRResponse


def analyze_receipt(ocr_text: str) -> ReceiptData:
    """
    OCRテキストからレシート情報を抽出
    """
    lines = [line.strip() for line in ocr_text.split("\n") if line.strip()]

    # 店舗名抽出
    店舗名 = None
    for line in lines[:5]:
        if len(line) > 2 and not line.isdigit():
            店舗名 = line
            break

    # 店舗住所抽出
    店舗住所 = None
    for line in lines:
        if any(keyword in line for keyword in ["市", "区", "町", "県", "都"]):
            店舗住所 = line
            break

    # 電話番号抽出
    電話番号 = None
    for line in lines:
        if "-" in line and any(char.isdigit() for char in line):
            if len(line.replace("-", "").replace(" ", "")) >= 10:
                電話番号 = line
                break

    # 日付抽出
    日付 = None
    for line in lines:
        if "2024" in line or "令和" in line:
            日付 = line
            break

    # 時刻抽出
    時刻 = None
    for line in lines:
        if ":" in line and any(char.isdigit() for char in line):
            if len(line.replace(":", "").replace(" ", "")) <= 6:
                時刻 = line
                break

    # 金額抽出
    合計金額 = None
    for line in lines:
        if "合計" in line or "計" in line:
            numbers = [int(s) for s in line.split() if s.isdigit()]
            if numbers:
                合計金額 = max(numbers)
                break

    # カテゴリ分類
    text_lower = ocr_text.lower()
    if any(keyword in text_lower for keyword in ["薬局", "病院", "医療"]):
        商品カテゴリ = "医療費"
    elif any(keyword in text_lower for keyword in ["スーパー", "コンビニ", "食品"]):
        商品カテゴリ = "食費"
    elif any(keyword in text_lower for keyword in ["電車", "バス", "交通"]):
        商品カテゴリ = "交通費"
    else:
        商品カテゴリ = "その他"

    return ReceiptData(
        店舗名=店舗名,
        店舗住所=店舗住所,
        電話番号=電話番号,
        日付=日付,
        時刻=時刻,
        合計金額=合計金額,
        商品カテゴリ=商品カテゴリ,
    )


def process_receipt_ocr(image_base64: str) -> ReceiptOCRResponse:
    """
    レシートOCR処理メイン関数
    """
    start_time = datetime.now()

    try:
        # Base64デコード
        if image_base64.startswith("data:image"):
            base64_data = image_base64.split(",")[1]
        else:
            base64_data = image_base64

        image_bytes = base64.b64decode(base64_data)
        image = Image.open(io.BytesIO(image_bytes))

        # Tesseract OCR
        ocr_text = pytesseract.image_to_string(image, lang="jpn+eng")

        # レシート解析
        receipt_data = analyze_receipt(ocr_text)

        processing_time = (datetime.now() - start_time).total_seconds()

        return ReceiptOCRResponse(
            success=True,
            receipt_data=receipt_data,
            raw_text=ocr_text,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat(),
            engine_used="tesseract",
            confidence=0.8,
            error=None,
        )

    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        return ReceiptOCRResponse(
            success=False,
            receipt_data=None,
            raw_text=f"エラー: {str(e)}",
            processing_time=processing_time,
            timestamp=datetime.now().isoformat(),
            engine_used="tesseract",
            confidence=None,
            error=str(e),
        )

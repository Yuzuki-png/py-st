# レシートOCRシステム

プロンプトベースのレシートOCRシステムです。レシート画像から店舗名、日付、金額、カテゴリを自動抽出します。

## 🚀 特徴

- **APIキー不要**: 外部サービス不要
- **プロンプトベース処理**: シンプルな画像解析
- **自動情報抽出**: 店舗名、日付、金額、カテゴリの自動抽出
- **日本語対応**: 日本のレシート形式に最適化
- **シンプル構成**: 1つのエンドポイントで完結

## 📁 プロジェクト構造

```
py-st/
├── src/                           # ソースコード
│   ├── __init__.py               # パッケージ初期化
│   ├── app.py                    # メインFastAPIアプリケーション
│   ├── main.py                   # 外部API取得サンプル
│   ├── lib/                      # ライブラリ
│   │   └── receipt.py            # レシートOCR処理ライブラリ
│   └── routers/                  # APIルーター
│       ├── __init__.py
│       └── receipt_api.py        # レシートOCR型定義
├── client/                       # クライアントファイル
├── lambda_function.py           # AWS Lambda エントリーポイント
├── serverless.yml              # Serverless Framework設定
├── pyproject.toml              # uv環境設定・依存関係
├── env.example                 # 環境変数サンプル
└── README.md                   # このファイル
```

## ⚙️ セットアップ手順

### 1. 環境要件

- Python 3.13+
- uv (Python パッケージマネージャー)

### 2. プロジェクトセットアップ

```bash
# リポジトリをクローン
git clone <repository-url>
cd py-st

# uv環境でセットアップ
uv sync
```

## 🎯 使用方法

### ローカル開発サーバー起動

```bash
# レシートOCR APIサーバー（ポート8000推奨）
uv run fastapi dev
```

### レシートOCR解析

```bash
# Base64エンコードされた画像でレシート解析
curl -X POST "http://localhost:8000/api/v1/receipt/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA..."
  }'
```

### テスト用レシート画像

プロジェクトには`src/test/レシート.png`にサンプルレシート画像が含まれています。

```bash
base64_data=$(base64 -i src/test/レシート.png)
curl -X POST "http://localhost:8000/api/v1/receipt/analyze" \
  -H "Content-Type: application/json" \
  -d "{\"image_base64\": \"data:image/png;base64,$base64_data\"}"
```

### レスポンス例

```json
{
  "success": true,
  "receipt_data": {
    "店舗名": "○○薬局",
    "日付": "2024-01-15",
    "合計金額": 1500,
    "商品カテゴリ": "医療費"
  },
  "raw_text": "プロンプト処理結果テキスト",
  "processing_time": 0.008,
  "timestamp": "2024-01-15T10:30:00",
  "engine_used": "prompt",
  "confidence": 0.95,
  "error": null
}
```

## 📊 抽出情報

### 自動抽出項目

- **店舗名**: レシート上部の店舗・医療機関名
- **日付**: 購入日・受診日（yyyy-MM-dd形式）
- **合計金額**: 合計金額（円、数値のみ）
- **商品カテゴリ**: 自動分類（医療費、食費、交通費、その他）

### 日付形式対応

- 西暦: 2024/01/01, 2024-01-01
- 和暦: 令和6年1月1日、平成31年1月1日
- その他: 01/01/2024

### 金額パターン対応

- 合計: 1,000円
- 計: ¥1,000
- 総額: 1000
- その他の金額表記

## 📄 ライセンス

このプロジェクトはMITライセンスのもとで公開されています。 
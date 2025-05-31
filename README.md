# レシートOCRシステム

プロンプトベースのレシートOCRシステムです。レシート画像から店舗名、日付、金額、カテゴリを自動抽出します。

## 特徴

- **APIキー不要**: 外部サービス不要
- **プロンプトベース処理**: シンプルな画像解析
- **自動情報抽出**: 店舗名、日付、金額、カテゴリの自動抽出
- **日本語対応**: 日本のレシート形式に最適化
- **シンプル構成**: 1つのエンドポイントで完結
- **AWS Lambda対応**: サーバーレスデプロイ可能

## プロジェクト構造

```
py-st/
├── src/                           # ソースコード
│   ├── __init__.py               # パッケージ初期化
│   ├── app.py                    # メインFastAPIアプリケーション
│   ├── main.py                   # 外部API取得サンプル
│   ├── requirements.txt          # Lambda用依存関係
│   ├── ocr/                      # OCR処理モジュール
│   │   ├── __init__.py
│   │   └── receipt.py            # レシートOCR処理ライブラリ
│   ├── routers/                  # APIルーター
│   │   ├── __init__.py
│   │   └── receipt_api.py        # レシートOCR型定義
│   └── test/                     # テスト用データ
│       └── レシート.png           # サンプルレシート画像
├── template.yaml               # AWS SAM テンプレート
├── samconfig.toml             # SAM設定ファイル
├── Dockerfile                 # Lambda用Dockerイメージ
├── deploy.sh                  # デプロイスクリプト
├── pyproject.toml            # uv環境設定・依存関係
├── .gitignore                # Git除外設定
└── README.md                 # このファイル
```

## セットアップ手順

### 1. 環境要件

- Python 3.13+
- uv (Python パッケージマネージャー)
- AWS CLI (Lambdaデプロイ用)
- AWS SAM CLI (Lambdaデプロイ用)
- Docker (Lambda用イメージビルド)

### 2. プロジェクトセットアップ

```bash
git clone <repository-url>
cd py-st

uv sync
```

## 使用方法

### ローカル開発サーバー起動

```bash
uv run python -m uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

または

```bash
uv run fastapi dev src/app.py
```

### AWS Lambdaにデプロイ

#### 1. AWS認証設定

```bash
aws configure
```

#### 2. デプロイ実行

```bash
# 開発環境へデプロイ
./deploy.sh dev

# 本番環境へデプロイ
./deploy.sh prod
```

#### 3. 手動デプロイ

```bash
# SAMビルド
sam build

# SAMデプロイ
sam deploy --guided
```

### レシートOCR解析

#### ローカル

```bash
curl -X POST "http://localhost:8000/api/v1/receipt/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA..."
  }'
```

#### AWS Lambda（デプロイ後）

```bash
curl -X POST "https://[API_GATEWAY_URL]/dev/api/v1/receipt/analyze" \
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

## デプロイメント

### AWS Lambda構成

- **Runtime**: Python 3.13 (Container Image)
- **Memory**: 1024MB
- **Timeout**: 30秒
- **OCR Engine**: Tesseract OCR
- **Handler**: Mangum (FastAPI + Lambda)

### API Gateway設定

- **エンドポイント**: RESTful API
- **CORS**: 有効（全オリジン許可）
- **バイナリメディア**: image/*, application/octet-stream
- **認証**: なし（パブリックアクセス）

### 環境変数

- `STAGE`: デプロイ環境 (dev/staging/prod)

## 抽出情報

### 自動抽出項目

- **店舗名**: レシート上部の店舗・医療機関名
- **店舗住所**: 住所や支店名（あれば）
- **電話番号**: 電話番号（形式例：03-xxxx-xxxx）
- **日付**: 購入日・受診日（yyyy-MM-dd形式）
- **時刻**: 購入時間（HH:mm形式、任意）
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
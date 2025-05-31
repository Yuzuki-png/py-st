# レシートOCRシステム

プロンプトベースのレシートOCRシステムです。レシート画像から店舗名、日付、金額、カテゴリを自動抽出します。

## インフラ図
![Image](https://github.com/user-attachments/assets/dd4c8cf7-13c1-4ead-9248-4157d3cebe9d)

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
uv run fastapi dev src/app.py
```

### デプロイ

#### 主要ブランチに push すると、Github CI/CD により自動デプロイが行われる。

- 本番環境 (`prod`)
- ステージング環境 (`staging`)

#### 手動デプロイ

```bash
sam build

sam deploy --guided
```
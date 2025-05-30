STAGE=${1:-dev}
echo "デプロイ環境: $STAGE"

echo "SAM ビルドを実行中"
sam build

echo "AWS Lambdaにデプロイ中"
sam deploy \
  --parameter-overrides \
    Stage=$STAGE \
  --no-confirm-changeset \
  --no-fail-on-empty-changeset

echo "デプロイ完了"
echo ""
echo "スタック情報:"
sam list stack-outputs --stack-name receipt-ocr-api

echo ""
echo "API エンドポイント:"
aws cloudformation describe-stacks \
  --stack-name receipt-ocr-api \
  --query "Stacks[0].Outputs[?OutputKey=='ReceiptOCRApi'].OutputValue" \
  --output text

echo ""
echo "テスト方法:"
echo "curl -X POST [API_URL]/api/v1/receipt/analyze \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"image_base64\":\"[BASE64_IMAGE]\"}'" 
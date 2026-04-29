# Deployment Guide

## Prerequisites

- AWS CLI installed and configured (`aws configure`)
- IAM user with permissions for: Lambda, API Gateway, S3, DynamoDB, Bedrock, IAM
- Python 3.11+
- Boto3 installed

---

## Step 1 — Create S3 Bucket (Knowledge Base)

```bash
aws s3 mb s3://customer-service-bot-kb --region us-west-1
```

Upload FAQ documents:
```bash
aws s3 cp docs/knowledge/ s3://customer-service-bot-kb/ --recursive
```

---

## Step 2 — Create DynamoDB Table

```bash
aws dynamodb create-table \
  --table-name ChatHistory \
  --attribute-definitions \
    AttributeName=session_id,AttributeType=S \
    AttributeName=timestamp,AttributeType=N \
  --key-schema \
    AttributeName=session_id,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region us-west-1
```

---

## Step 3 — Create IAM Role for Lambda

Create `lambda-trust-policy.json`:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "lambda.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }]
}
```

```bash
aws iam create-role \
  --role-name CustomerServiceBotRole \
  --assume-role-policy-document file://lambda-trust-policy.json
```

Attach permissions (Bedrock, S3, DynamoDB, CloudWatch Logs):
```bash
aws iam attach-role-policy --role-name CustomerServiceBotRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

aws iam attach-role-policy --role-name CustomerServiceBotRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

aws iam attach-role-policy --role-name CustomerServiceBotRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

aws iam attach-role-policy --role-name CustomerServiceBotRole \
  --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess
```

---

## Step 4 — Package and Deploy Lambda

```bash
cd src
pip install -r ../requirements.txt -t package/
cp *.py package/
cd package && zip -r ../lambda.zip . && cd ..

aws lambda create-function \
  --function-name CustomerServiceBot \
  --runtime python3.11 \
  --role arn:aws:iam::<ACCOUNT_ID>:role/CustomerServiceBotRole \
  --handler lambda_handler.handler \
  --zip-file fileb://lambda.zip \
  --timeout 30 \
  --region us-west-1 \
  --environment Variables="{S3_BUCKET=customer-service-bot-kb,DYNAMODB_TABLE=ChatHistory}"
```

To update after code changes:
```bash
bash scripts/deploy.sh
```

---

## Step 5 — Create API Gateway

```bash
# Create REST API
aws apigateway create-rest-api --name CustomerServiceBotAPI --region us-west-1

# (Continue setup via console or with additional CLI commands — TBD)
```

---

## Step 6 — Smoke Test

```bash
curl -X POST https://<API_ID>.execute-api.us-west-1.amazonaws.com/prod/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test-001", "message": "What is your return policy?"}'
```

---

## Teardown

```bash
aws lambda delete-function --function-name CustomerServiceBot
aws dynamodb delete-table --table-name ChatHistory
aws s3 rm s3://customer-service-bot-kb --recursive
aws s3 rb s3://customer-service-bot-kb
```

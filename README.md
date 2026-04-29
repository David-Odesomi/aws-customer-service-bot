# AI Customer Service Bot

An AWS-native customer service chatbot for e-commerce/retail. Handles FAQs and maintains conversation history using Amazon Bedrock, S3, DynamoDB, and API Gateway.

---

## Stack

| Layer | Service |
|---|---|
| Interface | CLI |
| Entry point | AWS API Gateway |
| Logic | AWS Lambda (Python) |
| AI model | Amazon Bedrock |
| Knowledge base | Amazon S3 |
| Conversation history | Amazon DynamoDB |

**Deferred (Phase 2):** Cognito (auth), SNS (notifications)

---

## Architecture

See [docs/architecture.md](docs/architecture.md) for the system diagram and service responsibilities.

---

## Getting Started

### Prerequisites
- Python 3.11+
- AWS CLI configured (`aws configure`)
- IAM role with access to Bedrock, S3, DynamoDB, and Lambda

### Install dependencies
```bash
pip install -r requirements.txt
```

### Configure environment
```bash
cp .env.example .env
# Fill in your values
```

### Run locally (CLI)
```bash
python src/cli.py
```

---

## Project Structure

```
ai-customer-service-bot/
├── src/
│   ├── cli.py               # CLI entry point
│   ├── lambda_handler.py    # Lambda function handler
│   ├── bedrock_client.py    # Bedrock API wrapper
│   ├── dynamodb_client.py   # Conversation history CRUD
│   └── s3_client.py         # Knowledge base access
├── tests/
│   ├── test_lambda.py
│   └── test_clients.py
├── scripts/
│   └── deploy.sh            # Lambda deployment script
├── docs/
│   ├── architecture.md
│   ├── requirements.md
│   ├── deployment.md
│   └── changelog.md
├── .env.example
├── requirements.txt
└── README.md
```

---

## Documentation Index

| Doc | Purpose |
|---|---|
| [Architecture](docs/architecture.md) | System design, service roles, data flow |
| [Requirements](docs/requirements.md) | Functional and non-functional requirements |
| [Deployment](docs/deployment.md) | Step-by-step AWS deployment guide |
| [Changelog](docs/changelog.md) | Version history and updates |

---

## Status

- [ ] Architecture finalized
- [ ] Lambda function scaffolded
- [ ] Bedrock integration
- [ ] DynamoDB schema + client
- [ ] S3 knowledge base setup
- [ ] API Gateway configured
- [ ] CLI client built
- [ ] End-to-end test

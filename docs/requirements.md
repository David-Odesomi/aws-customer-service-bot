# Requirements

## Functional Requirements

### F1 — FAQ Handling
- The bot must answer common e-commerce questions (orders, returns, shipping, product info)
- Responses must be grounded in documents stored in the S3 knowledge base
- Unanswerable questions must be gracefully deflected (e.g. "I don't have info on that")

### F2 — Conversation History
- The bot must remember prior messages within a session
- History must persist in DynamoDB keyed by `session_id`
- Lambda must inject the last N turns of history into each Bedrock prompt

### F3 — CLI Interface
- Users interact via a command-line interface
- CLI accepts a message, sends it to API Gateway, and prints the bot's response
- Session ID is generated or passed at runtime

---

## Non-Functional Requirements

### NF1 — Latency
- Response time should be under 5 seconds end-to-end for typical messages
- Lambda timeout: 30 seconds

### NF2 — Cost Efficiency
- Lambda runs only on invocation (serverless — no idle cost)
- DynamoDB on-demand billing
- S3 charged per request and storage

### NF3 — Security
- IAM roles with least-privilege access
- No API keys hardcoded — use environment variables and AWS Secrets Manager
- API Gateway endpoint should be protected (at minimum, API key auth — Cognito in Phase 2)

### NF4 — Maintainability
- Knowledge base (S3) can be updated without redeploying Lambda
- Adding new FAQ documents = upload to S3 bucket (no code change)

---

## Out of Scope (v1)

- Web or mobile frontend
- User authentication (Cognito)
- Push notifications (SNS)
- Analytics dashboard
- Multi-language support

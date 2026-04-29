# Architecture

## Overview

The bot follows a serverless, event-driven pattern. All infrastructure lives in AWS. The CLI sends a user message → API Gateway receives it → Lambda processes it (fetches context from S3, retrieves chat history from DynamoDB, calls Bedrock) → response returns to the CLI.

---

## System Diagram

```
CLI client
    |
    v
API Gateway  (HTTPS entry point)
    |
    v
AWS Lambda   (core request handler)
    |
    |---------> Amazon Bedrock   (AI model — generates response)
    |---------> Amazon S3        (knowledge base — FAQ docs, product info)
    |---------> DynamoDB         (conversation history — per session)
```

---

## Service Responsibilities

### API Gateway
- Exposes a single POST endpoint (`/chat`)
- Passes the full request body to Lambda via proxy integration
- Returns Lambda's response directly to the caller

### AWS Lambda
- Entry point for all chat requests
- Orchestrates the flow: fetch history → fetch context → call Bedrock → save history → return response
- Runtime: Python 3.11

### Amazon Bedrock
- Hosts the foundation model (TBD: Claude / Titan / etc.)
- Receives a constructed prompt (system context + chat history + user message)
- Returns the AI-generated response

### Amazon S3
- Stores FAQ documents, product catalogs, return policies — anything the bot should know
- Lambda fetches relevant docs at runtime to inject as context into the Bedrock prompt

### DynamoDB
- Stores conversation history keyed by `session_id`
- Lambda reads history before each Bedrock call and writes the new exchange after
- Enables multi-turn conversation memory

---

## Data Flow (Single Request)

1. User types a message in the CLI
2. CLI POSTs `{ session_id, message }` to API Gateway
3. Lambda invoked with the request
4. Lambda fetches last N messages from DynamoDB (by `session_id`)
5. Lambda retrieves relevant context from S3 (keyword/semantic match — TBD)
6. Lambda constructs prompt: system prompt + context + history + new message
7. Lambda calls Bedrock with the constructed prompt
8. Bedrock returns a response
9. Lambda saves `{ user_message, bot_response }` to DynamoDB
10. Lambda returns response to API Gateway → CLI displays it

---

## DynamoDB Schema (Draft)

Table: `ChatHistory`

| Attribute | Type | Notes |
|---|---|---|
| `session_id` | String (PK) | Unique per conversation |
| `timestamp` | Number (SK) | Unix epoch, for ordering |
| `role` | String | `user` or `assistant` |
| `content` | String | Message text |

---

## Deferred (Phase 2)

| Service | Purpose |
|---|---|
| AWS Cognito | User authentication and session management |
| AWS SNS | Notifications (escalation alerts, email summaries) |

import json
import dynamodb_client
import s3_client

def lambda_handler(event, context):
    body = event["body"]
    body = json.loads(body)
    session_id = body["session_id"]
    context = s3_client.message
    history = dynamodb_client.get_chat_history(session_id)

    
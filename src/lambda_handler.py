import json

def lambda_handler(event, context):
    body = event["body"]
    body = json.loads(body)
    session_id = body["session_id"]
    message = body["message"]
    history = get_chat_history["session_id"]
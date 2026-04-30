import json
import dynamodb_client
import s3_client
import bedrock_client

def lambda_handler(event, context):
    body = event["body"]
    body = json.loads(body)
    session_id = body["session_id"]
    message = body["message"]
    history = dynamodb_client.get_chat_history(session_id)
    context = s3_client.get_context(message)
    prompt = bedrock_client.generate_response(context, history, message)
    dynamodb_client.save_message(session_id, message, prompt)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': prompt
        })
    }
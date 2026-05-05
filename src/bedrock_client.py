import boto3
import json

bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

def generate_response(context, history, message):
    prompt = (f"You are a customer service assistant. Use the following "
              f"information to answer the question. context: {context} "
              f"history: {history} message: {message}")
    response = bedrock_client.invoke_model(modelId='anthropic.claude-3-sonnet-20240229-v1:0', body=json.dumps({
        'prompt': prompt,
        'max_tokens_to_sample': 500
    }))
    response = response['body'].read().decode('utf-8')
    completion = json.loads(response)
    return completion['completion']
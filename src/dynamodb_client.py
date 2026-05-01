import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ChatHistory')



def get_chat_history(session_id):
    history = table.query(
        KeyConditionExpression=Key('session_id').eq(session_id)
    )

    return history['Items']

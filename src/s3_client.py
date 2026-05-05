import boto3

s3_client = boto3.client('s3', region_name='us-east-1')

def get_context(message):
    context = s3_client.get_object(Bucket ='customer-service-bot-kb', Key='faqs.txt')
    context = context['Body']
    return context.read().decode('utf-8')
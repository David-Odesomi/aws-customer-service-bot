import requests
import uuid

session_id = str(uuid.uuid4())

while True:
    message = input('Enter Your Message: ')
    response = requests.post('https://<API_ID>.execute-api.us-east-1.amazonaws.com/prod',
                             json={'session_id': session_id, 'message': message})
    data = response.json()
    print(data['message'])
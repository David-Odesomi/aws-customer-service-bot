import requests
import uuid

session_id = str(uuid.uuid4())

while True:
    message = input('Enter Your Message: ')
    response = requests.post('https://5luej3khxk.execute-api.us-east-1.amazonaws.com/prod/chat',
                             json={'session_id': session_id, 'message': message})
    data = response.json()
    print(data['message'])
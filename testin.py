import asyncio
import websocket
import json
import requests

def hello():
    url = 'http://localhost:8000/api/token/'
    data = {
        'username': 'admin',
        'password': 'admin'
    }
    response = requests.post(url, data=data)
    access_token = response.json()['access']
    ws = websocket.create_connection('ws://127.0.0.1:8000/ws/chat/1/')
    ws.send(json.dumps({'type': 'authenticate',
                        'token': access_token}))
    while True:
        result = ws.recv()
        print(result)


hello()

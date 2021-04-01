import requests
import socketio
import time

sio = socketio.Client()
sio.connect('http://localhost:8000',namespaces=['/notify'])



@sio.event(namespace='/notify')
def message(data):
    print(data)

while True:
    data = {'name': 'Alice',
            'location': [23, 45],
            'desti': [34, 89]}
    r = requests.post("http://localhost:8000/rider", json={'json_payload': data})
    time.sleep(1)




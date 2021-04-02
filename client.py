import requests
import socketio
import time
import random

sio = socketio.Client()
sio.connect('http://localhost:8000',namespaces=['/notify'])



@sio.event(namespace='/notify')
def message(data):
    print(data)

while True:
    x1 = random.randrange(2000)
    y1 = random.randrange(2000)
    x2 = random.randrange(2000)
    y2 = random.randrange(2000)

    rider_data = {'name': 'Alice',
            'location': [x1,y1],
            'desti': [x2,y2]}
    r = requests.post("http://localhost:8000/rider", json= rider_data)

    x3 = random.randrange(2000)
    y3 = random.randrange(2000)
    carnum = random.randrange(10000000)

    driver_data = {'name': 'Alice',
                  'car_number': carnum,
                  'location': [x3, y3]}
    r = requests.post("http://localhost:8000/driver", json=driver_data)

    time.sleep(1)




import requests
from flask import Flask,request
from flask_apscheduler import APScheduler
import json
import os

location = os.environ.get('LOCATION')

app = Flask(__name__)
scheduler = APScheduler()


riders = []
drivers = []


@app.route('/api/driver', methods=['POST'])
def driver():
    data = request.json
    x = json.loads(data)
    drivers.append(x)
    return data

@app.route('/api/rider', methods=['POST'])
def rider():
    data = request.json
    x = json.loads(data)
    print('recived')
    riders.append(x)
    return data
    


def match_rider_driver():
    mini = 1e10
    for rider in riders:
        driverr = {}
        r1 = rider['location'][0]
        r2 = rider['location'][1]
        r3 = rider['desti'][0]
        r4 = rider['desti'][1]

        for driver in drivers:
            d1 = driver['location'][0]
            d2 = driver['location'][1]

            distance = ((r1 - d1) ** 2 + (r2 - d2) ** 2) ** .5
            if distance < mini:
                driverr = driver

        r_name = rider['name']
        d_name = driverr['name']
        fare = (((r1 - r3) ** 2 + (r2 - r4) ** 2) ** .5) * 2

        messageClient = {
            'riderName': r_name,
            'driverName': d_name,
            'fare': fare
        }
        url = "http://communication."+location+".com:8080/api/clientMessage"
        r = requests.post(f"{url}", json=json.dumps(messageClient))

        drivers.remove(driverr)
        riders.remove(rider)


if __name__ == '__main__':
    scheduler.add_job(id='Schedule task', func=match_rider_driver, trigger = 'interval', seconds = 5)
    scheduler.start()
    app.run(host="0.0.0.0",port=8080)


from flask import Flask,request,g
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO,emit
import sqlite3
import json

app = Flask(__name__)
scheduler = APScheduler()
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

riders = []
drivers = []

def insertVaribleIntoTable(rating):
    conn = sqlite3.connect('./ratings.db')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Preparing SQL queries to INSERT a record into the database.
    cursor.execute('''INSERT INTO ratings(rating) VALUES
       (?)''',str(rating))


    # Commit your changes in the database
    conn.commit()
    print("Records inserted........")

    # Closing the connection
    conn.close()


@app.route('/driver', methods=['POST'])
def driver():
    data = request.json
    x = json.loads(data)
    drivers.append(x)
    #print('received driver data')
    return data

@app.route('/rider', methods=['POST'])
def rider():
    data = request.json
    x = json.loads(data)
    riders.append(x)
    #print('receive rider data')
    return data

@app.route('/rating', methods=['POST'])
def ratings():
    data = request.json
    x = json.loads(data)
    rat = int(x['rating'])
    print(type(rat))
    insertVaribleIntoTable(rat)
    return data

@socketio.on('message' , namespace='/notify')
def handle_message(data):
    print('received fare : ' + str(data) + ' Taka')

@socketio.on('message')
def scheduledJob():
    # sabbir please see this section

    '''print(riders[0]['location'][0])
    print(riders[0]['location'][1])'''

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
                #mini = distance

        #print(driverr)
        r_name = rider['name']
        d_name = driverr['name']
        fare = (((r1 - r3) ** 2 + (r2 - r4) ** 2) ** .5) * 2

        assign = [r_name,d_name,fare]

        socketio.emit('message', assign, namespace='/notify')

        # now change driver's current location to rider's destination
        '''driverr['location'][0] = r3
        driverr['location'][1] = r4'''

        #print(driverr)
        # if you change to remove the driver from drivers list:
        drivers.remove(driverr)
        riders.remove(rider)



if __name__ == '__main__':
    scheduler.add_job(id='Schedule task', func=scheduledJob, trigger = 'interval', seconds = 5)
    scheduler.start()
    #app.run()
    socketio.run(app,port=8000)
from flask import Flask,request
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO,emit

app = Flask(__name__)
scheduler = APScheduler()
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

riders = []
drivers = []
count = 0

@app.route('/driver', methods=['POST'])
def driver():
    data = request.json
    print(data)
    return data

@app.route('/rider', methods=['POST'])
def rider():
    global count
    data = request.json
    riders.append(data)
    count+=1
    print(riders[count-1])
    return data

@app.route('/')
def index():
    return 'hellow jony'

@socketio.on('message')
def scheduledJob():
    print("hello sdk")
    socketio.emit('message',"Hellow Sadek",namespace='/notify')

if __name__ == '__main__':
    scheduler.add_job(id='Schedule task', func=scheduledJob, trigger = 'interval', seconds = 5)
    scheduler.start()
    #app.run()
    socketio.run(app,port=8000)
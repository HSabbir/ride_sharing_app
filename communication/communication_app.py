from flask import Flask,request
from flask_socketio import SocketIO,emit
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('message')
def send_message_client(data):
    assign = [data['riderName'], data['driverName'], data['fare']]
    socketio.emit('message', assign, namespace='/communication')

@app.route('/api/clientMessage', methods=['POST'])
def driver():
    data = request.json
    x = json.loads(data)
    send_message_client(x)
    return data



if __name__ == '__main__':
    socketio.run(app,host="0.0.0.0",port=8080)

import os
from flask import Flask, render_template, session, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
# CORS(app, resources={r"/socket.io/*":{"origins":"*"}})
app.secret_key = "bbbbbbbbbbb6917"
app.debug = True
socketio = SocketIO(app)


@app.before_request
def before_reqest():
    pass

@app.route('/')
def index():
    return render_template('web-socket-client.html');

@socketio.on('connect')
def connect():
    emit("connection", {'data':'Connected', 'username':'test connect'})
    print('connect')

@socketio.on('disconnect')
def disconnect():
    print("Disconnectd")

@socketio.on('request')
def request():
    emit("response", {'data':'request', 'username':'test request'})
    print('request')


if __name__ == '__main__':
    socketio.run(app)
    # app.run()
import socketio
import eventlet.wsgi
from flask import Flask
from dotenv import load_dotenv
from enums.status_enum import StatusEnum
import os

env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path=env_path)

# Create a Socket.IO server
sio = socketio.Server(async_mode='eventlet')

# Create a Flask web application
app = Flask(__name__)

# Attach the Socket.IO server to the web app
app = socketio.WSGIApp(sio, app)

# Handle connection events
@sio.event
def connect(sid, environ, auth):
    print(auth.get('token'))
    print(os.getenv('AUTH_TOKEN'))
    # Assuming you are using 'auth' to authenticate clients
    if auth and auth.get('token') == os.getenv('AUTH_TOKEN'):
        print(f"Authenticated user {sid}")
        sio.emit('status', StatusEnum.SUCCESSFUL_CONNECTION, to=sid)
    else:
        print(f"Authentication failed for {sid}")
        sio.emit('status', StatusEnum.AUTH_FAILED, to=sid)
        sio.disconnect(sid)

@sio.event
def disconnect(sid):
    print(f'disconnect {sid}')

# Handle custom event
@sio.event
def my_event(sid, data):
    print(f"Received event from {sid}: {data}")
    sio.emit('my_event', f"Server received: {data}", to=sid)

if __name__ == '__main__':
    print(os.getenv('SERVER_PORT'))
    # Start the eventlet WSGI server to listen for connections
    eventlet.wsgi.server(eventlet.listen((os.getenv('SERVER_IP'), int(os.getenv('SERVER_PORT')))), app)

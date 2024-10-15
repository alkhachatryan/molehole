import os
import socketio
import eventlet.wsgi
from flask import Flask
from server_inc import EventHandler
from inc.helpers import load_env_file

load_env_file()

# Initialize Socket.IO server and Flask app
sio = socketio.Server(async_mode='eventlet')
app = Flask(__name__)
app = socketio.WSGIApp(sio, app)

# Store active connections
active_connections = {}

# Initialize event handlers
EventHandler(sio, active_connections)

if __name__ == '__main__':
    # Start the eventlet server
    eventlet.wsgi.server(
        eventlet.listen(('0.0.0.0', int(os.getenv('PORT')))), app
    )

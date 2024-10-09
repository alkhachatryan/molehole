import os
import subprocess
import socketio
import eventlet.wsgi
from flask import Flask
from dotenv import load_dotenv
from server_inc import EventHandler  # Import your event handlers class

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path=env_path)

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
        eventlet.listen((os.getenv('SERVER_IP'), int(os.getenv('SERVER_PORT')))), app
    )

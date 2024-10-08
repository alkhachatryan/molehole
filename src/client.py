import socketio
import threading
from dotenv import load_dotenv
import os
from enums.status_enum import StatusEnum

env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path=env_path)
print(os.getenv('AUTH_TOKEN'))
sio = socketio.Client()

# Handle disconnection event
@sio.event
def disconnect():
    print('Disconnected from the server')

@sio.event
def status(data):
    if data == StatusEnum.SUCCESSFUL_CONNECTION:
        command_thread = threading.Thread(target=listen_for_commands)
        command_thread.start()
        print('Successful connection')
    else:
        print(f'Connection failed with status: {data}')

# Handle any incoming event from the server
@sio.event
def my_event(data):
    print(f"Received message from server: {data}")

def listen_for_commands():
    """Wait for user input from the command line and send it to the server."""
    while True:
        command = input("Enter a message (or type 'exit' to quit): ")
        if command.lower() == 'exit':
            sio.disconnect()
            break
        sio.emit('my_event', command)

# Connect to the server with authentication
try:
    sio.connect(f'http://{os.getenv('SERVER_IP')}:{os.getenv('SERVER_PORT')}',
                auth={'token': 'asdf'+os.getenv('AUTH_TOKEN')})
except socketio.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")

# Keep the client running until manually disconnected
sio.wait()

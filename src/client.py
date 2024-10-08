import socketio
import threading
from dotenv import load_dotenv
import os
from enums.status_enum import StatusEnum

env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path=env_path)
sio = socketio.Client()
state = {}

def show_command_input():
    command = input(f'$:{state['current_path']}: ')
    if command.lower() == 'exit':
        sio.disconnect()
        return

    sio.emit('cmd', command)

# Handle disconnection event
@sio.event
def disconnect():
    print('Disconnected from the server')

@sio.event
def status(data):
    global state
    if data['status'] == StatusEnum.SUCCESSFUL_CONNECTION:
        print('Successful connection')
        state = data['state']
        show_command_input()
    else:
        print(f'Connection failed with status: {data}')

@sio.event
def command_output(data):
    global state
    state = data['state']
    print(data['output'])
    show_command_input()


# Connect to the server with authentication
try:
    sio.connect(f'http://{os.getenv('SERVER_IP')}:{os.getenv('SERVER_PORT')}',
                auth={'token': os.getenv('AUTH_TOKEN')})
except socketio.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")

# Keep the client running until manually disconnected
sio.wait()

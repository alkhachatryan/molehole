import socketio
import os
from enums.status_enum import StatusEnum
from inc.helpers import load_env_file

load_env_file()

# Initialize the SocketIO client
sio = socketio.Client()

# Global state for storing the current path and other session data
state = {}


def show_command_input():
    """
    Prompt the user for a command and send it to the server.
    If 'exit' is entered, disconnect the client.
    """
    try:
        command = input(f'$:{state.get("current_path", "")}: ')

        if command.strip().lower() == 'exit':
            print("Exiting the session...")
            sio.disconnect()
            return

        sio.emit('cmd', command)

    except (EOFError, KeyboardInterrupt):
        print("\nSession terminated.")
        sio.disconnect()


# Handle disconnection event
@sio.event
def disconnect():
    """Handle client disconnection."""
    print('Disconnected from the server.')


@sio.event
def status(data):
    """
    Handle status events from the server.
    If connected successfully, update the state and prompt for input.
    """
    global state
    if data['status'] == StatusEnum.SUCCESSFUL_CONNECTION:
        print('Successfully connected to the server.')
        state = data['state']
        show_command_input()
    else:
        print(f'Connection failed with status: {data["status"]}')


@sio.event
def command_output(data):
    """
    Handle the output of commands from the server.
    Update the state and display the output to the user.
    """
    global state
    state = data.get('state', {})
    output = data.get('output', '')

    if output:
        print(output)
    show_command_input()


def connect_to_server():
    """
    Connect to the server using the provided IP, port, and authentication token.
    Handles connection errors gracefully.
    """
    server_ip = os.getenv('SERVER_IP')
    server_port = os.getenv('SERVER_PORT')
    auth_token = os.getenv('AUTH_TOKEN')

    if not server_ip or not server_port or not auth_token:
        print("Server IP, port, or authentication token is missing in the environment variables.")
        return

    try:
        sio.connect(f'http://{server_ip}:{server_port}', auth={'token': auth_token})

    except socketio.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        return


if __name__ == '__main__':
    # Attempt to connect to the server
    connect_to_server()

    # Keep the client running until manually disconnected
    sio.wait()

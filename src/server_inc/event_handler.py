import os
from .connection import Connection
from .command_runner import CommandRunner
from enums.status_enum import StatusEnum


class EventHandler:
    def __init__(self, sio, active_connections):
        self.sio = sio
        self.active_connections = active_connections
        self._command_runner = CommandRunner()

        # Register event handlers
        self.sio.on('connect', self.connect)
        self.sio.on('cmd', self.cmd)
    # todo disconnect
    def connect(self, sid, environ, auth):
        """Handles new connections."""
        if auth and auth.get('token') == os.getenv('AUTH_TOKEN'):
            self.active_connections[sid] = Connection(sid, os.getcwd())
            self.sio.emit('status', {
                'status': StatusEnum.SUCCESSFUL_CONNECTION,
                'state': self.active_connections[sid].state.__dict__,
            }, to=sid)
        else:
            self.sio.emit('status', {'status': StatusEnum.AUTH_FAILED}, to=sid)
            if sid in self.active_connections:
                del self.active_connections[sid]
            self.sio.disconnect(sid)

    def cmd(self, sid, command):
        """Handles command events from clients."""
        connection = self.active_connections[sid]
        if not command:
            self.sio.emit('command_output', {
                'output': '',
                'state': connection.state.__dict__,
            }, to=sid)
            return

        # Run the command using CommandRunner and send the output back to the client
        output = self._command_runner.run_command(connection, command)
        self.sio.emit('command_output', {
            'output': output,
            'state': connection.state.__dict__,
        }, to=sid)

import re
import subprocess

from .connection import Connection


class CommandRunner:
    def __init__(self):
        self._server_executable = CommandRunner.get_server_executable()

    def run_command(self, connection: Connection, command):
        """Executes a command in the current session's context."""
        cd_pattern = r'^cd\s+(.+)$'
        cd_command = re.match(cd_pattern, command)

        if cd_command:
            # Handle 'cd' command to change directories
            return self.change_directory(connection, cd_command.group(1))

        # Validate if the command is interactive
        if CommandRunner.is_interactive_command(command):
            return 'Interactive commands are disallowed.'

        # Run the non-interactive command
        try:
            # Run the command in the current session's directory
            command = f"cd {connection.state.current_path} && {command.strip()}"
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=True,
                executable=self._server_executable
            )
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return str(e)

    def change_directory(self, connection: Connection, new_path):
        """Change the working directory for the given session."""
        new_path = new_path.strip()

        try:
            # Update current path in the connection's state
            result = subprocess.run(
                'pwd',
                capture_output=True,
                text=True,
                shell=True,
                executable=self._server_executable,
                cwd=new_path
            )
            updated_path = result.stdout.strip() or result.stderr.strip()
            connection.state.current_path = updated_path
            return ''
        except Exception as e:
            return str(e)

    @staticmethod
    def is_interactive_command(command):
        """Checks if a command is interactive and disallowed."""
        interactive_commands = [
            "nano", "vim", "vi", "emacs", "gedit", "bash", "sh", "zsh", "fish",
            # Add more interactive commands as needed
        ]
        first_part = command.split()[0] if command else ''
        return any(first_part.startswith(cmd) for cmd in interactive_commands)

    @staticmethod
    def get_server_executable():
        bash_path = subprocess.run(["which", "bash"], capture_output=True, text=True)
        return bash_path.stdout.strip() or '/bin/bash'
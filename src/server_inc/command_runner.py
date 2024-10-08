import re
import subprocess


class CommandRunner:
    def __init__(self, server_executable):
        self._server_executable = server_executable

    def run_command(self, sid, command):
        """Executes a command in the current session's context."""
        cd_pattern = r'^cd\s+(.+)$'
        cd_command = re.match(cd_pattern, command)

        if cd_command:
            # Handle 'cd' command to change directories
            return CommandRunner.change_directory(sid, cd_command.group(1))

        # Validate if the command is interactive
        if CommandRunner.is_interactive_command(command):
            return 'Interactive commands are disallowed.'

        # Run the non-interactive command
        return CommandRunner.execute_command(sid, command)

    def change_directory(self, connection, new_path):
        """Change the working directory for the given session."""

        if connection is None:
            return "Invalid session."

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

    def execute_command(self, connection, command):
        """Executes a non-interactive command in the session's current directory."""
        if connection is None:
            return "Invalid session."

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

    @staticmethod
    def is_interactive_command(command):
        """Checks if a command is interactive and disallowed."""
        interactive_commands = [
            "nano", "vim", "vi", "emacs", "gedit", "bash", "sh", "zsh", "fish",
            # Add more interactive commands as needed
        ]
        first_part = command.split()[0] if command else ''
        return any(first_part.startswith(cmd) for cmd in interactive_commands)
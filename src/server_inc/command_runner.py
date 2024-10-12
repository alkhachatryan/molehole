import os.path
import platform
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

        # Run the non-interactive command
        try:
            # Run the command in the current session's directory
            command = f"cd {connection.state.current_path} && {command.strip()}"

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=True,
                executable=self._server_executable,
                stdin=subprocess.DEVNULL,
            )

            # Check the return code
            if result.returncode != 0:
                return result.stderr.strip()

            return result.stdout if result.stdout else result.stderr.strip()
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
                cwd=os.path.join(connection.state.current_path, new_path)
            )
            updated_path = result.stdout.strip() or result.stderr.strip()
            connection.state.current_path = updated_path
            return ''
        except Exception as e:
            return str(e)

    @staticmethod
    def get_server_executable():
        system_name = platform.system().lower()

        # Check if we're on Linux-based systems
        if system_name == 'linux':
            # Try using 'which' to find bash if available
            try:
                bash_path = subprocess.run(["which", "bash"], capture_output=True, text=True)
                if bash_path.returncode == 0 and bash_path.stdout.strip():
                    return bash_path.stdout.strip()
            except FileNotFoundError:
                # If 'which' is not available, manually look for bash in known locations
                bash_locations = ["/bin/bash", "/usr/bin/bash", "/usr/local/bin/bash"]
                for path in bash_locations:
                    if os.path.exists(path):
                        return path

        # Check if we're on Mac (Darwin) or BSD systems
        elif system_name == 'darwin' or 'bsd' in system_name:
            try:
                bash_path = subprocess.run(["which", "bash"], capture_output=True, text=True)
                if bash_path.returncode == 0 and bash_path.stdout.strip():
                    return bash_path.stdout.strip()
            except FileNotFoundError:
                # For MacOS, common locations for bash
                bash_locations = ["/bin/bash", "/usr/local/bin/bash"]
                for path in bash_locations:
                    if os.path.exists(path):
                        return path

        elif system_name == 'windows':
            bash_path = "C:\\Program Files\\Git\\bin\\bash.exe"
            if os.path.exists(bash_path):
                return bash_path
            else:
                return 'cmd.exe'

        return '/bin/bash'  # Default executable
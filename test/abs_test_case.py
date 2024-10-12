import sys
from abc import ABC, abstractmethod

import pexpect
import pytest
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from inc import helpers

helpers.load_env_file()

class TestLinuxCommands(ABC):
    client = None
    ip = None

    def _connect_to_server(self):
        if not self.client:
            client_command = f"python3 src/client.py --host={self.ip}"
            self.client = pexpect.spawn(client_command)
            # Wait until it connects to the server and prompts for input
            self.client.expect_exact('$:')

    def run_client_command(self, command):
        self._connect_to_server()

        self.client.sendline(command)
        self.client.expect_exact('$:')  # Wait for the next prompt after command execution
        output = self.client.before.decode('utf-8')  # Capture the output before the next prompt
        return self.normalize_output(output)

    def normalize_output(self, output):
        return "\r\n".join(output.splitlines()[1:]).rstrip("\r\n")

    def test_ls_command(self):
        self.run_client_command('cd /app')
        output = self.run_client_command("ls")

        assert "" == output
        self.run_client_command("cd ../")
        output = self.run_client_command("ls")
        assert output.startswith('app\r\n')

    def test_cd_command(self):
        wrong_path = '/this/path/not/exists'
        output = self.run_client_command(f'cd {wrong_path}')
        assert output == f"[Errno 2] No such file or directory: '{wrong_path}'"

        correct_path = '/var/www/html'
        self.run_client_command(f'cd {correct_path}')
        output = self.run_client_command('pwd')
        assert output == correct_path

    def test_mkdir_command(self):
        self.run_client_command('cd /app')
        self.run_client_command('mkdir test_folder')
        output = self.run_client_command(f'ls')
        assert output == 'test_folder'

        output = self.run_client_command('mkdir test_folder')
        assert output.startswith('mkdir: cannot create directory') and output.endswith('File exists')

        self.run_client_command('rm -rf test_folder')

    @abstractmethod
    def test_distro_specific_commands(self):
        pass

if __name__ == '__main__':
    pytest.main()

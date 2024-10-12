import pytest
from .abs_test_case import TestLinuxCommands

class TestFedoraServerBackdoor(TestLinuxCommands):
    ip = "molehole_testing_fedora_server"

    def test_distro_specific_commands(self):
        self.check_for_rpm()

    def check_for_rpm(self):
        output = self.run_client_command('rpm')
        assert output.startswith("RPM version ")


if __name__ == '__main__':
    pytest.main()

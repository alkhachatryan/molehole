import pytest
from .abs_test_case import TestLinuxCommands

class TestUbuntuServerBackdoor(TestLinuxCommands):
    ip = "molehole_testing_debian_server"

    def test_distro_specific_commands(self):
        self.check_for_service()
        self.check_for_dpkg()

    def check_for_service(self):
        output = self.run_client_command('service')
        assert output == 'Usage: service < option > | --status-all | [ service_name [ command | --full-restart ] ]'

    def check_for_dpkg(self):
        output = self.run_client_command('dpkg')
        assert output.startswith('dpkg: error: need an action option')


if __name__ == '__main__':
    pytest.main()

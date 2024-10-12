import pytest
from .abs_test_case import TestLinuxCommands

class TestArchServerBackdoor(TestLinuxCommands):
    ip = "molehole_testing_arch_server"

    def test_distro_specific_commands(self):
        self.check_for_makepkg()

    def check_for_makepkg(self):
        output = self.run_client_command('makepkg')
        assert output.startswith("==> ERROR: Running makepkg as root is not allowed as it can cause permanent,")


if __name__ == '__main__':
    pytest.main()

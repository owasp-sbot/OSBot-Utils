import pytest

from osbot_utils.helpers.ssh.SSH__Execute import SSH__Execute
from osbot_utils.helpers.ssh.SSH__Python import SSH__Python
from osbot_utils.helpers.ssh.TestCase__SSH import TestCase__SSH

class test_SSH__Python(TestCase__SSH):
    ssh_python = SSH__Python

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ssh_python = cls.ssh.ssh_python()

    def test_setUpClass(self):
        assert type(self.ssh_python            ) is SSH__Python
        assert type(self.ssh_python.ssh_execute) is SSH__Execute


    def test_execute_python__code(self):
        with self.ssh_python as _:
            assert _.execute_python__code('print(40+2)').get('stdout') == '42\n'

    def test__execute_python__code__return_stdout(self):
        multi_line_command = """
import sys
print(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
"""
        with self.ssh_python as _:
            assert _.execute_python__code__return_stdout(multi_line_command) == '3 12 2'

    def test_execute_python__function(self):
        def an_function():
            return 'Hello from the SSH instance!'

        with self.ssh_python as _:
            assert _.execute_python__function(an_function).get('stdout') == 'Hello from the SSH instance!\n'


    def test_execute_python__function__return_stdout(self):

        def test_osbot_utils():
            from osbot_utils.utils.Misc import str_to_base64
            an_value = 'this will be base64 encoded!'
            return str_to_base64(an_value)

        # todo: this one needs osbot_utils installed
        # with self.ssh_python as _:
        #     function_return_value = _.execute_python__function__return_stderr(test_osbot_utils)
        #     pprint(function_return_value)
        #     #assert base64_to_str(function_return_value) == 'this will be base64 encoded!'

    @pytest.mark.skip("needs check to see if it already installed")
    def test_install_python3(self):
        with self.ssh_python as _:
            result = _.install_python3()
            assert 'libpython3' in result.get('stdout')


    def test_pip_install(self):
        with self.ssh_python as _:
            result = _.pip_install('osbot-utils')
            assert 'osbot-utils' in result

    def test_pip_version(self):
        with self.ssh_python as _:
            result = _.pip_version()
            assert result.startswith('pip 24.0')

    def test_python_version(self):
        with self.ssh_python as _:
            result = _.python_version()
            assert result == 'Python 3.12.2'

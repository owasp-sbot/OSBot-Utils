import pytest
from osbot_utils.helpers.ssh.SSH__Execute           import ENV_VAR__SSH__HOST, ENV_VAR__SSH__KEY_FILE, ENV_VAR__SSH__USER, ENV_VAR__SSH__PORT, ENV_VAR__SSH__STRICT_HOST_CHECK
from osbot_utils.helpers.ssh.SSH__Health_Check      import SSH__Health_Check
from osbot_utils.helpers.ssh.TestCase__SSH          import TestCase__SSH
from osbot_utils.utils.Env                          import get_env


class test_SSH__Health_Check(TestCase__SSH):

    def setUp(self):
        self.ssh_health_check = SSH__Health_Check().setup()

    @pytest.mark.skip("need to handle case when this is executed in GH")
    def test_update_server_ssh_host_fingerprint(self):
        with self.ssh_health_check as _:
            result = _.update_server_ssh_host_fingerprint()
            assert result.get('status') == 'ok'

    def test_check_connection(self):
        with self.ssh_health_check as _:
            result = _.check_connection()
            assert result.get('status') == 'ok'

    def test_env_vars_names(self):
        with self.ssh_health_check as _:
            assert _.env_vars_names() == ['ssh_host' ,'ssh_key_file', 'ssh_key_user', 'ssh_port', 'strict_host_check']

    def test_env_vars_values(self):
        with self.ssh_health_check as _:
            expected_values = { 'ssh_host'         : get_env(ENV_VAR__SSH__HOST             ),
                                'ssh_key_file'     : get_env(ENV_VAR__SSH__KEY_FILE         ),
                                'ssh_key_user'     : get_env(ENV_VAR__SSH__USER             ),
                                'ssh_port'         : get_env(ENV_VAR__SSH__PORT             ),
                                'strict_host_check': get_env(ENV_VAR__SSH__STRICT_HOST_CHECK)}
            assert _.env_vars_values() == expected_values

    def test_env_vars_set_ok(self):
        with self.ssh_health_check as _:
            assert _.env_vars_set_ok() is True


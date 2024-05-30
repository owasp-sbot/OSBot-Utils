from unittest import TestCase

import pytest

from osbot_utils.helpers.ssh.SSH__Health_Check import SSH__Health_Check
from osbot_utils.helpers.ssh.TestCase__SSH import TestCase__SSH
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env import get_env


class test_SSH__Health_Check(TestCase__SSH):

    def setUp(self):
        self.ssh_health_check = SSH__Health_Check().setup()

    def test_check_connection(self):
        with self.ssh_health_check as _:
            result = _.check_connection()
            pprint(result)

    def test_env_vars_names(self):
        with self.ssh_health_check as _:
            assert _.env_vars_names() == ['ssh_host', 'ssh_key_file', 'ssh_key_user', 'strict_host_check']

    def test_env_vars_values(self):
        with self.ssh_health_check as _:
            expected_values = { 'ssh_host'         : get_env('SSH__HOST'             ),
                                'ssh_key_file'     : get_env('SSH__KEY_FILE__FILE'   ),
                                'ssh_key_user'     : get_env('SSH__KEY_FILE__USER'   ),
                                'strict_host_check': get_env('SSH__STRICT_HOST_CHECK')}
            assert _.env_vars_values() == expected_values

    def test_env_vars_set_ok(self):
        with self.ssh_health_check as _:
            assert _.env_vars_set_ok() is True


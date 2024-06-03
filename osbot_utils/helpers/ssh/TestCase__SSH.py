from unittest import TestCase

import pytest

import osbot_utils
from osbot_utils.helpers.ssh.SSH                    import SSH
from osbot_utils.helpers.ssh.SSH__Cache__Requests   import SSH__Cache__Requests
from osbot_utils.helpers.ssh.SSH__Execute import SSH__Execute
from osbot_utils.utils.Env                          import load_dotenv
from osbot_utils.utils.Files                        import path_combine

ENV_FILE__WITH_ENV_VARS           = "../.ssh.env"

class TestCase__SSH(TestCase):
    ssh : SSH

    @classmethod
    def setUpClass(cls):
        cls.load_dotenv()
        cls.ssh = SSH().setup()
        if not cls.ssh.ssh_execute().ssh_host:
            pytest.skip("SSH host not set")

        cls.cache = SSH__Cache__Requests()
        cls.cache.patch_apply()

    @classmethod
    def tearDownClass(cls):
        cls.cache.patch_restore()
        assert SSH__Execute.execute_command.__qualname__ == 'SSH__Execute.execute_command'

    @staticmethod
    def load_dotenv():
        env_file_path = path_combine(osbot_utils.path, ENV_FILE__WITH_ENV_VARS)
        load_dotenv(dotenv_path=env_file_path)
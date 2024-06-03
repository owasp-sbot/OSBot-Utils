import pytest

from osbot_utils.helpers.ssh.SSH__Execute import SSH__Execute
from osbot_utils.helpers.ssh.TestCase__SSH  import TestCase__SSH
from osbot_utils.utils.Dev                  import pprint
from osbot_utils.utils.Env                  import in_github_action
from osbot_utils.utils.Misc                 import list_set

ENV_VAR_TEST_OSBOT__SSH_HOST      = 'SSH__HOST'
ENV_VAR_TEST_OSBOT__SSH_KEY_FILE  = 'SSH__KEY_FILE__FILE'
ENV_VAR_TEST_OSBOT__SSH_KEY_USER  = 'SSH__KEY_FILE__USER'

ENV_FILE__WITH_ENV_VARS           = "../../../.ssh.env"

class test_SSH(TestCase__SSH):
    #ssh           : SSH
    #ssh_host       : str
    #ssh_key_file  : str
    #ssh_key_user  : str

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_ssh_execute(self):
        assert type(self.ssh.ssh_execute()) is SSH__Execute



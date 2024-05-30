import pytest

from osbot_utils.helpers.ssh.SSH__Linux import SSH__Linux
from osbot_utils.helpers.ssh.TestCase__SSH import TestCase__SSH
from osbot_utils.utils.Dev import pprint

class test__SSH_Linux(TestCase__SSH):

    def setUp(self):
        self.ssh_linux = SSH__Linux(ssh=self.ssh)
        if self.ssh_linux.ssh.ssh_not__setup_ok():
            self.skipTest('ssh is not setup or enabled')


    def test_echo(self):
        #self.cache.cache_table__clear()
        with self.ssh_linux as _:
            assert _.echo('hello world') == 'hello world'

        #pprint(self.cache.cache_entries())
        pprint(self.cache.requests_data__all())


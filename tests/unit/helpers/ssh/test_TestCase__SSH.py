from osbot_utils.helpers.ssh.SSH import SSH
from osbot_utils.helpers.ssh.SSH__Cache__Requests import SSH__Cache__Requests
from osbot_utils.helpers.ssh.SSH__Execute import SSH__Execute
from osbot_utils.helpers.ssh.TestCase__SSH import TestCase__SSH


qualname__original = 'SSH__Execute.execute_command'
qualname__patched  = 'Sqlite__Cache__Requests__Patch.patch_apply.<locals>.proxy'

class test_TestCase__SSH(TestCase__SSH):

    @classmethod
    def setUpClass(cls):
        assert SSH__Execute.execute_command.__qualname__ == qualname__original
        super().setUpClass()
        assert SSH__Execute.execute_command.__qualname__ == qualname__patched

    @classmethod
    def tearDownClass(cls):
        assert SSH__Execute.execute_command.__qualname__ == qualname__patched
        super().tearDownClass()
        assert SSH__Execute.execute_command.__qualname__ == qualname__original

    def test_setUpClass(self):
        assert type(self.cache) is SSH__Cache__Requests
        assert SSH__Execute.execute_command.__qualname__ == qualname__patched

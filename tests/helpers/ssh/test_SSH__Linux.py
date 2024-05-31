import pytest

from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.helpers.ssh.SSH__Linux import SSH__Linux
from osbot_utils.helpers.ssh.TestCase__SSH import TestCase__SSH
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set


class test__SSH_Linux(TestCase__SSH):

    def setUp(self):
        self.ssh_linux = SSH__Linux(ssh=self.ssh)
        if self.ssh_linux.ssh.ssh_not__setup_ok():
            self.skipTest('ssh is not setup or enabled')

    def test_disk_space(self):
        disk_space = self.ssh_linux.disk_space(index_by='Mounted_on')
        assert '/dev' in list_set(disk_space)
        for _, disk_details in disk_space.items():
            assert list_set(disk_details) == ['Avail', 'Filesystem', 'Mounted_on', 'Size', 'Use%', 'Used']

    def test_cat(self):
        with self.ssh_linux as _:
            assert 'root:*:' in _.cat('/etc/shadow')

    def test_echo(self):
        with self.ssh_linux as _:
            assert "hello world" in _.echo('hello world')


    def test_find(self):
        expected_systemd = '/usr/lib/systemd/user/paths.target'
        systemd_path = '/usr/lib/systemd/user'
        with self.ssh_linux as _:
            results = _.find(systemd_path)
            assert len(results) > 10
            assert expected_systemd in results

    def test_ls(self):
        with self.ssh_linux as _:
            ls_on_root =  _.ls('/')
            assert 'bin'   in ls_on_root
            assert 'media' in ls_on_root

    @pytest.mark.skip("was failing in GH Actions")
    def test_mkdir(self):
        #self.cache.disable()               # todo add support for cache caching based on source code
        folder_name = './an_folder_3'
        with self.ssh_linux as _:
            _.mkdir(folder_name)
            assert _.dir_exists(folder_name) is True
            _.rmdir(folder_name)
            assert _.dir_exists(folder_name) is False




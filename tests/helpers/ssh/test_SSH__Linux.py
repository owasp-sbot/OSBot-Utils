import pytest

from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.helpers.ssh.SSH__Linux import SSH__Linux
from osbot_utils.helpers.ssh.TestCase__SSH import TestCase__SSH
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env import in_github_action
from osbot_utils.utils.Misc import list_set


class test__SSH_Linux(TestCase__SSH):

    def setUp(self):
        self.ssh_linux = self.ssh.ssh_linux()
        if self.ssh_linux.ssh_execute.ssh_not__setup_ok():
            self.skipTest('ssh is not setup or enabled')

    def test_apt_update(self):
        with self.ssh_linux as _:
            assert 'Hit:1' in  _.apt_update()

    def test_apt_install(self):
        with self.ssh_linux as _:
            _.apt_install('curl')           # todo add assert

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

    def test_memory_usage(self):
        memory_usage = self.ssh_linux.memory_usage()
        assert 'Mem:' in memory_usage[1]


    @pytest.mark.skip("needs refactoring to make it more solid (like taking into account if folders already exist)")
    def test_mkdir(self):
        if in_github_action():
            return                                  # todo: figure out why this is failing in GH actions
        folder_name = './an_folder_3' ;
        with self.ssh_linux as _:
            _.mkdir(folder_name)
            assert _.dir_exists(folder_name) is True
            _.rmdir(folder_name)
            assert _.dir_exists(folder_name) is False


    def test_running_processes(self):
        result = self.ssh_linux.running_processes(index_by='COMMAND')
        #assert '/usr/lib/systemd/systemd' in list_set(result) # in docker container we get a different list: '/usr/bin/ps'
        for _, process_data in result.items():
            assert list_set(process_data) == ['%CPU', '%MEM', 'COMMAND', 'PID' , 'RSS', 'START',
                                              'STAT', 'TIME', 'TTY'    , 'USER', 'VSZ'         ]

    def test_system_uptime(self):
        uptime = self.ssh_linux.system_uptime()
        assert 'up' in uptime

    def test_uname(self):
        assert self.ssh_linux.uname() == 'Linux'

    def test_which(self):
        assert self.ssh_linux.which('bash')  == '/usr/bin/bash'


    @pytest.mark.skip(reason="just PoC (which worked great:) ")
    def test__workflow__install_python(self):
        command ='sudo yum install python3-pip -y'
        result = self.ssh.execute_command__return_stdout(command)
        assert 'Complete!' in result

        command = 'pip3 install Flask'
        result = self.ssh.execute_command__return_stdout(command)
        pprint('Flask' in result)

        command = 'python3 -m flask --version'
        result = self.ssh.execute_command__return_stdout(command)
        assert result == 'Python 3.9.16\nFlask 3.0.3\nWerkzeug 3.0.3'




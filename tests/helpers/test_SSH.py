import pytest
from os                         import environ
from unittest                   import TestCase
from dotenv                     import load_dotenv
from osbot_utils.helpers.SSH    import SSH
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_name
from osbot_utils.utils.Misc import list_set

ENV_VAR_TEST_OSBOT__SSH_HOST      = 'TEST_OSBOT__SSH_HOST'
ENV_VAR_TEST_OSBOT__SSH_KEY_FILE  = 'TEST_OSBOT__SSH_KEY_FILE'
ENV_VAR_TEST_OSBOT__SSH_KEY_USER  = 'TEST_OSBOT__SSH_KEY_USER'

class test_SSH(TestCase):
    ssh      : SSH
    ssh_host       : str
    ssh_key_file  : str
    ssh_key_user  : str

    @classmethod
    def setUpClass(cls):
        #load_dotenv(dotenv_path='../../.local.env',override=True)       # todo: find a better solution for this use of ../../.local.env
        cls.ssh_host     = environ.get(ENV_VAR_TEST_OSBOT__SSH_HOST    )
        cls.ssh_key_file = environ.get(ENV_VAR_TEST_OSBOT__SSH_KEY_FILE)
        cls.ssh_key_user = environ.get(ENV_VAR_TEST_OSBOT__SSH_KEY_USER)
        if not cls.ssh_host:
            pytest.skip("SSH host not set")
        cls.ssh = SSH(ssh_host=cls.ssh_host, ssh_key_file=cls.ssh_key_file, ssh_key_user=cls.ssh_key_user)

    def test__init__(self):
        with self.ssh as _:
            assert _.__locals__() == {'ssh_host'          : self.ssh_host     ,
                                      'ssh_key_file'      : self.ssh_key_file ,
                                      'ssh_key_user'      : self.ssh_key_user ,
                                      'strict_host_check' : False             }

    def test_execute_command(self):
        assert self.ssh.execute_command(None) == { 'data' : None, 'message': '', 'status': 'error' ,
                                                   'error': 'in execute_command not all required vars were setup'}
        command = 'uname'
        ssh_args = self.ssh.execute_command_args(command)
        result   = self.ssh.execute_command(command)
        assert result == { 'cwd'      : '.'                   ,
                           'duration' : result.get('duration'),
                           'error'    : None                  ,
                           'kwargs'   : {'cwd': '.', 'stderr': -1, 'stdout': -1, 'timeout': None},
                           'runParams': ['ssh'] + ssh_args    ,
                           'status'   : 'ok'                  ,
                           'stderr'   : ''                    ,
                           'stdout'   : 'Linux\n'             }

    def test_execute_command_args(self):
        command = 'an_linux_command'
        ssh_args  = self .ssh.execute_command_args(command=command)
        assert ssh_args == [ '-o'                                  ,
                             'StrictHostKeyChecking=no'            ,
                             '-i'                                  ,
                             self.ssh_key_file                     ,
                             f'{self.ssh_key_user}@{self.ssh_host}',
                             command                               ]

    # helpers for common linux methods

    def test_disk_space(self):
        disk_space = self.ssh.disk_space(index_by='Mounted_on')
        assert list_set(disk_space) == ['/', '/boot/efi', '/dev', '/dev/shm', '/run', '/run/user/1000', '/tmp']
        for _, disk_details in disk_space.items():
            assert list_set(disk_details) == ['Avail', 'Filesystem', 'Mounted_on', 'Size', 'Use%', 'Used']

    def test_ls(self):
        ls_on_root =  self.ssh.ls('/')
        assert 'bin'   in ls_on_root
        assert 'media' in ls_on_root

    def test_memory_usage(self):
        memory_usage = self.ssh.memory_usage()
        assert 'Mem:' in memory_usage[1]


    def test_running_processes(self):
        result = self.ssh.running_processes(index_by='COMMAND')
        assert '/usr/lib/systemd/systemd' in list_set(result)
        for _, process_data in result.items():
            assert list_set(process_data) == ['%CPU', '%MEM', 'COMMAND', 'PID' , 'RSS', 'START',
                                              'STAT', 'TIME', 'TTY'    , 'USER', 'VSZ'         ]
            break

    def test_system_uptime(self):
        uptime = self.ssh.system_uptime()
        assert 'up' in uptime


    def test_uname(self):
        assert self.ssh.uname() == 'Linux'

    def test_which(self):
        assert self.ssh.which('bash')  == '/usr/bin/bash'


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



import pytest
from os                           import environ
from unittest                     import TestCase
from osbot_utils.helpers.ssh.SSH  import SSH
from osbot_utils.helpers.ssh.TestCase__SSH import TestCase__SSH
from osbot_utils.utils.Dev        import pprint
from osbot_utils.utils.Env import load_dotenv
from osbot_utils.utils.Misc       import list_set

ENV_VAR_TEST_OSBOT__SSH_HOST      = 'SSH__HOST'
ENV_VAR_TEST_OSBOT__SSH_KEY_FILE  = 'SSH__KEY_FILE__FILE'
ENV_VAR_TEST_OSBOT__SSH_KEY_USER  = 'SSH__KEY_FILE__USER'

ENV_FILE__WITH_ENV_VARS           = "../../../.ssh.env"

class test_SSH(TestCase__SSH):
    #ssh      : SSH
    #ssh_host       : str
    #ssh_key_file  : str
    #ssh_key_user  : str

    @classmethod
    def setUpClass(cls):
        super().setUpClass()


    def test__init__(self):
        with self.ssh as _:
            assert _.__locals__() == {'ssh_host'          : self.ssh.ssh_host     ,
                                      'ssh_key_file'      : self.ssh.ssh_key_file ,
                                      'ssh_key_user'      : self.ssh.ssh_key_user ,
                                      'ssh_port'          : self.ssh.ssh_port     ,
                                      'strict_host_check' : False                 }

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
        assert ssh_args == [ '-p'                                          ,
                             '22222'                                       ,
                             '-o'                                          ,
                             'StrictHostKeyChecking=no'                    ,
                             '-i'                                          ,
                             self.ssh.ssh_key_file                         ,
                             f'{self.ssh.ssh_key_user}@{self.ssh.ssh_host}',
                             command                                       ]

    # helpers for common linux methods

    def test_disk_space(self):
        disk_space = self.ssh.disk_space(index_by='Mounted_on')
        assert '/dev' in list_set(disk_space)
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
        #assert '/usr/lib/systemd/systemd' in list_set(result) # in docker container we get a different list: '/usr/bin/ps'
        for _, process_data in result.items():
            assert list_set(process_data) == ['%CPU', '%MEM', 'COMMAND', 'PID' , 'RSS', 'START',
                                              'STAT', 'TIME', 'TTY'    , 'USER', 'VSZ'         ]

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



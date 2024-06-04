from osbot_utils.helpers.ssh.SSH__Execute import SSH__Execute
from osbot_utils.helpers.ssh.TestCase__SSH import TestCase__SSH
from osbot_utils.utils.Env import in_github_action


class test_SSH(TestCase__SSH):
    #ssh           : SSH
    #ssh_host       : str
    #ssh_key_file  : str
    #ssh_key_user  : str
    ssh_execute   : SSH__Execute

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ssh_execute = cls.ssh.ssh_execute()

    def test__init__(self):
        with self.ssh_execute as _:
            assert _.__locals__() == {'print_after_exec'  : False                         ,
                                      'ssh_host'          : self.ssh_execute.ssh_host     ,
                                      'ssh_key_file'      : self.ssh_execute.ssh_key_file ,
                                      'ssh_key_user'      : self.ssh_execute.ssh_key_user ,
                                      'ssh_port'          : self.ssh_execute.ssh_port     ,
                                      'strict_host_check' : False                         }

    def test_execute_command(self):
        # result_ssh_host_remove = self.ssh.remove_server_ssh_host_fingerprint()          # todo: find a to handle the case when the
        # pprint(result_ssh_host_remove)                                                  #       /home/runner/.ssh/known_hosts doesn't exist or has changed

        assert self.ssh_execute.execute_command(None) == { 'data' : None, 'message': '', 'status': 'error' ,
                                                   'error': 'in execute_command not all required vars were setup'}
        command = 'uname'
        ssh_args = self.ssh_execute.execute_command_args(command)
        result   = self.ssh_execute.execute_command(command)
        if in_github_action():
            stderr   =  "Warning: Permanently added '[localhost]:22222' (ED25519) to the list of known hosts.\r\n"
        else:
            stderr   = ''
        assert result == { 'cwd'      : '.'                   ,
                           'duration' : result.get('duration'),
                           'error'    : None                  ,
                           'kwargs'   : {'cwd': '.', 'stderr': -1, 'stdout': -1, 'timeout': None},
                           'runParams': ['ssh'] + ssh_args    ,
                           'status'   : 'ok'                  ,
                           'stderr'   : stderr                ,
                           'stdout'   : 'Linux\n'             }

    def test_execute_command_args(self):
        command   = 'an_linux_command'
        ssh_args  = self .ssh_execute.execute_command_args(command=command)
        assert ssh_args == [ '-p'                                                          ,
                             '22222'                                                       ,
                             '-o'                                                          ,
                             'StrictHostKeyChecking=no'                                    ,
                             '-i'                                                          ,
                             self.ssh_execute.ssh_key_file                                 ,
                             f'{self.ssh_execute.ssh_key_user}@{self.ssh_execute.ssh_host}',
                             command                                                       ]


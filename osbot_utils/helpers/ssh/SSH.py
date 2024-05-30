from decimal import Decimal

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.context_managers.capture_duration import capture_duration
from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env import get_env
from osbot_utils.utils.Functions import function_source_code
from osbot_utils.utils.Misc import timestamp_utc_now, str_to_bool, str_to_int
from osbot_utils.utils.Process import start_process
from osbot_utils.utils.Status import status_error

ENV_VAR__SSH__HOST              = 'SSH__HOST'
ENV_VAR__SSH__PORT              = 'SSH__PORT'
ENV_VAR__SSH__KEY_FILE          = 'SSH__KEY_FILE'
ENV_VAR__SSH__USER              = 'SSH__USER'
ENV_VAR__SSH__STRICT_HOST_CHECK = 'SSH__STRICT_HOST_CHECK'

class SSH(Kwargs_To_Self):
    ssh_host          : str
    ssh_port          : int  = 22
    ssh_key_file      : str
    ssh_key_user      : str
    strict_host_check : bool = False

    # setup commands             # todo refactor into separate class
    def setup(self):
        self.setup_using_env_vars()
        return self

    def setup_using_env_vars(self):         # move this to a CONFIG class (see code in SSH__Health_Check)
        ssh_host              = get_env(ENV_VAR__SSH__HOST               )
        ssh_port              = get_env(ENV_VAR__SSH__PORT              )
        ssh_key_file          = get_env(ENV_VAR__SSH__KEY_FILE          )
        ssh_key_user          = get_env(ENV_VAR__SSH__USER              )
        ssh_strict_host_check = get_env(ENV_VAR__SSH__STRICT_HOST_CHECK )
        if ssh_host:
            self.ssh_host = ssh_host
        if ssh_port:
            self.ssh_port = str_to_int(ssh_port)
        if ssh_key_file:
            self.ssh_key_file = ssh_key_file
        if ssh_key_user:
            self.ssh_key_user = ssh_key_user
        if ssh_strict_host_check is not None:
            self.strict_host_check = str_to_bool(ssh_strict_host_check)

    def ssh_setup_ok(self):
        # todo: add check to see if ssh executable exists (this check can be cached)
        if self.ssh_host and self.ssh_key_file and self.ssh_key_user:
            return True
        return False

    def ssh_not__setup_ok(self):
        return self.ssh_setup_ok() is False

    # execution & other commands # todo refactor into separate class
    def exec(self, command):
        return self.execute_command__return_stdout(command)

    def exec__print(self, command):
        result = self.execute_command__return_stdout(command)
        self.print_header_for_command(command)
        print(result)
        return result

    def execute_command(self, command):
        if self.ssh_setup_ok()  and command:
            ssh_args = self.execute_command_args(command)
            with capture_duration() as duration:
                result          = start_process("ssh", ssh_args)                                 # execute command using subprocess.run(...)
            result['duration']  = duration.data()
            return result
        return status_error(error='in execute_command not all required vars were setup')

    def execute_command__print(self, command):
        self.print_header_for_command(command)
        result = self.execute_command(command)
        pprint(result)
        return result

    def execute_python__code(self, python_code, python_executable='python3'):
        python_command  = f"{python_executable} -c \"{python_code}\""
        return self.execute_command(python_command)

    def execute_python__code__return_stdout(self, *args, **kwargs):
        return self.execute_python__code(*args, **kwargs).get('stdout').strip()

    def execute_python__function(self, function, python_executable='python3'):
        function_name   = function.__name__
        function_code   = function_source_code(function)
        exec_code       = f"{function_code}\nresult= {function_name}(); print(result)"
        python_command  = f"{python_executable} -c \"{exec_code}\""
        return self.execute_command(python_command)

    def execute_python__function__return_stderr(self, *args, **kwargs):
        return self.execute_python__function(*args, **kwargs).get('stderr').strip()

    def execute_python__function__return_stdout(self, *args, **kwargs):
        return self.execute_python__function(*args, **kwargs).get('stdout').strip()

    def execute_ssh_args(self):
        ssh_args = []
        if self.ssh_port:
            ssh_args += ['-p', str(self.ssh_port)]
        if self.strict_host_check is False:
            ssh_args += ['-o', 'StrictHostKeyChecking=no']  # todo: add support for updating the local hosts file so that we dont need to do this that often
        if self.ssh_key_file:
            ssh_args += ['-i', self.ssh_key_file]
        return ssh_args

    def execute_command_args(self, command=None):
        ssh_args = self.execute_ssh_args()
        if self.ssh_host:
            ssh_args += [self.execute_command_target_host()]
        if command:
           ssh_args += [command]
        return ssh_args

    def execute_command_target_host(self):
        if self.ssh_key_user:
            return f'{self.ssh_key_user}@{self.ssh_host}'
        else:
            return f'{self.ssh_host}'

    def execute_command__return_stdout(self, command):
        return self.execute_command(command).get('stdout', '').strip()

    def execute_command__return_stderr(self, command):
        return self.execute_command(command).get('stderr', '').strip()

    @index_by
    @group_by
    def execute_command__return_dict(self, command):
        stdout = self.execute_command(command).get('stdout').strip()
        return self.parse_stdout_to_dict(stdout)

    # helpers for common linux methods

    def cat(self, path=''):
        command = f'cat {path}'
        return self.execute_command__return_stdout(command)

    @index_by
    def disk_space(self):
        command           = "df -h"
        stdout            = self.execute_command__return_stdout(command)
        stdout_disk_space = stdout.replace('Mounted on', 'Mounted_on')              # todo, find a better way to do this
        disk_space        = self.parse_stdout_to_dict(stdout_disk_space)
        return disk_space

    def find(self, path=''):
        command = f'find {path}'
        return self.execute_command__return_stdout(command)

    def ls(self, path=''):
        command = f'ls {path}'
        ls_raw  = self.execute_command__return_stdout(command)
        return ls_raw.splitlines()

    def mkdir(self, folder):
        command = f'mkdir -p {folder}'
        return self.execute_command__return_stdout(command)

    def memory_usage(self):
        command = "free -h"
        memory_usage_raw = self.execute_command__return_stdout(command)     # todo: add fix for data parsing issue
        return memory_usage_raw.splitlines()

    def rm(self, path=''):
        command = f'rm {path}'
        return self.execute_command__return_stderr(command)

    def running_processes(self,**kwargs):
        command = "ps aux"
        return self.execute_command__return_dict(command, **kwargs)

    def system_uptime(self):
        command = "uptime"
        uptime_raw = self.execute_command__return_stdout(command)
        return uptime_raw.strip()

    def uname(self):
        return self.execute_command__return_stdout('uname')

    def parse_stdout_to_dict(self, stdout):
        lines = stdout.splitlines()
        headers = lines[0].split()
        result = []

        for line in lines[1:]:                                          # Split each line into parts based on whitespace
            parts = line.split()                                        # Combine the parts with headers to create a dictionary
            entry = {headers[i]: parts[i] for i in range(len(headers))}
            result.append(entry)

        return result

    def which(self, target):
        command = f'which {target}'                                     # todo: security-vuln: add protection against code injection
        return self.execute_command__return_stdout(command)

    def whoami(self):
        command = f'whoami'                                     # todo: security-vuln: add protection against code injection
        return self.execute_command__return_stdout(command)

    # print helpers
    def print_ls(self, path=''):
        pprint(self.ls(path))
        return self

    def print_exec(self, command=''):
        return self.exec__print(command)

    def print_header_for_command(self, command):
        print('\n')
        print('*' * (30 + len(command)))
        print(f'******   stdout for: {command}   ******')
        print('*' * (30 + len(command)))
        print()

    # def ifconfig(self):
    #     command = "export PATH=$PATH:/sbin && ifconfig"               # todo add example with PATH modification
    #     return self.execute_command__return_stdout(command)

    # def ifconfig(self):                                               # todo add command to execute in separate bash (see when it is needed)
    #     command = "bash -l -c 'ifconfig'"
    #     return self.execute_command__return_stdout(command)
    # if port_forward:      # todo: add support for port forward   (this will need async execution)
    #     local_port  = port_forward.get('local_port' )
    #     remote_ip   = port_forward.get('remote_ip'  )
    #     remote_port = port_forward.get('remote_port')

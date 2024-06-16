from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.context_managers.capture_duration          import capture_duration
from osbot_utils.decorators.lists.group_by                  import group_by
from osbot_utils.decorators.lists.index_by                  import index_by
from osbot_utils.utils.Dev                                  import pprint
from osbot_utils.utils.Env                                  import get_env
from osbot_utils.utils.Http import is_port_open
from osbot_utils.utils.Misc                                 import str_to_int, str_to_bool
from osbot_utils.utils.Process import start_process, run_process
from osbot_utils.utils.Status                               import status_error

ENV_VAR__SSH__HOST              = 'SSH__HOST'
ENV_VAR__SSH__PORT              = 'SSH__PORT'
ENV_VAR__SSH__KEY_FILE          = 'SSH__KEY_FILE'
ENV_VAR__SSH__USER              = 'SSH__USER'
ENV_VAR__SSH__STRICT_HOST_CHECK = 'SSH__STRICT_HOST_CHECK'


class SSH__Execute(Type_Safe):
    ssh_host          : str
    ssh_port          : int  = 22
    ssh_key_file      : str
    ssh_key_user      : str
    strict_host_check : bool = False
    print_after_exec  : bool = False

    # execution & other commands # todo refactor into separate class
    def exec(self, command):
        return self.execute_command__return_stdout(command)

    def exec__print(self, command):
        result = self.execute_command__return_stdout(command)
        self.print_header_for_command(command)
        self.print_status__stderr__stdout(result)
        return result

    def execute_command(self, command):
        if self.ssh_setup_ok()  and command:
            ssh_args = self.execute_command_args(command)
            with capture_duration() as duration:
                result          = start_process("ssh", ssh_args)                                 # execute command using subprocess.run(...)
            result['duration']  = duration.data()
            if self.print_after_exec:
                self.print_status__stderr__stdout(result)
            return result
        return status_error(error='in execute_command not all required vars were setup')

    def execute_command__print(self, command):
        self.print_header_for_command(command)
        result = self.execute_command(command)
        self.print_status__stderr__stdout(result)
        return result

    def execute_ssh_args(self):
        ssh_args = []
        if self.ssh_port:
            ssh_args += ['-p', str(self.ssh_port)]
        if self.strict_host_check is False:
            ssh_args += ['-o', 'StrictHostKeyChecking=no']
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

    @index_by
    @group_by
    def execute_command__return_list(self, command):
        stdout = self.execute_command(command).get('stdout').strip()
        return self.parse_stdout_to_list(stdout)

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

    def parse_stdout_to_dict(self, stdout):
        lines = stdout.splitlines()
        headers = lines[0].split()
        result = []

        for line in lines[1:]:                                          # Split each line into parts based on whitespace
            parts = line.split()                                        # Combine the parts with headers to create a dictionary
            entry = {headers[i]: parts[i] for i in range(len(headers))}
            result.append(entry)

        return result

    def parse_stdout_to_list(self, stdout):  # todo: add support for more ways to split the data
        lines = stdout.splitlines()
        return lines


    def ssh_setup_ok(self):
        # todo: add check to see if ssh executable exists (this check can be cached)
        if self.ssh_host and self.ssh_key_file and self.ssh_key_user:
            return True
        return False

    def ssh_not__setup_ok(self):
        return self.ssh_setup_ok() is False

    def ssh_host_available(self):
        return is_port_open(self.ssh_host, self.ssh_port)

    def ssh_host_not_available(self):
        return self.ssh_host_available() is False

    def print_status__stderr__stdout(self, result):
        print()
        print( '┌──────────────────────────────────────────')
        print(f'├ command: {result.get("command")        }')
        print(f'│ status : {result.get("status" ).strip()}')
        print(f'│ stderr : {result.get("stderr" ).strip()}')
        print(f'│ stdout : {result.get("stdout" ).strip()}')
        return self

    def print_header_for_command(self, command):
        print('\n')
        print('*' * (30 + len(command)))
        print(f'******   stdout for: {command}   ******')
        print('*' * (30 + len(command)))
        print()

    def remove_server_ssh_host_fingerprint(self):           # todo: refactor to utils class
        cmd_ssh_keyscan = "ssh-keygen"
        cmd_remove_host = ['-R', f'[{self.ssh_host}]:{self.ssh_port}']
        return run_process(cmd_ssh_keyscan, cmd_remove_host)

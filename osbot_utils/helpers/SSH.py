from decimal import Decimal

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.context_managers.capture_duration import capture_duration
from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.utils.Misc import timestamp_utc_now
from osbot_utils.utils.Process import start_process
from osbot_utils.utils.Status import status_error

class SSH(Kwargs_To_Self):
    ssh_host          : str
    ssh_key_file      : str
    ssh_key_user      : str
    strict_host_check : bool = False

    def execute_command(self, command):
        if self.ssh_host and self.ssh_key_file and self.ssh_key_user and command:             # todo: add check to see if ssh executable exists (this check can be cached)
            ssh_args = self.execute_command_args(command)
            with capture_duration() as duration:
                result          = start_process("ssh", ssh_args)                                 # execute command using subprocess.run(...)
            result['duration']  = duration.data()
            return result
        return status_error(error='in execute_command not all required vars were setup')

    def execute_command_args(self, command=None):
        ssh_args = []
        if self.strict_host_check is False:
            ssh_args += ['-o', 'StrictHostKeyChecking=no']          # todo: add support for updating the local hosts file so that we dont need to do this that often
        if self.ssh_key_file:
            ssh_args += ['-i', self.ssh_key_file]

        if self.ssh_host:
            if self.ssh_key_user:
                ssh_args += [f'{self.ssh_key_user}@{self.ssh_host}']
            else:
                ssh_args += [f'{self.ssh_host}'                    ]
        if command:
           ssh_args += [command]
        return ssh_args

    def execute_command__return_stdout(self, command):
        return self.execute_command(command).get('stdout').strip()

    @index_by
    @group_by
    def execute_command__return_dict(self, command):
        stdout = self.execute_command(command).get('stdout').strip()
        return self.parse_stdout_to_dict(stdout)

    # helpers for common linux methods
    @index_by
    def disk_space(self):
        command           = "df -h"
        stdout            = self.execute_command__return_stdout(command)
        stdout_disk_space = stdout.replace('Mounted on', 'Mounted_on')              # todo, find a better way to do this
        disk_space        = self.parse_stdout_to_dict(stdout_disk_space)
        return disk_space

    def ls(self, path=''):
        command = f'ls {path}'
        ls_raw  = self.execute_command__return_stdout(command)
        return ls_raw.splitlines()

    def memory_usage(self):
        command = "free -h"
        memory_usage_raw = self.execute_command__return_stdout(command)     # todo: add fix for data parsing issue
        return memory_usage_raw.splitlines()

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
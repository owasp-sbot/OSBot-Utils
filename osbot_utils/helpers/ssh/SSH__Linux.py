from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.decorators.lists.index_by      import index_by
from osbot_utils.helpers.ssh.SSH__Execute       import SSH__Execute


class SSH__Linux(Kwargs_To_Self):
    ssh_execute : SSH__Execute

    def apt_update(self):
        return self.ssh_execute.execute_command__return_stdout('apt-get update')

    def apt_install(self, package_name):
        return self.ssh_execute.execute_command(f'apt-get install -y {package_name}')

    def cat(self, path=''):
        command = f'cat {path}'
        return self.ssh_execute.execute_command__return_stdout(command)

    @index_by
    def disk_space(self):
        command = "df -h"
        stdout = self.ssh_execute.execute_command__return_stdout(command)
        stdout_disk_space = stdout.replace('Mounted on', 'Mounted_on')  # todo, find a better way to do this
        disk_space = self.ssh_execute.parse_stdout_to_dict(stdout_disk_space)
        return disk_space

    def dir_exists(self, folder_name):
        message__folder_exists     = "Folder exists"
        message__folder_not_exists = "Folder does not exist"
        test_command               = f'test -d {folder_name} && echo "{message__folder_exists}"  || echo "{message__folder_not_exists}"'
        result                     = self.ssh_execute.execute_command__return_stdout(test_command)
        if result == message__folder_exists:
            return True
        if result == message__folder_not_exists:
            return False

    def echo(self, message):
        return self.ssh_execute.execute_command__return_stdout(f"echo '{message}'")

    def find(self, path=''):
        command = f'find {path}'
        return self.ssh_execute.execute_command__return_list(command)

    def ls(self, path=''):
        command = f'ls {path}'
        ls_raw  = self.ssh_execute.execute_command__return_stdout(command)
        return ls_raw.splitlines()

    def memory_usage(self):
        command = "free -h"
        memory_usage_raw = self.ssh_execute.execute_command__return_stdout(command)     # todo: add fix for data parsing issue
        return memory_usage_raw.splitlines()


    def mkdir(self, folder):
        command = f'mkdir -p {folder}'
        return self.ssh_execute.execute_command(command)

    def mv(self, source, destination):
        command = f'mv {source} {destination}'
        return self.ssh_execute.execute_command(command)

    def pwd(self):
        return self.ssh_execute.execute_command__return_stdout('pwd')

    def rm(self, path=''):
        command = f'rm {path}'
        return self.ssh_execute.execute_command__return_stderr(command)

    def rmdir(self, folder):
        command = f'rmdir {folder}'
        return self.ssh_execute.execute_command(command)

    def running_processes(self,**kwargs):
        command = "ps aux"
        return self.ssh_execute.execute_command__return_dict(command, **kwargs)

    def system_uptime(self):
        command = "uptime"
        uptime_raw = self.ssh_execute.execute_command__return_stdout(command)
        return uptime_raw.strip()

    def uname(self):
        return self.ssh_execute.execute_command__return_stdout('uname')

    def which(self, target):
        command = f'which {target}'                                     # todo: security-vuln: add protection against code injection
        return self.ssh_execute.execute_command__return_stdout(command)

    def whoami(self):
        command = f'whoami'
        return self.ssh_execute.execute_command__return_stdout(command)

    # todo: add methods below (and respective tests)

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
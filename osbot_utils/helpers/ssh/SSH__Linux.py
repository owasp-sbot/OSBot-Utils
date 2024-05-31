from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.helpers.ssh.SSH import SSH
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists


class SSH__Linux(Kwargs_To_Self):
    ssh : SSH

    def cat(self, path=''):
        command = f'cat {path}'
        return self.ssh.execute_command__return_stdout(command)


    @index_by
    def disk_space(self):
        command = "df -h"
        stdout = self.ssh.execute_command__return_stdout(command)
        stdout_disk_space = stdout.replace('Mounted on', 'Mounted_on')  # todo, find a better way to do this
        disk_space = self.ssh.parse_stdout_to_dict(stdout_disk_space)
        return disk_space

    def dir_exists(self, folder_name):
        message__folder_exists     = "Folder exists"
        message__folder_not_exists = "Folder does not exist"
        test_command               = f'test -d {folder_name} && echo "{message__folder_exists}"  || echo "{message__folder_not_exists}"'
        result                     = self.ssh.execute_command__return_stdout(test_command)
        if result == message__folder_exists:
            return True
        if result == message__folder_not_exists:
            return False

    def echo(self, message):
        return self.ssh.execute_command__return_stdout(f"echo '{message}'")

    def find(self, path=''):
        command = f'find {path}'
        return self.ssh.execute_command__return_list(command)

    def ls(self, path=''):
        command = f'ls {path}'
        ls_raw  = self.ssh.execute_command__return_stdout(command)
        return ls_raw.splitlines()

    def mkdir(self, folder):
        command = f'mkdir -p {folder}'
        return self.ssh.execute_command(command)

    def rmdir(self, folder):
        command = f'rmdir {folder}'
        return self.ssh.execute_command(command)


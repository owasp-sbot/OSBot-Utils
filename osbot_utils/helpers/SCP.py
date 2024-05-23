from osbot_utils.context_managers.capture_duration import capture_duration
from osbot_utils.helpers.SSH import SSH
from osbot_utils.testing.Temp_Zip import Temp_Zip
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_exists, file_not_exists, file_name
from osbot_utils.utils.Process import start_process
from osbot_utils.utils.Status import status_error
from osbot_utils.utils.Zip import zip_folder


class SCP(SSH):

    def copy_file_to_host(self, local_file, host_file=None):
        if file_not_exists(local_file):
            return status_error(error="in copy_file_to_host, local_file provided doesn't exist in current host", data={'local_file':local_file})
        if host_file is None:
            host_file = file_name(local_file)
        scp_args = self.execute_ssh_args()
        scp_args += [local_file]
        scp_args += [f'{self.execute_command_target_host()}:{host_file}']
        return self.execute_scp_command__return_stderr(scp_args)

    def copy_file_from_host(self, host_file, local_file):
        scp_args = self.execute_ssh_args()
        scp_args += [f'{self.execute_command_target_host()}:{host_file}']
        scp_args += [local_file]
        return self.execute_scp_command__return_stderr(scp_args)


    def copy_folder_as_zip_to_host(self, local_folder, unzip_to_folder):
        if file_not_exists(local_folder):
            return status_error(error="in copy_folder_as_zip_to_host, local_folder provided doesn't exist in current host", data={'local_folder':local_folder})
        with Temp_Zip(target=local_folder) as temp_zip:
            host_file = temp_zip.file_name()
            kwargs    = dict(local_file = temp_zip.path(),
                             host_file  = host_file      )
            self.mkdir(unzip_to_folder)
            self.copy_file_to_host(**kwargs)
            command = f'unzip {host_file} -d {unzip_to_folder}'
            self.execute_command(command)
            self.rm(host_file)




    def execute_scp_command(self, scp_args):
        if self.ssh_host and self.ssh_key_file and self.ssh_key_user and scp_args:
            with capture_duration() as duration:
                result = start_process("scp", scp_args)  # execute scp command using subprocess.run(...)
            result['duration'] = duration.data()
            return result
        return status_error(error='in copy_file not all required vars were setup')

    def execute_scp_command__return_stdout(self, scp_args):
        return self.execute_scp_command(scp_args).get('stdout').strip()

    def execute_scp_command__return_stderr(self, scp_args):
        return self.execute_scp_command(scp_args).get('stderr').strip()

from osbot_utils.helpers.duration.decorators.capture_duration  import capture_duration
from osbot_utils.helpers.ssh.SSH__Execute                      import SSH__Execute
from osbot_utils.testing.Temp_Zip                              import Temp_Zip
from osbot_utils.utils.Files                                   import file_not_exists, file_name
from osbot_utils.utils.Process                                 import start_process
from osbot_utils.utils.Status                                  import status_error



class SCP(SSH__Execute):

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
            host_file        = temp_zip.file_name()
            kwargs           = dict(local_file = temp_zip.path(),
                                    host_file  = host_file      )
            command_unzip    = f'unzip {host_file} -d {unzip_to_folder}'
            result_ssh_mkdir = self.mkdir(unzip_to_folder)
            result_scp_zip   = self.copy_file_to_host(**kwargs)
            result_ssh_unzip = self.execute_command(command_unzip)
            result_rm_zip    = self.rm(host_file)
            return dict(result_ssh_mkdir=result_ssh_mkdir ,
                        result_scp_zip  =result_scp_zip   ,
                        result_ssh_unzip=result_ssh_unzip ,
                        result_rm_zip   =result_rm_zip    )

    def execute_scp_command(self, scp_args):
        if self.ssh_host and self.ssh_key_file and self.ssh_key_user and scp_args:
            if scp_args[0] == '-p':         # todo refactor this to a better method/class to create the ssh and scp args
                scp_args[0] = '-P'          #      this hack is to handle the fact that ssh and scp use different flags for the port!! WTF!! :)

            with capture_duration() as duration:
                result = start_process("scp", scp_args)  # execute scp command using subprocess.run(...)
            result['duration'] = duration.data()
            return result
        return status_error(error='in copy_file not all required vars were setup')

    def execute_scp_command__return_stdout(self, scp_args):
        return self.execute_scp_command(scp_args).get('stdout').strip()

    def execute_scp_command__return_stderr(self, scp_args):
        return self.execute_scp_command(scp_args).get('stderr').strip()

from osbot_utils.helpers.ssh.SSH__Linux import SSH__Linux


class SSH__Linux__Amazon(SSH__Linux):

    def install_python3(self):
        execute_commands = ('sudo yum install -y python3.11                 && '  
                            'curl -O https://bootstrap.pypa.io/get-pip.py   && '
                            'sudo python3.11 get-pip.py'                       )

        return self.ssh_execute.execute_command__return_stdout(execute_commands)

    def pip_install(self, package_name):
        return self.ssh_execute.execute_command__return_stdout(f'pip3.11 install {package_name}')
from decimal import Decimal

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.context_managers.capture_duration import capture_duration
from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.ssh.SSH__Execute import SSH__Execute
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env import get_env
from osbot_utils.utils.Functions import function_source_code
from osbot_utils.utils.Misc import timestamp_utc_now, str_to_bool, str_to_int
from osbot_utils.utils.Process import start_process, run_process
from osbot_utils.utils.Status import status_error


class SSH(Kwargs_To_Self):





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



    # helpers for common linux methods



    def rm(self, path=''):
        command = f'rm {path}'
        return self.execute_command__return_stderr(command)






    def whoami(self):
        command = f'whoami'                                     # todo: security-vuln: add protection against code injection
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


    def setup(self):
        self.ssh_execute().setup()
        return self


    # todo: refactor all methods above to specfic classes related to what those methods are
    #       then create methods (like bellow) to provide a more user friendly interface

    @cache_on_self
    def ssh_execute(self):
        return SSH__Execute()


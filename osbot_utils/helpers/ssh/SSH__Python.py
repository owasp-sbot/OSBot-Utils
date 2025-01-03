from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.helpers.ssh.SSH__Execute import SSH__Execute
from osbot_utils.helpers.ssh.SSH__Linux import SSH__Linux
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Functions import function_source_code
from osbot_utils.utils.Lists import list_index_by

PYTHON3__LINUX__INSTALLER = 'python3'

class SSH__Python(Type_Safe):
    ssh_execute: SSH__Execute
    ssh_linux  : SSH__Linux

    def execute_python__code(self, python_code, python_executable='python3'):
        python_command  = f"{python_executable} -c \"{python_code}\""
        return self.ssh_execute.execute_command(python_command)

    def execute_python__code__return_stdout(self, *args, **kwargs):
        return self.execute_python__code(*args, **kwargs).get('stdout').strip()

    def execute_python__function(self, function, python_executable='python3'):
        function_name   = function.__name__
        function_code   = function_source_code(function)
        exec_code       = f"{function_code}\nresult= {function_name}(); print(result)"
        return self.execute_python__code(exec_code)

    def execute_python__function__return_stderr(self, *args, **kwargs):
        return self.execute_python__function(*args, **kwargs).get('stderr').strip()

    def execute_python__function__return_stdout(self, *args, **kwargs):
        return self.execute_python__function(*args, **kwargs).get('stdout').strip()

    def install_python3(self):
        return self.ssh_linux.apt_install(PYTHON3__LINUX__INSTALLER)

    def pip_list(self):
        pip_list = self.ssh_execute.execute_command__return_dict('pip list')
        return list_index_by(pip_list, 'Package')

    def pip_install(self, package_name):
        return self.ssh_execute.execute_command__return_stdout(f'pip install {package_name}')

    def pip_version(self):
        return self.ssh_execute.execute_command__return_stdout('pip --version')

    def python_version(self):
        return self.ssh_execute.execute_command__return_stdout('python3 --version')


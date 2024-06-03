from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.ssh.SSH__Execute import SSH__Execute


class SSH__Python(Type_Safe):
    ssh_execute: SSH__Execute

    def execute_python__code(self, python_code, python_executable='python3'):
        python_command  = f"{python_executable} -c \"{python_code}\""
        return self.ssh_execute.execute_command(python_command)

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
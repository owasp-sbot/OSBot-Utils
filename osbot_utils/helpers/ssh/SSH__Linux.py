from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.ssh.SSH import SSH


class SSH__Linux(Kwargs_To_Self):
    ssh : SSH

    def echo(self, message):
        return self.ssh.execute_command__return_stdout(f"echo '{message}'")
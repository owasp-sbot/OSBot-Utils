from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.helpers.ssh.SCP                    import SCP
from osbot_utils.helpers.ssh.SSH__Execute           import SSH__Execute
from osbot_utils.helpers.ssh.SSH__Linux             import SSH__Linux
from osbot_utils.helpers.ssh.SSH__Linux__Amazon import SSH__Linux__Amazon
from osbot_utils.helpers.ssh.SSH__Python            import SSH__Python

class SSH(Type_Safe):       # todo: add ip_address to global vars here, and when that is done, add the wait_for_ssh method (that exists in EC2_Instance)

    def setup(self):
        self.ssh_execute().setup()
        return self

    def exec(self,command):
        return self.ssh_execute().execute_command(command)
    @cache_on_self
    def scp(self):
        kwargs = self.ssh_execute().__locals__()        # get the current ssh config details
        scp = SCP(**kwargs)                             # use it in the ctor of SCP
        return scp

    @cache_on_self
    def ssh_execute(self):
        return SSH__Execute()

    @cache_on_self
    def ssh_linux(self):
        return SSH__Linux(ssh_execute = self.ssh_execute())

    @cache_on_self
    def ssh_linux_amazon(self):
        return SSH__Linux__Amazon(ssh_execute=self.ssh_execute())

    @cache_on_self
    def ssh_python(self):
        return SSH__Python(ssh_execute = self.ssh_execute(), ssh_linux = self.ssh_linux())


from decimal import Decimal

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.context_managers.capture_duration import capture_duration
from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.ssh.SSH__Execute import SSH__Execute
from osbot_utils.helpers.ssh.SSH__Python import SSH__Python
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env import get_env
from osbot_utils.utils.Functions import function_source_code
from osbot_utils.utils.Misc import timestamp_utc_now, str_to_bool, str_to_int
from osbot_utils.utils.Process          import start_process, run_process
from osbot_utils.utils.Status           import status_error


class SSH(Kwargs_To_Self):

    def setup(self):
        self.ssh_execute().setup()
        return self

    @cache_on_self
    def ssh_execute(self):
        return SSH__Execute()

    @cache_on_self
    def ssh_python(self):
        return SSH__Python(ssh_execute = self.ssh_execute())
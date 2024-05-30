from osbot_utils.helpers.ssh.SSH import SSH
from osbot_utils.utils.Env import get_env
from osbot_utils.utils.Misc import list_set, random_text
from osbot_utils.utils.Status import status_ok, status_error

ENV_VAR_TEST_OSBOT__SSH_HOST      = 'SSH__HOST'
ENV_VAR_TEST_OSBOT__SSH_KEY_FILE  = 'SSH__KEY_FILE__FILE'
ENV_VAR_TEST_OSBOT__SSH_KEY_USER  = 'SSH__KEY_FILE__USER'

ENV_VARS__FOR_SSH = {'ssh_host'         : 'SSH__HOST'              ,
                     'ssh_key_file'     : 'SSH__KEY_FILE__FILE'    ,
                     'ssh_key_user'     : 'SSH__KEY_FILE__USER'    ,
                     'strict_host_check': 'SSH__STRICT_HOST_CHECK' }

class SSH__Health_Check(SSH):

    def check_connection(self):
        text_message = random_text('echo')
        response = self.execute_command(f'echo "{text_message}"')
        if response.get('status') == 'ok':
            stderr = response.get('stderr').strip()
            if stderr == '':
                stdout = response.get('stdout').strip()
                if stdout == text_message:
                    return status_ok(message='connection ok')
                else:
                    return status_error(message=f'expected stdout did not march: {text_message} != {stdout}')
            else:
                return status_error(message=f'stderr was not empty', error=stderr, data=response)
        else:
            return status_error(message=f'request failed', data=response)

    def env_vars_names(self):
        return list_set(ENV_VARS__FOR_SSH)

    def env_vars_values(self):
        values = {}
        for key, value in ENV_VARS__FOR_SSH.items():
            env_value = get_env(value)
            values[key] = env_value
        return values

    def env_vars_set_ok(self):
        env_values = self.env_vars_values()
        if  (env_values.get('ssh_host'    ) and
             env_values.get('ssh_key_file') and
             env_values.get('ssh_key_user')    ):
                return True
        return False



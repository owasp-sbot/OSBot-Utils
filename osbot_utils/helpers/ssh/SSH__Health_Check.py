from osbot_utils.helpers.ssh.SSH__Execute import ENV_VAR__SSH__HOST, ENV_VAR__SSH__KEY_FILE, ENV_VAR__SSH__USER, \
    ENV_VAR__SSH__PORT, ENV_VAR__SSH__STRICT_HOST_CHECK, SSH__Execute
from osbot_utils.utils.Env import get_env
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Status import status_ok, status_error

ENV_VARS__FOR_SSH = {'ssh_host'         : ENV_VAR__SSH__HOST              ,
                     'ssh_key_file'     : ENV_VAR__SSH__KEY_FILE          ,
                     'ssh_key_user'     : ENV_VAR__SSH__USER              ,
                     'ssh_port'         : ENV_VAR__SSH__PORT              ,
                     'strict_host_check': ENV_VAR__SSH__STRICT_HOST_CHECK }

class SSH__Health_Check(SSH__Execute):

    def check_connection(self):
        text_message = 'test connection'  #random_text('echo')
        response = self.execute_command(f'echo {text_message}')
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



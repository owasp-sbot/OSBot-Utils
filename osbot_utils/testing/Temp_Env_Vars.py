import os
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Env           import del_env, set_env


class Temp_Env_Vars(Type_Safe):
    env_vars         : dict
    original_env_vars: dict

    def __enter__(self):
        return self.set_vars()

    def __exit__(self, exc_type, exc_value, traceback):
        self.restore_vars()

    def set_vars(self):
        for key, value in self.env_vars.items():
            self.original_env_vars[key] = os.environ.get(key)                   # Backup original environment variables and set new ones
            set_env(key, value)
        return self

    def restore_vars(self):
        for key in self.env_vars:                                               # Restore original environment variables
            if self.original_env_vars[key] is None:
                del_env(key)
            else:
                set_env(key, self.original_env_vars[key])

import os

from osbot_utils.base_classes.Type_Safe import Type_Safe


class Temp_Env_Vars(Type_Safe):
    env_vars         : dict
    original_env_vars: dict

    def __enter__(self):
        for key, value in self.env_vars.items():
            self.original_env_vars[key] = os.environ.get(key)                   # Backup original environment variables and set new ones
            os.environ[key] = value

    def __exit__(self, exc_type, exc_value, traceback):
        for key in self.env_vars:                                               # Restore original environment variables
            if self.original_env_vars[key] is None:
                del os.environ[key]
            else:
                os.environ[key] = self.original_env_vars[key]
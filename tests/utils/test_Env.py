import os
from unittest import TestCase

from osbot_utils.utils.Env import env_value, env_vars, env_vars_list, load_dotenv
from osbot_utils.utils.Lists import list_contains_list


class test_Env(TestCase):

    def test_env_value(self):
        load_dotenv()
        assert env_value("ENV_VAR_1") == "ENV_VAR_1_VALUE"

    def test_env_vars(self):
        os.environ.__setitem__("ENV_VAR_FROM_CODE", "ENV_VAR_FROM_CODE_VALUE")
        loaded_env_vars = env_vars(reload_vars=True)
        assert loaded_env_vars.get("ENV_VAR_1"        ) == 'ENV_VAR_1_VALUE'
        assert loaded_env_vars.get("ENV_VAR_2"        ) == 'ENV_VAR_2_VALUE'
        assert loaded_env_vars.get("ENV_VAR_FROM_CODE") == 'ENV_VAR_FROM_CODE_VALUE'

    def test_env_vars_list(self):
        assert env_vars_list().__contains__("ENV_VAR_1")
        assert env_vars_list().__contains__("ENV_VAR_2")
        assert env_vars_list() == sorted(set(env_vars()))
        assert list_contains_list(env_vars_list(), ['PATH', 'HOME', 'PWD']) is True
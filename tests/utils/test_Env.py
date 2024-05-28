import os
from unittest import TestCase

from osbot_utils.testing.Temp_File import Temp_File
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env import env_value, env_vars, env_vars_list, load_dotenv, unload_dotenv
from osbot_utils.utils.Files import file_not_exists, file_exists
from osbot_utils.utils.Lists import list_contains_list


class test_Env(TestCase):

    def tearDown(self) -> None:
        unload_dotenv()

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
        assert "ENV_VAR_1" not in env_vars_list()
        assert "ENV_VAR_2" not in env_vars_list()
        load_dotenv()
        assert "ENV_VAR_1" in env_vars_list()
        assert "ENV_VAR_2" in env_vars_list()
        assert env_vars_list() == sorted(set(env_vars()))
        assert list_contains_list(env_vars_list(), ['PATH', 'HOME', 'PWD']) is True

    def test_load_dotenv(self):
        env_file_data = """
AN_VAR_1=41
AN_VAR_2='42'
ENV_VAR_2='42 is the answer'
AN_VAR_3_WITH_SPACES  =  '42'
"""

        with Temp_File(contents=env_file_data, file_name='.env') as temp_file:
            assert file_exists(temp_file.file_path)
            assert 'AN_VAR_1'  not in env_vars()
            assert 'ENV_VAR_2' not in env_vars()
            load_dotenv()
            assert 'AN_VAR_1' not in env_vars()                         # confirm vars in temp_file have not  been loaded
            assert 'ENV_VAR_2' in env_vars()                            # confirms value in the default .env in the root of this repo
            assert os.getenv('ENV_VAR_2') =='ENV_VAR_2_VALUE'           #          that is there had nas not been changed to the value in temp_file
            assert os.getenv('ENV_VAR_2') == env_value('ENV_VAR_2')
            load_dotenv(dotenv_path=temp_file.file_path, override=False)
            assert 'AN_VAR_1' in env_vars()                             # now AN_VAR_1 exists in the env_vars
            assert env_value('AN_VAR_1') == '41'                        # and has the value from the temp_file (which was converted to a string)
            assert env_value('AN_VAR_2') == '42'
            assert os.getenv('ENV_VAR_2') == 'ENV_VAR_2_VALUE'          # due to override=False the value in the default .env file is still the same
            load_dotenv(dotenv_path=temp_file.file_path, override=True)
            assert os.getenv('ENV_VAR_2') == '42 is the answer'         # with override=True the value from the temp_file is now used

            assert os.getenv('AN_VAR_3_WITH_SPACES') == '42'            # confirm that spaces are removed from the key and value


            unload_dotenv(dotenv_path=temp_file.file_path)              # remove the values from the temp_file

            assert os.getenv('AN_VAR_1'            ) is None            # confirm that the values have been removed
            assert os.getenv('AN_VAR_2'            ) is None
            assert os.getenv('AN_VAR_3_WITH_SPACES') is None
            assert os.getenv('ENV_VAR_1'           ) is not None        # these values are still in the env_vars
            assert os.getenv('ENV_VAR_2'           ) is None            # except for this one , which will have been removed since it existed in the temp_file

            unload_dotenv()                                             # trigger unload of the .env that is in the root of this repo
            assert os.getenv('ENV_VAR_1'           ) is None            # confirm that the values from the .env file have beeb removed
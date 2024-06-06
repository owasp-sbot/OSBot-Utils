import os
from os.path import abspath
from unittest import TestCase

from osbot_utils.testing.Temp_Folder import Temp_Folder

from osbot_utils.utils.Dev import pprint

from osbot_utils.testing.Temp_File  import Temp_File
from osbot_utils.utils.Env import env_value, env_vars, env_vars_list, load_dotenv, unload_dotenv, platform_darwin, \
    find_dotenv_file
from osbot_utils.utils.Files import file_not_exists, file_exists, file_create, file_delete, file_full_path, \
    parent_folder, current_temp_folder, path_combine
from osbot_utils.utils.Lists        import list_contains_list


class test_Env(TestCase):
    temp_env_file          = '.env'
    temp_env_file_contents = """
                ENV_VAR_1='ENV_VAR_1_VALUE'
                ENV_VAR_2='ENV_VAR_2_VALUE'
                """
    @classmethod
    def setUpClass(cls):
        assert file_not_exists(test_Env.temp_env_file)
        file_create(test_Env.temp_env_file, test_Env.temp_env_file_contents)

    @classmethod
    def tearDownClass(cls):
        assert file_exists(test_Env.temp_env_file)
        file_delete(test_Env.temp_env_file)
        assert file_not_exists(test_Env.temp_env_file)


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
        if platform_darwin():  # todo: figure out why this is failing on docker
            assert "ENV_VAR_1" not in env_vars_list()
            assert "ENV_VAR_2" not in env_vars_list()
            load_dotenv()
            assert "ENV_VAR_1" in env_vars_list()
            assert "ENV_VAR_2" in env_vars_list()
            assert env_vars_list() == sorted(set(env_vars()))
            assert list_contains_list(env_vars_list(), ['PATH', 'HOME', 'PWD']) is True

    def test_find_dotenv_file(self):
        assert find_dotenv_file() == file_full_path(test_Env.temp_env_file)                   # we should find the temp .env that was added to the current test folder
        assert find_dotenv_file(parent_folder(path='.', use_full_path=True)) is None          # there should be no .env paths anywere in the current parent path folders
        with Temp_Folder() as folder_a:
            with Temp_Folder(parent_folder=folder_a.full_path) as folder_b:
                with Temp_Folder(parent_folder=folder_b.full_path) as folder_c:
                    env_file__in_folder_a = file_create(path_combine(folder_a.full_path, '.env'), 'TEMP__ENV_VAR_A=1')
                    env_file__in_folder_b = file_create(path_combine(folder_b.full_path, '.env'), 'TEMP__ENV_VAR_B=1')
                    env_file__in_folder_c = file_create(path_combine(folder_c.full_path, '.env'), 'TEMP__ENV_VAR_C=1')

                    assert parent_folder(folder_c.full_path) == folder_b.full_path
                    assert parent_folder(folder_b.full_path) == folder_a.full_path
                    assert parent_folder(folder_a.full_path) == current_temp_folder()

                    assert parent_folder(env_file__in_folder_a) == folder_a.full_path
                    assert parent_folder(env_file__in_folder_b) == folder_b.full_path
                    assert parent_folder(env_file__in_folder_c) == folder_c.full_path

                    assert find_dotenv_file(folder_c.full_path) == env_file__in_folder_c
                    assert find_dotenv_file(folder_b.full_path) == env_file__in_folder_b
                    assert find_dotenv_file(folder_a.full_path) == env_file__in_folder_a

                    file_delete(env_file__in_folder_c)
                    assert find_dotenv_file(folder_c.full_path) == env_file__in_folder_b
                    assert find_dotenv_file(folder_b.full_path) == env_file__in_folder_b
                    assert find_dotenv_file(folder_a.full_path) == env_file__in_folder_a

                    file_delete(env_file__in_folder_b)
                    assert find_dotenv_file(folder_c.full_path) == env_file__in_folder_a
                    assert find_dotenv_file(folder_b.full_path) == env_file__in_folder_a
                    assert find_dotenv_file(folder_a.full_path) == env_file__in_folder_a

                    file_delete(env_file__in_folder_a)
                    assert find_dotenv_file(folder_c.full_path) is None
                    assert find_dotenv_file(folder_b.full_path) is None
                    assert find_dotenv_file(folder_a.full_path) is None



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
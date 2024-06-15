import os
from unittest import TestCase

from osbot_utils.testing.Temp_Env_Vars import Temp_Env_Vars
from osbot_utils.utils.Env import get_env


class test_Temp_Env_Vars(TestCase):

    def test__enter__leave__(self):
        env_vars = {'var_1': 'value-1', 'var_2': 'value-2'}

        assert get_env('var_1') is None                                 # Ensure the environment variables are not set initially
        assert get_env('var_2') is None


        with Temp_Env_Vars(env_vars=env_vars):                          # Use Temp_Env_Vars context manager to set the environment variables
            assert get_env('var_1') == 'value-1'                        # Check that the environment variables are set within the context
            assert get_env('var_2') == 'value-2'

        assert get_env('var_1') is None                                 # Ensure the environment variables are restored to their original state
        assert get_env('var_2') is None

        os.environ['var_1'] = 'original-value-1'                        # Check behavior when some variables are initially set
        assert get_env('var_1') == 'original-value-1'
        assert get_env('var_2') is None

        with Temp_Env_Vars(env_vars=env_vars):
            assert get_env('var_1') == 'value-1'
            assert get_env('var_2') == 'value-2'

        assert get_env('var_1') == 'original-value-1'                   # Ensure the environment variables are restored to their original state
        assert get_env('var_2') is None

        del os.environ['var_1']                                         # Clean up
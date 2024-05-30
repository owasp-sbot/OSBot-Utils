from osbot_utils.utils.Env import get_env


def skip_pytest__if_env_var_is_not_set(env_var_name):
    if not get_env(env_var_name):
        import pytest                                                # we can only import this locally since this dependency doesn't exist in the main osbot_utils codebase
        pytest.skip(f"Skipping tests because the {env_var_name} env var doesn't have a value")

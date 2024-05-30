from osbot_utils.utils.Env import get_env, load_dotenv

needs_load_dotenv = True

def skip_pytest__if_env_var_is_not_set(env_var_name):
    if needs_load_dotenv:
        load_dotenv()

    if not get_env(env_var_name):
        import pytest                                                # we can only import this locally since this dependency doesn't exist in the main osbot_utils codebase
        pytest.skip(f"Skipping tests because the {env_var_name} env var doesn't have a value")

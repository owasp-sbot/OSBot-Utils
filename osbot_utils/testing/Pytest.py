from osbot_utils.utils.Env import get_env, load_dotenv, in_python_debugger

needs_load_dotenv = True

def skip_pytest(message=r"Skipping pytest for some reason ¯\_o_/¯"):
    import pytest                                                # we can only import this locally since this dependency doesn't exist in the main osbot_utils codebase
    pytest.skip(message)

def skip_pytest__if_env_var_is_not_set(env_var_name):
    if needs_load_dotenv:
        load_dotenv()

    if not get_env(env_var_name):
        skip_pytest(f"Skipping tests because the {env_var_name} env var doesn't have a value")

def skip__if_in_python_debugger():
    if in_python_debugger():
        skip_pytest("Skipping tests because we are in a debugger")
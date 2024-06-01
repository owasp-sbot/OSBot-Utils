
import os
import sys
from sys                        import platform
from osbot_utils.utils.Files    import all_parent_folders, file_exists
from osbot_utils.utils.Misc     import list_set
from osbot_utils.utils.Str      import strip_quotes

def env__home_root():
    return os.getenv('HOME') == '/root'

def env__terminal_xterm():
    return os.getenv('TERM') == 'xterm'

def env__not_terminal_xterm():
    return not env__terminal_xterm()

def platform_darwin():
    return platform == 'darwin'

def env_value(var_name):
    return env_vars().get(var_name, None)

def env_vars_list():
    return list_set(env_vars())

def env_vars(reload_vars=False):
    """
    if reload_vars reload data from .env file
    then return dictionary with current environment variables
    """
    if reload_vars:
        load_dotenv()
    vars = os.environ
    data = {}
    for key in vars:
        data[key] = vars[key]
    return data

def env_load_from_file(path, override=False):
    if file_exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):                # Strip whitespace and ignore comments
                    continue
                if line.startswith('export '):                      # if the line starts with export, we can ignore it and continue
                    line = line[7:]
                key, value = line.split(sep='=', maxsplit=1)        # Split the line into key and value
                value = strip_quotes(value.strip())                 # Handle case when the value is in quotes
                if override or key.strip() not in os.environ:       # Set the environment variable
                    os.environ[key.strip()] = value.strip()

def env_unload_from_file(path):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):  # Strip whitespace and ignore comments
                    continue
                key, _ = line.split(sep='=', maxsplit=1)  # Split the line into key and value
                key = key.strip()
                if key in os.environ:  # Remove the environment variable if it exists
                    del os.environ[key]

def in_github_action():
    return os.getenv('GITHUB_ACTIONS') == 'true'

def in_python_debugger():
    if sys.gettrace() is not None:              # Check for a trace function
        return True

    pycharm_hosted           = os.getenv('PYCHARM_HOSTED') == '1'                     # Check for PyCharm specific environment variables and other potential indicators
    pydevd_load_values_async = os.getenv('PYDEVD_LOAD_VALUES_ASYNC') is not None
    if pycharm_hosted and pydevd_load_values_async:
        return True

    return False

def load_dotenv(dotenv_path=None, override=False):
    if dotenv_path:                                                 # If a specific dotenv path is provided, load from it
        env_load_from_file(dotenv_path, override)
    else:
        directories = all_parent_folders(include_path=True)         # Define the possible directories to search for the .env file (which is this and all parent folders)
        for directory in directories:                               # Iterate through the directories and load the .env file if found
            env_path = os.path.join(directory, '.env')              # Define the path to the .env file
            if os.path.exists(env_path):                            # If we found one
                env_load_from_file(env_path, override)              # Process it
                break                                               # Stop after loading the first .env file                                                     # Stop after loading the first .env file


def not_in_github_action():
    return in_github_action() is False


def unload_dotenv(dotenv_path=None):
    if dotenv_path:                                                 # If a specific dotenv path is provided, unload from it
        env_unload_from_file(dotenv_path)
    else:
        directories = all_parent_folders(include_path=True)         # Define the possible directories to search for the .env file (which is this and all parent folders)
        for directory in directories:                               # Iterate through the directories and unload the .env file if found
            env_path = os.path.join(directory, '.env')              # Define the path to the .env file
            if os.path.exists(env_path):                            # If we found one
                env_unload_from_file(env_path)                      # Process it
                break                                               # Stop after unloading the first .env file


env_load = load_dotenv
get_env  = os.getenv
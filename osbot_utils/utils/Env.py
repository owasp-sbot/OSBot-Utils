# In Misc.py
import os

from osbot_utils.utils.Files import all_parent_folders
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Str import strip_quotes


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

def load_dotenv():
    directories = all_parent_folders(include_path=True)                     # Define the possible directories to search for the .env file (which is this and all parent folders)
    for directory in directories:                                           # Iterate through the directories and load the .env file if found
        env_path = os.path.join(directory, '.env')                          # Define the path to the .env file
        if os.path.exists(env_path):                                        # if we found one
            with open(env_path) as f:                                       # process it
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):                    # Strip whitespace and ignore comments
                        continue
                    key, value = line.split(sep='=', maxsplit=1)            # Split the line into key and value
                    value = strip_quotes(value.strip())                     # handle case when the value is in quotes
                    os.environ[key.strip()] = value.strip()                 # Set the environment variable
            break                                                           # Stop after loading the first .env file


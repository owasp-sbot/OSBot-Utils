import sys
from osbot_utils.helpers.transformers.Dict__To__Toml import Dict__To__Toml
from osbot_utils.testing.__helpers                   import dict_to_obj
from osbot_utils.utils.Files                         import file_create, file_contents



def dict_to_toml(data):
    return Dict__To__Toml().convert(data)                                                 # Singleton instance for convenience

def toml_dict_to_file(toml_file, data):
    str_toml = dict_to_toml(data)
    return file_create(toml_file, str_toml)

def toml_dict_from_file(toml_file):
    str_toml = file_contents(toml_file)
    return toml_to_dict(str_toml)

def toml_to_dict(str_toml):
    if sys.version_info >= (3, 11):
        import tomllib
        return tomllib.loads(str_toml)
    raise NotImplementedError("TOML parsing is not supported in Python versions earlier than 3.11")


def toml_obj_from_file(toml_file):
    data = toml_dict_from_file(toml_file)
    return dict_to_obj(data)

json_load_file = toml_dict_from_file
toml_file_load = toml_dict_from_file

toml_from_file = toml_dict_from_file
toml_load      = toml_dict_from_file
toml_load_obj  = toml_obj_from_file
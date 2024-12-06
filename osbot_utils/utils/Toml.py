import sys
from osbot_utils.utils.Files   import file_create, file_contents
from osbot_utils.utils.Objects import dict_to_obj


def dict_to_toml(data, indent_level=0):
    toml_str = ""
    indent = " " * (indent_level * 4)

    for key, value in data.items():
        if isinstance(value, dict):
            toml_str += f"{indent}[{key}]\n"
            toml_str += dict_to_toml(value, indent_level + 1)
        elif isinstance(value, (list, tuple, set)):
            toml_str += f"{indent}{key} = [\n"
            for item in value:
                toml_str += f"{indent}    {repr(item)},\n"
            toml_str += f"{indent}]\n"
        elif isinstance(value, str):
            toml_str += f"{indent}{key} = '{value}'\n"
        elif isinstance(value, bool):
            toml_str += f"{indent}{key} = {str(value).lower()}\n"
        else:
            toml_str += f"{indent}{key} = {value}\n"

    return toml_str

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
import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    tomllib = None

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

def toml_to_dict(toml_string):
    if tomllib is None:
        raise NotImplementedError("TOML parsing is not supported in Python versions earlier than 3.11")
    return tomllib.loads(toml_string)
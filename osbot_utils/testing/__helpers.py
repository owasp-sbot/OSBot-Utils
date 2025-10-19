import json
from types                                                                                      import SimpleNamespace
from osbot_utils.testing.__                                                                     import __
from collections.abc                                                                            import Mapping
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Python__Identifier import Safe_Str__Python__Identifier

def dict_to_obj(target):
    if isinstance(target, Mapping):
        new_dict = {}
        for key, value in target.items():                                        # Sanitize the key to ensure it's a valid Python identifier
            safe_key = str(Safe_Str__Python__Identifier(str(key)))
            new_dict[safe_key] = dict_to_obj(value)                              # Recursively convert elements in the dict
        return __(**new_dict)
    elif isinstance(target, list):                                               # Recursively convert elements in the list
        return [dict_to_obj(item) for item in target]
    elif isinstance(target, tuple):                                              # Recursively convert elements in the tuple
        return tuple(dict_to_obj(item) for item in target)

    return target

def obj_to_dict(target):                                                            # Recursively converts an object (SimpleNamespace) back into a dictionary."""
    if isinstance(target, SimpleNamespace):                                         # Convert SimpleNamespace attributes to a dictionary
        return {key: obj_to_dict(value) for key, value in target.__dict__.items()}
    elif isinstance(target, list):                                                  # Handle lists: convert each item in the list
        return [obj_to_dict(item) for item in target]
    elif isinstance(target, tuple):                                                 # Handle tuples: convert each item and return as a tuple
        return tuple(obj_to_dict(item) for item in target)
    elif isinstance(target, set):                                                   # Handle sets: convert each item and return as a set
        return {obj_to_dict(item) for item in target}
    return target                                                                   # Return non-object types as is

def str_to_obj(target):
    if hasattr(target, 'json'):
        return dict_to_obj(target.json())
    return dict_to_obj(json.loads(target))


json_to_obj         = str_to_obj
obj                 = dict_to_obj
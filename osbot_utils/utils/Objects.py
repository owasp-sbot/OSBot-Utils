# todo add tests
import inspect
import json
import os
import types
from typing import get_origin

from dotenv import load_dotenv

from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Str  import str_unicode_escape, str_max_width

def are_types_compatible_for_assigment(source_type, target_type):
    if source_type is target_type:
        return True
    if source_type is int and target_type is float:
        return True
    return False

def base_classes(cls):
    if type(cls) is type:
        target = cls
    else:
        target = type(cls)
    return type_base_classes(target)

def class_functions_names(target):
    return list_set(class_functions(target))

def class_functions(target):
    functions = {}
    for function_name, function_ref in inspect.getmembers(type(target), predicate=inspect.isfunction):
        functions[function_name] = function_ref
    return functions

def class_name(target):
    if target:
        return type(target).__name__

def class_full_name(target):
    if target:
        type_target = type(target)
        type_module = type_target.__module__
        type_name   = type_target.__name__
        return f'{type_module}.{type_name}'

def default_value(target : type):
    try:
        return target()                 #  try to create the object using the default constructor
    except TypeError:
        return None                     # if not return None

def dict_remove(data, target):
    if type(data) is dict:
        if type(target) is list:
            for key in list(data.keys()):
                if key in target:
                    del data[key]
        else:
            if target in data:
                del data[target]
    return data

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

def get_field(target, field, default=None):
    if target is not None:
        try:
            value = getattr(target, field)
            if value is not None:
                return value
        except:
            pass
    return default

def get_missing_fields(target,fields):
    missing_fields = []
    if fields:
        for field in fields:
            if get_field(target, field) is None:
                missing_fields.append(field)
    return missing_fields

def get_value(target, key, default=None):
    if target is not None:
        value = target.get(key)
        if value is not None:
            return value
    return default

def print_object_methods(target, name_width=30, value_width=100, show_private=False, show_internals=False):
    print_object_members(target, name_width=name_width, value_width=value_width,show_private=show_private,show_internals=show_internals, only_show_methods=True)

def print_obj_data_aligned(obj_data):
    print(obj_data_aligned(obj_data))

def print_obj_data_as_dict(target, **kwargs):
    data           = obj_data(target, **kwargs)
    indented_items = obj_data_aligned(data, tab_size=5)
    print("dict(" + indented_items + " )")
    return data

def obj_data_aligned(obj_data, tab_size=0):
    max_key_length = max(len(k) for k in obj_data.keys())                                 # Find the maximum key length
    items          = [f"{k:<{max_key_length}} = {v!r:6}," for k, v in obj_data.items()]   # Format each key-value pair
    items[-1]      = items[-1][:-2]                                                       # Remove comma from the last item
    tab_string = f"\n{' ' * tab_size }"                                                   # apply tabbing (if needed)
    indented_items = tab_string.join(items)                                               # Join the items with newline and
    return indented_items

# todo: add option to not show class methods that are not bultin types
def print_object_members(target, name_width=30, value_width=100, show_private=False, show_internals=False, show_value_class=False, show_methods=False, only_show_methods=False):
    max_width = name_width + value_width
    print()
    print(f"Members for object:\n\t {target} of type:{type(target)}")
    print(f"Settings:\n\t name_width: {name_width} | value_width: {value_width} | show_private: {show_private} | show_internals: {show_internals}")
    print()
    if only_show_methods:
        show_methods = True                                             # need to make sure this setting is True, or there will be no methods to show
        print(f"{'method':<{name_width}} (params)")
    else:
        if show_value_class:
            print(f"{'field':<{name_width}} | {'type':<{name_width}} |value")
        else:
            print(f"{'field':<{name_width}} | value")

    print(f"{'-' * max_width}")
    for name, value in obj_data(target, name_width=name_width, value_width=value_width, show_private=show_private, show_internals=show_internals, show_value_class=show_value_class, show_methods=show_methods, only_show_methods=only_show_methods).items():
        if only_show_methods:
            print(f"{name:<{name_width}} {value}"[:max_width])
        else:
            if show_value_class:
                value_class = obj_full_name(value)
                print(f"{name:<{name_width}} | {value_class:{name_width}} | {value}"[:max_width])
            else:
                print(f"{name:<{name_width}} | {value}"[:max_width])

def obj_base_classes(obj):
    return type_base_classes(type(obj))

def type_base_classes(cls):
    base_classes = cls.__bases__
    all_base_classes = list(base_classes)
    for base in base_classes:
        all_base_classes.extend(type_base_classes(base))
    return all_base_classes

def obj_base_classes_names(obj, show_module=False):
    names = []
    for base in obj_base_classes(obj):
        if show_module:
            names.append(base.__module__ + '.' + base.__name__)
        else:
            names.append(base.__name__)
    return names

def obj_data(target, name_width=30, value_width=100, show_private=False, show_internals=False, show_value_class=False, show_methods=False, only_show_methods=False):
    result = {}
    if show_internals:
        show_private = True                                     # show_private will skip all internals, so need to make sure it is True
    for name, value in inspect.getmembers(target):
        if show_methods is False and type(value) is types.MethodType:
            continue
        if only_show_methods and type(value) is not types.MethodType:
            continue
        if not show_private and name.startswith("_"):
            continue
        if not show_internals and name.startswith("__"):
            continue
        if only_show_methods:
            value = inspect.signature(value)
        if value !=None and type(value) not in [bool, int, float]:
            value       = str(value).encode('unicode_escape').decode("utf-8")
            value       = str_unicode_escape(value)
            value       = str_max_width(value, value_width)
            name        = str_max_width(name, name_width)
        result[name] = value
    return result

# def obj_data(target=None):
#     data = {}
#     for key,value in obj_items(target):
#         data[key] = value
#     return data

def obj_dict(target=None):
    if target and hasattr(target,'__dict__'):
        return target.__dict__
    return {}

def obj_items(target=None):
    return sorted(list(obj_dict(target).items()))

def obj_keys(target=None):
    return sorted(list(obj_dict(target).keys()))

def obj_full_name(target):
    module = target.__class__.__module__
    name   = target.__class__.__qualname__
    return f"{module}.{name}"

def obj_get_value(target=None, key=None, default=None):
    return get_field(target=target, field=key, default=default)

def obj_values(target=None):
    return list(obj_dict(target).values())

def value_type_matches_obj_annotation_for_attr(target, attr_name, value):
    if hasattr(target, '__annotations__'):
        obj_annotations  = target.__annotations__
        if hasattr(obj_annotations,'get'):
            attr_type        = obj_annotations.get(attr_name)
            if attr_type:
                origin_attr_type = get_origin(attr_type)                # to handle when type definion contains an generic
                if origin_attr_type:
                    attr_type = origin_attr_type
                target_type = type(value)
                if are_types_compatible_for_assigment(source_type=target_type, target_type=attr_type):
                    return True
                return target_type is attr_type
    return None





# helper duplicate methods
base_types          = base_classes

obj_list_set        = obj_keys
obj_info            = print_object_members
obj_methods         = print_object_methods

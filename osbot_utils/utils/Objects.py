# todo add tests
import inspect
import pickle
import sys
import types
import typing
from typing import Union

from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Str  import str_unicode_escape, str_max_width

# Backport implementations of get_origin and get_args for Python 3.7
if sys.version_info < (3, 8):
    def get_origin(tp):
        if isinstance(tp, typing._GenericAlias):
            return tp.__origin__
        elif tp is typing.Generic:
            return typing.Generic
        else:
            return None

    def get_args(tp):
        if isinstance(tp, typing._GenericAlias):
            return tp.__args__
        else:
            return ()
else:
    from typing import get_origin, get_args


def are_types_compatible_for_assigment(source_type, target_type):
    if source_type is target_type:
        return True
    if source_type is int and target_type is float:
        return True
    if target_type in source_type.__mro__:          # this means that the source_type has the target_type has of its base types
        return True
    if target_type is callable:                     # handle case where callable was used as the target type
        if source_type is types.MethodType:         #     and a method or function was used as the source type
            return True
        if source_type is types.FunctionType:
            return True
        if source_type is staticmethod:
            return True
    if target_type is typing.Any:
        return True
    return False

def are_types_magic_mock(source_type, target_type):
    from unittest.mock import MagicMock
    if isinstance(source_type, MagicMock):
        return True
    if isinstance(target_type, MagicMock):
        return True
    if source_type is MagicMock:
        return True
    if target_type is MagicMock:
        return True
    # if class_full_name(source_type) == 'unittest.mock.MagicMock':
    #     return True
    # if class_full_name(target_type) == 'unittest.mock.MagicMock':
    #     return True
    return False

def base_classes(cls):
    if type(cls) is type:
        target = cls
    else:
        target = type(cls)
    return type_base_classes(target)

def base_classes_names(cls):
    return [cls.__name__ for cls in base_classes(cls)]

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

def convert_dict_to_value_from_obj_annotation(target, attr_name, value):
    if target is not None and attr_name is not None:
        if hasattr(target, '__annotations__'):
            obj_annotations  = target.__annotations__
            if hasattr(obj_annotations,'get'):
                attribute_annotation = obj_annotations.get(attr_name)
                if 'Type_Safe' in base_classes_names(attribute_annotation):
                    return attribute_annotation(**value)
    return value


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

def enum_from_value(enum_type, value):
    try:
        return enum_type[value]         # Attempt to convert the value to an Enum member by name
    except KeyError:
        raise ValueError(f"Value '{value}' is not a valid member of {enum_type.__name__}.")     # Handle the case where the value does not match any Enum member


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
    return [obj_type for obj_type in type_base_classes(type(obj))]

def type_mro(target):
    if type(target) is type:
        cls = target
    else:
        cls = type(target)
    return list(inspect.getmro(cls))

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

def obj_data(target, convert_value_to_str=True, name_width=30, value_width=100, show_private=False, show_internals=False, show_value_class=False, show_methods=False, only_show_methods=False):
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
        if value is not None and type(value) not in [bool, int, float]:
            if convert_value_to_str:
                value       = str(value).encode('unicode_escape').decode("utf-8")
                value       = str_unicode_escape(value)
                value       = str_max_width(value, value_width)
            name  = str_max_width(name, name_width)                                     # todo: look at the side effects of running this for all (at the moment if we do that we break the test_cache_on_self test)
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

def raise_exception_on_obj_type_annotation_mismatch(target, attr_name, value):
    # todo : check if this is is not causing the type safety issues
    if value_type_matches_obj_annotation_for_attr(target, attr_name, value) is False:               # handle case with normal types
        if value_type_matches_obj_annotation_for_union_attr(target, attr_name, value) is True:      # handle union cases
            return                                                                                  #     this is done like this because value_type_matches_obj_annotation_for_union_attr will return None when there is no Union objects
        raise Exception(f"Invalid type for attribute '{attr_name}'. Expected '{target.__annotations__.get(attr_name)}' but got '{type(value)}'")

def obj_attribute_annotation(target, attr_name):
    if target is not None and attr_name is not None:
        if hasattr(target, '__annotations__'):
            obj_annotations  = target.__annotations__
            if hasattr(obj_annotations,'get'):
                attribute_annotation = obj_annotations.get(attr_name)
                return attribute_annotation
    return None

def obj_is_attribute_annotation_of_type(target, attr_name, expected_type):
    attribute_annotation = obj_attribute_annotation(target, attr_name)
    #attribute_type       = type(attribute_annotation)
    #return attribute_type is expected_type
    if expected_type is attribute_annotation:
        return True
    if expected_type is type(attribute_annotation):
        return True
    return False

def obj_is_type_union_compatible(var_type, compatible_types):
    origin = get_origin(var_type)
    if origin is Union:                                                     # For Union types, including Optionals
        args = get_args(var_type)                                           # Get the argument types
        for arg in args:                                                    # Iterate through each argument in the Union
            if not (arg in compatible_types or arg is type(None)):          # Check if the argument is either in the compatible_types or is type(None)
                return False                                                # If any arg doesn't meet the criteria, return False immediately
        return True                                                         # If all args are compatible, return True
    return var_type in compatible_types or var_type is type(None)           # Check for direct compatibility or type(None) for non-Union types

def value_type_matches_obj_annotation_for_union_attr(target, attr_name, value):
    value_type           = type(value)
    attribute_annotation = obj_attribute_annotation(target,attr_name)
    origin               = get_origin(attribute_annotation)
    if origin is Union:                                                     # For Union types, including Optionals
        args = get_args(attribute_annotation)                               # Get the argument types
        return value_type in args
    return None                                                             # if it is not an Union type just return None (to give an indication to the caller that the comparison was not made)


def pickle_save_to_bytes(target: object) -> bytes:
    return pickle.dumps(target)

def pickle_load_from_bytes(pickled_data: bytes):
    if type(pickled_data) is bytes:
        try:
            return pickle.loads(pickled_data)
        except Exception:
            return {}

def value_type_matches_obj_annotation_for_attr(target, attr_name, value):
    if hasattr(target, '__annotations__'):
        obj_annotations  = target.__annotations__
        if hasattr(obj_annotations,'get'):
            attr_type        = obj_annotations.get(attr_name)
            if attr_type:
                origin_attr_type = get_origin(attr_type)                # to handle when type definion contains an generic
                if origin_attr_type:
                    attr_type = origin_attr_type
                value_type = type(value)
                if are_types_compatible_for_assigment(source_type=value_type, target_type=attr_type):
                    return True
                if are_types_magic_mock(source_type=value_type, target_type=attr_type):
                    return True

                return value_type is attr_type
    return None





# helper duplicate methods
base_types          = base_classes
bytes_to_obj        = pickle_load_from_bytes

full_type_name      = class_full_name

obj_list_set        = obj_keys
obj_info            = print_object_members
obj_methods         = print_object_methods
obj_to_bytes        = pickle_save_to_bytes

pickle_from_bytes   = pickle_load_from_bytes
pickle_to_bytes     = pickle_save_to_bytes

type_full_name      = class_full_name

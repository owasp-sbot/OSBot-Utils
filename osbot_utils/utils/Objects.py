
def base_classes(cls):
    if type(cls) is type:
        target = cls
    else:
        target = type(cls)
    return type_base_classes(target)

def base_classes_names(cls):
    return [cls.__name__ for cls in base_classes(cls)]

def class_functions_names(target):
    from osbot_utils.utils.Misc import list_set

    return list_set(class_functions(target))

def class_functions(target):
    import inspect

    functions = {}
    for function_name, function_ref in inspect.getmembers(type(target), predicate=inspect.isfunction):
        functions[function_name] = function_ref
    return functions

def class_name(target):
    if target:
        return type(target).__name__
    return None

def class_full_name(target):
    if target:
        if isinstance(target, type):  # Check if target is a type
            type_module = target.__module__
            type_name   = target.__name__
        else:  # Handle instances
            type_target = type(target)
            type_module = type_target.__module__
            type_name   = type_target.__name__
        return f'{type_module}.{type_name}'
    return None


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



# def dict_to_obj(target):
#     from collections.abc import Mapping
#
#     if isinstance(target, Mapping):
#         new_dict = {}
#         for key, value in target.items():
#             new_dict[key] = dict_to_obj(value)                                  # Recursively convert elements in the dict
#         return __(**new_dict)
#     elif isinstance(target, list):                                              # Recursively convert elements in the list
#         return [dict_to_obj(item) for item in target]
#     elif isinstance(target, tuple):                                             # Recursively convert elements in the tuple
#         return tuple(dict_to_obj(item) for item in target)
#     # elif hasattr(target, 'json'):                                             # todo: see if we need this. I don't like the idea of adding this extra hidden behaviour to this class
#     #     return dict_to_obj(target.json())
#
#     return target

# def obj_to_dict(target):                                                            # Recursively converts an object (SimpleNamespace) back into a dictionary."""
#     if isinstance(target, SimpleNamespace):                                         # Convert SimpleNamespace attributes to a dictionary
#         return {key: obj_to_dict(value) for key, value in target.__dict__.items()}
#     elif isinstance(target, list):                                                  # Handle lists: convert each item in the list
#         return [obj_to_dict(item) for item in target]
#     elif isinstance(target, tuple):                                                 # Handle tuples: convert each item and return as a tuple
#         return tuple(obj_to_dict(item) for item in target)
#     elif isinstance(target, set):                                                   # Handle sets: convert each item and return as a set
#         return {obj_to_dict(item) for item in target}
#     return target                                                                   # Return non-object types as is


def enum_from_value(enum_type, value):
    if value in enum_type.__members__:                                                              # Try to get by name (e.g., 'SYSTEM')
        return enum_type[value]

    if hasattr(enum_type, '_value2member_map_') and value in enum_type._value2member_map_:          # Try to get by value (e.g., 'system') using the reverse mapping
        return enum_type._value2member_map_[value]

    raise ValueError(f"Value '{value}' is not a valid member of {enum_type.__name__}.")             # If neither worked, raise an error


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
    import inspect

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
    import inspect
    import types
    from osbot_utils.utils.Str import str_unicode_escape, str_max_width

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

def pickle_save_to_bytes(target: object) -> bytes:
    import pickle
    return pickle.dumps(target)

def pickle_load_from_bytes(pickled_data: bytes):
    import pickle
    if type(pickled_data) is bytes:
        try:
            return pickle.loads(pickled_data)
        except Exception:
            return {}

# todo: see if it is possible to add recursive protection to this logic
# todo: we should move this method to the type_safe classes and folders
def serialize_to_dict(obj):
    from decimal                               import Decimal
    from enum                                  import Enum
    from typing                                import List
    from osbot_utils.type_safe.Type_Safe__Base import Type_Safe__Base

    if isinstance(obj, Type_Safe__Base) and hasattr(obj, 'json'):                                   # if it is one of these Type_Safe__Base  classes
        return obj.json()                                                                           #   use the provided .json() method, which handles the type conversions more specifically to those types (dict, list, set and tuple)
    elif hasattr(obj, '__primitive_base__') and isinstance(obj, (str, int, float)):
        return obj.__primitive_base__(obj)
    elif isinstance(obj, Enum):
        if isinstance(obj.value, (str, int, float, bool, type(None))):                          # Check if the enum value is directly serializable
            return obj.value
        elif isinstance(obj.value, (list, tuple, dict, set, frozenset)):                                        # Recursively serialize complex values
            return serialize_to_dict(obj.value)
        else:
            return obj.name                                                                     # Fallback to name for non-serializable values
    elif isinstance(obj, (str, int, float, bool, bytes, Decimal)) or obj is None:                # todo: add support for objects like datetime
        return obj
    elif isinstance(obj, type):
        return f"{obj.__module__}.{obj.__name__}"                                   # save the full type name
    elif isinstance(obj, (list, tuple, List)):                                     # Added tuple here
        return [serialize_to_dict(item) for item in obj]
    elif isinstance(obj, (set, frozenset)):
        return [serialize_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        serialized_dict = {}                                                        # todo: refactor to separate method
        for key, value in obj.items():
            if isinstance(key, type):                                           # Handle type keys by converting to fully qualified string
                serialized_key = f"{key.__module__}.{key.__name__}"
            else:
                serialized_key = key
            serialized_dict[serialized_key] = serialize_to_dict(value)         # Recursively serialize the value
        return serialized_dict
        #return {key: serialize_to_dict(value) for key, value in obj.items()}
    elif callable(obj) and not isinstance(obj, type):                                                         # For functions/lambdas, return a string representation
        if hasattr(obj, '__name__'):
            return obj.__name__
        if hasattr(obj, '__class__'):
            return obj.__class__.__name__
        return str(obj)
    elif hasattr(obj, "__dict__"):
        data = {}                                                                   # todo: look at a more advanced version which saved the type of the object, for example with {'__type__': type(obj).__name__}
        for key, value in obj.__dict__.items():
            if key.startswith('__') is False:                                       # don't process internal variables (for example the ones set by @cache_on_self)
                data[key] = serialize_to_dict(value)                                # Recursive call for complex types
        return data
    else:
        #raise TypeError(f"Type {type(obj)} not serializable")                      # Breaking change (we don't raise exception any more)
        return None                                                                 # just return None







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

# todo: find a way to add these documentations strings to a separate location so that
#       the code is not polluted with them (like in the example below)
#       the data is available in IDE's code complete
import functools
import inspect
import sys
import types
import typing
from decimal                                    import Decimal
from enum                                       import Enum, EnumMeta
from typing                                     import List
from osbot_utils.base_classes.Type_Safe__List   import Type_Safe__List
from osbot_utils.helpers.Random_Guid            import Random_Guid
from osbot_utils.utils.Dev                      import pprint
from osbot_utils.utils.Json                     import json_parse
from osbot_utils.utils.Misc                     import list_set
from osbot_utils.utils.Objects                  import default_value, value_type_matches_obj_annotation_for_attr, \
    raise_exception_on_obj_type_annotation_mismatch, obj_is_attribute_annotation_of_type, enum_from_value, \
    obj_is_type_union_compatible, value_type_matches_obj_annotation_for_union_attr, \
    convert_dict_to_value_from_obj_annotation

# Backport implementations of get_origin and get_args for Python 3.7
if sys.version_info < (3, 8):                                           # pragma: no cover
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

if sys.version_info >= (3, 10):
    NoneType = types.NoneType
else:                                                           # pragma: no cover
    NoneType = type(None)

immutable_types = (bool, int, float, complex, str, tuple, frozenset, bytes, NoneType, EnumMeta)


#todo: see if we can also add type safety to method execution
#      for example if we have an method like def add_node(self, title: str, call_index: int):
#          throw an exception if the type of the value passed in is not the same as the one defined in the method

class Type_Safe:

    def __init__(self, **kwargs):
        """
        Initialize an instance of the derived class, strictly assigning provided keyword
        arguments to corresponding instance attributes.

        Parameters:
            **kwargs: Variable length keyword arguments.

        Raises:
            Exception: If a key from kwargs does not correspond to any attribute
                       pre-defined in the class, an exception is raised to prevent
                       setting an undefined attribute.

        """
        # if 'disable_type_safety' in kwargs:                                 # special case
        #     self.__type_safety__ = kwargs['disable_type_safety'] is False
        #     del kwargs['disable_type_safety']

        for (key, value) in self.__cls_kwargs__().items():                  # assign all default values to self
            if value is not None:                                           # when the value is explicitly set to None on the class static vars, we can't check for type safety
                raise_exception_on_obj_type_annotation_mismatch(self, key, value)
            if hasattr(self, key):
                existing_value = getattr(self, key)
                if existing_value is not None:
                    setattr(self, key, existing_value)
                    continue
            setattr(self, key, value)

        for (key, value) in kwargs.items():                             # overwrite with values provided in ctor
            if hasattr(self, key):
                if value is not None:                                   # prevent None values from overwriting existing values, which is quite common in default constructors
                    setattr(self, key, value)
            else:
                raise ValueError(f"{self.__class__.__name__} has no attribute '{key}' and cannot be assigned the value '{value}'. "
                                 f"Use {self.__class__.__name__}.__default_kwargs__() see what attributes are available")

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

    def __setattr__(self, name, value):
        if not hasattr(self, '__annotations__'):                    # can't do type safety checks if the class does not have annotations
            return super().__setattr__(name, value)

        if value is not None:
            if type(value) is dict:
                value = convert_dict_to_value_from_obj_annotation(self, name, value)
            check_1 = value_type_matches_obj_annotation_for_attr      (self, name, value)
            check_2 = value_type_matches_obj_annotation_for_union_attr(self, name, value)
            if (check_1 is False and check_2 is None  or
                check_1 is None  and check_2 is False or
                check_1 is False and check_2 is False   ):          # fix for type safety assigment on Union vars
                raise ValueError(f"Invalid type for attribute '{name}'. Expected '{self.__annotations__.get(name)}' but got '{type(value)}'")
        else:
            if hasattr(self, name) and self.__annotations__.get(name) :     # don't allow previously set variables to be set to None
                if getattr(self, name) is not None:                         # unless it is already set to None
                    raise ValueError(f"Can't set None, to a variable that is already set. Invalid type for attribute '{name}'. Expected '{self.__annotations__.get(name)}' but got '{type(value)}'")

        super().__setattr__(name, value)

    def __attr_names__(self):
        return list_set(self.__locals__())

    @classmethod
    def __cls_kwargs__(cls, include_base_classes=True):
        """Return current class dictionary of class level variables and their values."""
        kwargs = {}

        for base_cls in inspect.getmro(cls):
            if base_cls is object:                                                      # Skip the base 'object' class
                continue
            for k, v in vars(base_cls).items():
                # todo: refactor this logic since it is weird to start with a if not..., and then if ... continue (all these should be if ... continue )
                if not k.startswith('__') and not isinstance(v, types.FunctionType):    # remove instance functions
                    if isinstance(v, classmethod):                                      # also remove class methods
                        continue
                    if type(v) is functools._lru_cache_wrapper:                         # todo, find better way to handle edge cases like this one (which happens when the @cache decorator is used in a instance method that uses Kwargs_To_Self)
                        continue
                    if (k in kwargs) is False:                                          # do not set the value is it has already been set
                        kwargs[k] = v

            if hasattr(base_cls,'__annotations__'):  # can only do type safety checks if the class does not have annotations
                for var_name, var_type in base_cls.__annotations__.items():
                    if hasattr(base_cls, var_name) is False:                                # only add if it has not already been defined
                        if var_name in kwargs:
                            continue
                        var_value = cls.__default__value__(var_type)
                        kwargs[var_name] = var_value
                    else:
                        var_value = getattr(base_cls, var_name)
                        if var_value is not None:                                                                   # allow None assignments on ctor since that is a valid use case
                            if var_type and not isinstance(var_value, var_type):                                    # check type
                                exception_message = f"variable '{var_name}' is defined as type '{var_type}' but has value '{var_value}' of type '{type(var_value)}'"
                                raise ValueError(exception_message)
                            if var_type not in immutable_types and var_name.startswith('__') is False:              # if var_type is not one of the immutable_types or is an __ internal
                                #todo: fix type safety bug that I believe is caused here
                                if obj_is_type_union_compatible(var_type, immutable_types) is False:                # if var_type is not something like Optional[Union[int, str]]
                                    if type(var_type) not in immutable_types:
                                        exception_message = f"variable '{var_name}' is defined as type '{var_type}' which is not supported by Kwargs_To_Self, with only the following immutable types being supported: '{immutable_types}'"
                                        raise ValueError(exception_message)
            if include_base_classes is False:
                break
        return kwargs

    @classmethod
    def __default__value__(cls, var_type):
        if var_type is typing.Set:                              # todo: refactor the dict, set and list logic, since they are 90% the same
            return set()
        if get_origin(var_type) is set:
            return set()                                        # todo: add Type_Safe__Set

        if var_type is typing.Dict:
            return {}
        if get_origin(var_type) is dict:
            return {}                                           # todo: add Type_Safe__Dict

        if var_type is typing.List:
            return []  # handle case when List was used with no type information provided
        if get_origin(var_type) is list:                        # if we have list defined as list[type]
            item_type = get_args(var_type)[0]                   #    get the type that was defined
            return Type_Safe__List(expected_type=item_type)     #    and used it as expected_type in Type_Safe__List
        else:
            return default_value(var_type)                      # for all other cases call default_value, which will try to create a default instance

    def __default_kwargs__(self):
        """Return entire (including base classes) dictionary of class level variables and their values."""
        kwargs = {}
        cls = type(self)
        for base_cls in inspect.getmro(cls):                  # Traverse the inheritance hierarchy and collect class-level attributes
            if base_cls is object:  # Skip the base 'object' class
                continue
            for k, v in vars(base_cls).items():
                if not k.startswith('__') and not isinstance(v, types.FunctionType):    # remove instance functions
                    if not isinstance(v, classmethod):
                        kwargs[k] = v
            # add the vars defined with the annotations
            if hasattr(base_cls,'__annotations__'):  # can only do type safety checks if the class does not have annotations
                for var_name, var_type in base_cls.__annotations__.items():
                    var_value        = getattr(self, var_name)
                    kwargs[var_name] = var_value

        return kwargs

    def __kwargs__(self):
        """Return a dictionary of the current instance's attribute values including inherited class defaults."""
        kwargs = {}
        # Update with instance-specific values
        for key, value in self.__default_kwargs__().items():
            kwargs[key] = self.__getattribute__(key)
            # if hasattr(self, key):
            #     kwargs[key] = self.__getattribute__(key)
            # else:
            #     kwargs[key] = value                                   # todo: see if this is stil a valid scenario
        return kwargs


    def __locals__(self):
        """Return a dictionary of the current instance's attribute values."""
        kwargs = self.__kwargs__()

        if not isinstance(vars(self), types.FunctionType):
            for k, v in vars(self).items():
                if not isinstance(v, types.FunctionType) and not isinstance(v,classmethod):
                    if k.startswith('__') is False:
                        kwargs[k] = v
        return kwargs

    @classmethod
    def __schema__(cls):
        if hasattr(cls,'__annotations__'):  # can only do type safety checks if the class does not have annotations
            return cls.__annotations__
        return {}

    # global methods added to any class that base classes this
    # todo: see if there should be a prefix on these methods, to make it easier to spot them
    #       of if these are actually that useful that they should be added like this
    def json(self):
        return self.serialize_to_dict()

    def merge_with(self, target):
        original_attrs = {k: v for k, v in self.__dict__.items() if k not in target.__dict__}       # Store the original attributes of self that should be retained.
        self.__dict__ = target.__dict__                                                             # Set the target's __dict__ to self, now self and target share the same __dict__.
        self.__dict__.update(original_attrs)                                                        # Reassign the original attributes back to self.
        return self

    # def locked(self, value=True):                                   # todo: figure out best way to do this (maybe???)
    #     self.__lock_attributes__ = value                            #     : update, with the latest changes were we don't show internals on __locals__() this might be a good way to do this
    #     return self

    def reset(self):
        for k,v in self.__cls_kwargs__().items():
            setattr(self, k, v)

    def update_from_kwargs(self, **kwargs):
        """Update instance attributes with values from provided keyword arguments."""
        for key, value in kwargs.items():
            if value is not None:
                if hasattr(self,'__annotations__'):  # can only do type safety checks if the class does not have annotations
                    if value_type_matches_obj_annotation_for_attr(self, key, value) is False:
                        raise ValueError(f"Invalid type for attribute '{key}'. Expected '{self.__annotations__.get(key)}' but got '{type(value)}'")
                setattr(self, key, value)
        return self


    def deserialize_from_dict(self, data):
        for key, value in data.items():
            if hasattr(self, key) and isinstance(getattr(self, key), Type_Safe):
                getattr(self, key).deserialize_from_dict(value)                             # Recursive call for complex nested objects
            else:
                if hasattr(self, '__annotations__'):                                        # can only do type safety checks if the class does not have annotations
                    if obj_is_attribute_annotation_of_type(self, key, EnumMeta):            # Handle the case when the value is an Enum
                        enum_type = getattr(self, '__annotations__').get(key)
                        if type(value) is not enum_type:                                    # If the value is not already of the target type
                            value = enum_from_value(enum_type, value)                       # Try to resolve the value into the enum
                    elif obj_is_attribute_annotation_of_type(self, key, Decimal):           # handle Decimals  # todo: refactor these special cases into a separate method to class
                        value = Decimal(value)
                    elif obj_is_attribute_annotation_of_type(self, key, Random_Guid):       # handle Random_Guid objects
                        value = Random_Guid(value)
                setattr(self, key, value)                                                   # Direct assignment for primitive types and other structures

        return self

    def serialize_to_dict(self):                        # todo: see if we need this method or if the .json() is enough
        return serialize_to_dict(self)

    def print(self):
        pprint(serialize_to_dict(self))

    @classmethod
    def from_json(cls, json_data):
        if type(json_data) is str:
            json_data = json_parse(json_data)
        if json_data:                                           # if there is no data or is {} then don't create an object (since this could be caused by bad data being provided)
            return cls().deserialize_from_dict(json_data)
        return None

# todo: see if it is possible to add recursive protection to this logic
def serialize_to_dict(obj):
    if isinstance(obj, (str, int, float, bool, bytes, Decimal)) or obj is None:
        return obj
    elif isinstance(obj, Enum):
        return obj.name
    elif isinstance(obj, list) or isinstance(obj, List):
        return [serialize_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_to_dict(value) for key, value in obj.items()}
    elif hasattr(obj, "__dict__"):
        data = {}                                           # todo: look at a more advanced version which saved the type of the object, for example with {'__type__': type(obj).__name__}
        for key, value in obj.__dict__.items():
            if key.startswith('__') is False:               # don't process internal variables (for example the ones set by @cache_on_self)
                data[key] = serialize_to_dict(value)        # Recursive call for complex types
        return data
    else:
        raise TypeError(f"Type {type(obj)} not serializable")

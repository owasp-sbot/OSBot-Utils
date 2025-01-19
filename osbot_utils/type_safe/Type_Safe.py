# todo: find a way to add these documentations strings to a separate location so that
#       the data is available in IDE's code complete

import sys
import types

from osbot_utils.type_safe.steps.Type_Safe__Step__Default_Kwargs    import type_safe_step_default_kwargs
from osbot_utils.type_safe.steps.Type_Safe__Step__Default_Value     import type_safe_step_default_value
from osbot_utils.type_safe.steps.Type_Safe__Step__Init              import type_safe_step_init
from osbot_utils.type_safe.steps.Type_Safe__Step__Set_Attr          import type_safe_step_set_attr
from osbot_utils.type_safe.Cache__Class_Kwargs                      import cache__class_kwargs

# Backport implementations of get_origin and get_args for Python 3.7
if sys.version_info < (3, 8):                                           # pragma: no cover
    def get_origin(tp):
        import typing
        if isinstance(tp, typing._GenericAlias):
            return tp.__origin__
        elif tp is typing.Generic:
            return typing.Generic
        else:
            return None

    def get_args(tp):
        import typing
        if isinstance(tp, typing._GenericAlias):
            return tp.__args__
        else:
            return ()
else:
    from typing import get_origin, get_args, ForwardRef, Any
    from osbot_utils.helpers.python_compatibility.python_3_8 import Annotated

if sys.version_info >= (3, 10):
    NoneType = types.NoneType
else:                                                           # pragma: no cover
    NoneType = type(None)




#todo: see if we can also add type safety to method execution
#      for example if we have an method like def add_node(self, title: str, call_index: int):
#          throw an exception if the type of the value passed in is not the same as the one defined in the method

class Type_Safe:

    def __init__(self, **kwargs):

        class_kwargs = self.__cls_kwargs__()
        type_safe_step_init.init(self, class_kwargs, **kwargs)


        # from osbot_utils.utils.Objects import raise_exception_on_obj_type_annotation_mismatch
        #
        # for (key, value) in class_kwargs.items():                  # assign all default values to self
        #     if value is not None:                                           # when the value is explicitly set to None on the class static vars, we can't check for type safety
        #         raise_exception_on_obj_type_annotation_mismatch(self, key, value)
        #     if hasattr(self, key):
        #         existing_value = getattr(self, key)
        #         if existing_value is not None:
        #             setattr(self, key, existing_value)
        #             continue
        #     setattr(self, key, value)
        #
        # for (key, value) in kwargs.items():                             # overwrite with values provided in ctor
        #     if hasattr(self, key):
        #         if value is not None:                                   # prevent None values from overwriting existing values, which is quite common in default constructors
        #             setattr(self, key, value)
        #     else:
        #         raise ValueError(f"{self.__class__.__name__} has no attribute '{key}' and cannot be assigned the value '{value}'. "
        #                          f"Use {self.__class__.__name__}.__default_kwargs__() see what attributes are available")

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass


    def __setattr__(self, name, value):
        type_safe_step_set_attr.setattr(super(), self, name, value)

        # from osbot_utils.utils.Objects                  import convert_dict_to_value_from_obj_annotation
        # from osbot_utils.utils.Objects                  import convert_to_value_from_obj_annotation
        # from osbot_utils.utils.Objects                  import value_type_matches_obj_annotation_for_attr
        # from osbot_utils.utils.Objects                  import value_type_matches_obj_annotation_for_union_and_annotated
        # from osbot_utils.type_safe.validators.Type_Safe__Validator import Type_Safe__Validator
        #
        # annotations = all_annotations(self)
        # if not annotations:                                             # can't do type safety checks if the class does not have annotations
        #     return super().__setattr__(name, value)
        #
        # if value is not None:
        #     if type(value) is dict:
        #         value = convert_dict_to_value_from_obj_annotation(self, name, value)
        #     elif type(value) in [int, str]:                                                   # for now only a small number of str and int classes are supported (until we understand the full implications of this)
        #         value = convert_to_value_from_obj_annotation (self, name, value)
        #     else:
        #         origin = get_origin(value)
        #         if origin is not None:
        #             value = origin
        #     check_1 = value_type_matches_obj_annotation_for_attr              (self, name, value)
        #     check_2 = value_type_matches_obj_annotation_for_union_and_annotated(self, name, value)
        #     if (check_1 is False and check_2 is None  or
        #         check_1 is None  and check_2 is False or
        #         check_1 is False and check_2 is False   ):          # fix for type safety assigment on Union vars
        #         raise ValueError(f"Invalid type for attribute '{name}'. Expected '{annotations.get(name)}' but got '{type(value)}'")
        # else:
        #     if hasattr(self, name) and annotations.get(name) :     # don't allow previously set variables to be set to None
        #         if getattr(self, name) is not None:                         # unless it is already set to None
        #             raise ValueError(f"Can't set None, to a variable that is already set. Invalid type for attribute '{name}'. Expected '{self.__annotations__.get(name)}' but got '{type(value)}'")
        #
        # # todo: refactor this to separate method
        # if hasattr(annotations, 'get'):
        #     annotation = annotations.get(name)
        #     if annotation:
        #         annotation_origin = get_origin(annotation)
        #         if annotation_origin is Annotated:
        #             annotation_args = get_args(annotation)
        #             target_type = annotation_args[0]
        #             for attribute in annotation_args[1:]:
        #                 if isinstance(attribute, Type_Safe__Validator):
        #                     attribute.validate(value=value, field_name=name, target_type=target_type)
        #         elif annotation_origin is dict:
        #             value = self.deserialize_dict__using_key_value_annotations(name, value)
        #
        # super().__setattr__(name, value)

    def __attr_names__(self):
        from osbot_utils.utils.Misc import list_set

        return list_set(self.__locals__())

    @classmethod
    def __cls_kwargs__(cls, include_base_classes=True):                  # Return current class dictionary of class level variables and their values
        return cache__class_kwargs.get_cls_kwargs(cls, include_base_classes)

        # import functools
        # import inspect
        # from enum                      import EnumMeta
        # from osbot_utils.utils.Objects import obj_is_type_union_compatible
        #
        # IMMUTABLE_TYPES = (bool, int, float, complex, str, tuple, frozenset, bytes, NoneType, EnumMeta, type)
        #
        #
        # kwargs = {}
        #
        # for base_cls in inspect.getmro(cls):
        #     if base_cls is object:                                                      # Skip the base 'object' class
        #         continue
        #     for k, v in vars(base_cls).items():
        #         # todo: refactor this logic since it is weird to start with a if not..., and then if ... continue (all these should be if ... continue )
        #         if not k.startswith('__') and not isinstance(v, types.FunctionType):    # remove instance functions
        #             if isinstance(v, classmethod):                                      # also remove class methods
        #                 continue
        #             if type(v) is functools._lru_cache_wrapper:                         # todo, find better way to handle edge cases like this one (which happens when the @cache decorator is used in a instance method that uses Kwargs_To_Self)
        #                 continue
        #             if isinstance(v, property):                                         # skip property descriptors since they should not be handled here
        #                 continue
        #             if (k in kwargs) is False:                                          # do not set the value is it has already been set
        #                 kwargs[k] = v
        #
        #     if hasattr(base_cls,'__annotations__'):  # can only do type safety checks if the class does not have annotations
        #         for var_name, var_type in base_cls.__annotations__.items():
        #             if hasattr(base_cls, var_name) is False:                                # only add if it has not already been defined
        #                 if var_name in kwargs:
        #                     continue
        #                 var_value = cls.__default__value__(var_type)
        #                 kwargs[var_name] = var_value
        #             else:
        #                 var_value = getattr(base_cls, var_name)
        #                 if var_value is not None:                                                                   # allow None assignments on ctor since that is a valid use case
        #                     if get_origin(var_type) is Annotated:
        #                         continue
        #                     if get_origin(var_type) is type:  # Special handling for Type[T]
        #                         if not isinstance(var_value, type):
        #                             exception_message = f"variable '{var_name}' is defined as Type[T] but has value '{var_value}' which is not a type"
        #                             raise ValueError(exception_message)
        #                         type_arg = get_args(var_type)[0]
        #                         if not issubclass(var_value, type_arg):
        #                             exception_message = f"variable '{var_name}' is defined as {var_type} but value {var_value} is not a subclass of {type_arg}"
        #                             raise ValueError(exception_message)
        #                     elif var_type and not isinstance(var_value, var_type):                                    # check type
        #                         exception_message = f"variable '{var_name}' is defined as type '{var_type}' but has value '{var_value}' of type '{type(var_value)}'"
        #                         raise ValueError(exception_message)
        #                     if var_type not in IMMUTABLE_TYPES and var_name.startswith('__') is False:              # if var_type is not one of the IMMUTABLE_TYPES or is an __ internal
        #                         #todo: fix type safety bug that I believe is caused here
        #                         if obj_is_type_union_compatible(var_type, IMMUTABLE_TYPES) is False:                # if var_type is not something like Optional[Union[int, str]]
        #                             if type(var_type) not in IMMUTABLE_TYPES:
        #                                 exception_message = f"variable '{var_name}' is defined as type '{var_type}' which is not supported by Type_Safe, with only the following immutable types being supported: '{IMMUTABLE_TYPES}'"
        #                                 raise ValueError(exception_message)
        #     if include_base_classes is False:
        #         break
        # return kwargs

    @classmethod
    def __default__value__(cls, var_type):
        return type_safe_step_default_value.default_value(cls, var_type)

        # import typing
        # from osbot_utils.type_safe.Type_Safe__List import Type_Safe__List
        # from osbot_utils.type_safe.Type_Safe__Dict import Type_Safe__Dict
        # if get_origin(var_type) is type:                        # Special handling for Type[T]  # todo: reuse the get_origin value
        #     type_args = get_args(var_type)
        #     if type_args:
        #         if isinstance(type_args[0], ForwardRef):
        #             forward_name = type_args[0].__forward_arg__
        #             for base_cls in inspect.getmro(cls):
        #                 if base_cls.__name__ == forward_name:
        #                     return cls                                                      # note: in this case we return the cls, and not the base_cls (which makes sense since this happens when the cls class uses base_cls as base, which has a ForwardRef to base_cls )
        #         return type_args[0]                             # Return the actual type as the default value
        #
        # if var_type is typing.Set:                              # todo: refactor the dict, set and list logic, since they are 90% the same
        #     return set()
        # if get_origin(var_type) is set:
        #     return set()                                        # todo: add Type_Safe__Set
        #
        # if var_type is typing.Dict:
        #     return {}
        #
        # if get_origin(var_type) is dict:                        # e.g. Dict[key_type, value_type]
        #     key_type, value_type = get_args(var_type)
        #     if isinstance(key_type, ForwardRef):                # Handle forward references on key_type ---
        #         forward_name = key_type.__forward_arg__
        #         if forward_name == cls.__name__:
        #             key_type = cls
        #     if isinstance(value_type, ForwardRef):              # Handle forward references on value_type ---
        #         forward_name = value_type.__forward_arg__
        #         if forward_name == cls.__name__:
        #             value_type = cls
        #     return Type_Safe__Dict(expected_key_type=key_type, expected_value_type=value_type)
        #
        # if var_type is typing.List:
        #     return []                                           # handle case when List was used with no type information provided
        #
        # if get_origin(var_type) is list:                        # if we have list defined as list[type]
        #     item_type = get_args(var_type)[0]                   #    get the type that was defined
        #     if isinstance(item_type, ForwardRef):               # handle the case when the type is a forward reference
        #         forward_name = item_type.__forward_arg__
        #         if forward_name == cls.__name__:                #    if the forward reference is to the current class (simple name check)
        #             item_type = cls                             #       set the item_type to the current class
        #     return Type_Safe__List(expected_type=item_type)     #    and used it as expected_type in Type_Safe__List
        # else:
        #     return default_value(var_type)                      # for all other cases call default_value, which will try to create a default instance

    def __default_kwargs__(self):                               # Return entire (including base classes) dictionary of class level variables and their values.
        return type_safe_step_default_kwargs.default_kwargs(self)
        # import inspect
        # kwargs = {}
        # cls = type(self)
        # for base_cls in inspect.getmro(cls):                  # Traverse the inheritance hierarchy and collect class-level attributes
        #     if base_cls is object:  # Skip the base 'object' class
        #         continue
        #     for k, v in vars(base_cls).items():
        #         if not k.startswith('__') and not isinstance(v, types.FunctionType):    # remove instance functions
        #             if not isinstance(v, classmethod):
        #                 kwargs[k] = v
        #     # add the vars defined with the annotations
        #     if hasattr(base_cls,'__annotations__'):  # can only do type safety checks if the class does not have annotations
        #         for var_name, var_type in base_cls.__annotations__.items():
        #             var_value        = getattr(self, var_name)
        #             kwargs[var_name] = var_value
        #
        # return kwargs

    def __kwargs__(self):                                   # Return a dictionary of the current instance's attribute values including inherited class defaults.
        return type_safe_step_default_kwargs.kwargs(self)
        # kwargs = {}
        # # Update with instance-specific values
        # for key, value in self.__default_kwargs__().items():
        #     kwargs[key] = self.__getattribute__(key)
        # return kwargs


    def __locals__(self):
        return type_safe_step_default_kwargs.locals(self)
        """Return a dictionary of the current instance's attribute values."""
        # kwargs = self.__kwargs__()
        #
        # if not isinstance(vars(self), types.FunctionType):
        #     for k, v in vars(self).items():
        #         if not isinstance(v, types.FunctionType) and not isinstance(v,classmethod):
        #             if k.startswith('__') is False:
        #                 kwargs[k] = v
        #return kwargs

    @classmethod
    def __schema__(cls):
        if hasattr(cls,'__annotations__'):  # can only do type safety checks if the class does not have annotations
            return cls.__annotations__
        return {}

    # global methods added to any class that base classes this
    # todo: see if there should be a prefix on these methods, to make it easier to spot them
    #       of if these are actually that useful that they should be added like this
    def bytes(self):
        from osbot_utils.utils.Json import json_to_bytes

        return json_to_bytes(self.json())

    def bytes_gz(self):
        from osbot_utils.utils.Json import json_to_gz

        return json_to_gz(self.json())

    def json(self):
        return self.serialize_to_dict()


    # todo: see if we still need this. now that Type_Safe handles base types, there should be no need for this
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

    # todo: see if we still need this here in this class
    def update_from_kwargs(self, **kwargs):                         # Update instance attributes with values from provided keyword arguments.
        from osbot_utils.utils.Objects import value_type_matches_obj_annotation_for_attr
        for key, value in kwargs.items():
            if value is not None:
                if hasattr(self,'__annotations__'):  # can only do type safety checks if the class does not have annotations
                    if value_type_matches_obj_annotation_for_attr(self, key, value) is False:
                        raise ValueError(f"Invalid type for attribute '{key}'. Expected '{self.__annotations__.get(key)}' but got '{type(value)}'")
                setattr(self, key, value)
        return self



    def obj(self):
        from osbot_utils.utils.Objects import dict_to_obj

        return dict_to_obj(self.json())

    def serialize_to_dict(self):                        # todo: see if we need this method or if the .json() is enough
        return serialize_to_dict(self)

    def print(self):
        from osbot_utils.utils.Dev import pprint

        pprint(serialize_to_dict(self))

    @classmethod
    def from_json(cls, json_data, raise_on_not_found=False):
        from osbot_utils.type_safe.steps.Type_Safe__Step__From_Json import type_safe_step_from_json     # circular dependency on Type_Safe
        return type_safe_step_from_json.from_json(cls, json_data, raise_on_not_found)

        # from osbot_utils.utils.Json import json_parse
        #
        # if type(json_data) is str:
        #     json_data = json_parse(json_data)
        # if json_data:                                           # if there is no data or is {} then don't create an object (since this could be caused by bad data being provided)
        #     return cls().deserialize_from_dict(json_data,raise_on_not_found=raise_on_not_found)
        # return cls()

# todo: see if it is possible to add recursive protection to this logic
def serialize_to_dict(obj):
    from decimal import Decimal
    from enum    import Enum
    from typing  import List

    if isinstance(obj, (str, int, float, bool, bytes, Decimal)) or obj is None:
        return obj
    elif isinstance(obj, Enum):
        return obj.name
    elif isinstance(obj, type):
        return f"{obj.__module__}.{obj.__name__}"                                   # save the full type name
    elif isinstance(obj, list) or isinstance(obj, List):
        return [serialize_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_to_dict(value) for key, value in obj.items()}
    elif hasattr(obj, "__dict__"):
        data = {}                                                                   # todo: look at a more advanced version which saved the type of the object, for example with {'__type__': type(obj).__name__}
        for key, value in obj.__dict__.items():
            if key.startswith('__') is False:                                       # don't process internal variables (for example the ones set by @cache_on_self)
                data[key] = serialize_to_dict(value)                                # Recursive call for complex types
        return data
    else:
        raise TypeError(f"Type {type(obj)} not serializable")
        #return f"UNSERIALIZABLE({type(obj).__name__})"             # todo: see if there are valid use cases for this


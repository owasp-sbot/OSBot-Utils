import sys
import types
from decimal                                             import Decimal
from enum                                                import EnumMeta
from osbot_utils.helpers.Obj_Id                          import Obj_Id
from osbot_utils.helpers.safe_str.Safe_Str__Hash         import Safe_Str__Hash
from osbot_utils.type_safe.Type_Safe                     import Type_Safe
from osbot_utils.type_safe.Type_Safe__List               import Type_Safe__List
from osbot_utils.helpers.Random_Guid                     import Random_Guid
from osbot_utils.helpers.Random_Guid_Short               import Random_Guid_Short
from osbot_utils.type_safe.Type_Safe__Set                import Type_Safe__Set
from osbot_utils.type_safe.shared.Type_Safe__Annotations import type_safe_annotations
from osbot_utils.type_safe.shared.Type_Safe__Cache       import type_safe_cache
from osbot_utils.type_safe.shared.Type_Safe__Convert     import type_safe_convert
from osbot_utils.utils.Objects                           import enum_from_value
from osbot_utils.helpers.Safe_Id                         import Safe_Id
from osbot_utils.helpers.Timestamp_Now                   import Timestamp_Now

# todo; refactor all this python compatibility into the python_3_8 class
if sys.version_info < (3, 8):                                           # pragma: no cover

    def get_args(tp):
        import typing
        if isinstance(tp, typing._GenericAlias):
            return tp.__args__
        else:
            return ()
else:
    from typing import get_args, Any


class Type_Safe__Step__From_Json:

    # todo: this needs refactoring, since the logic and code is getting quite complex (to be inside methods like this)
    def deserialize_from_dict(self, _self, data, raise_on_not_found=False):

        if hasattr(data, 'items') is False:
            raise ValueError(f"Expected a dictionary, but got '{type(data)}'")

        for key, value in data.items():
            if hasattr(_self, key) and isinstance(getattr(_self, key), Type_Safe):
                self.deserialize_from_dict(getattr(_self, key), value)                                             # if the attribute is a Type_Safe object, then also deserialize it
            else:
                if hasattr(_self, '__annotations__'):                                                        # can only do type safety checks if the class does not have annotations
                    if hasattr(_self, key) is False:                                                         # make sure we are now adding new attributes to the class
                        if raise_on_not_found:
                            raise ValueError(f"Attribute '{key}' not found in '{_self.__class__.__name__}'")
                        else:
                            continue
                    annotation        = type_safe_annotations.obj_attribute_annotation(_self, key)
                    annotation_origin = type_safe_cache.get_origin(annotation)


                    if annotation == type:                                                  # Handle type objects
                        value = self.deserialize_type__using_value(value)
                    elif annotation_origin == type:                                         # Handle type objects inside ForwardRef
                        value = self.deserialize_type__using_value(value)
                    if annotation_origin is tuple and isinstance(value, list):
                        # item_types = get_args(annotation)   # todo: see if we should do type safety here
                        value = tuple(value)
                    elif type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, dict):                                # handle the case when the value is a dict
                        value = self.deserialize_dict__using_key_value_annotations(_self, key, value)
                    elif type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, set):                              # handle the case when the value is a list
                        attribute_annotation = type_safe_annotations.obj_attribute_annotation(_self, key)                          # get the annotation for this variable
                        attribute_annotation_args = get_args(attribute_annotation)
                        if attribute_annotation_args:
                            expected_type        = get_args(attribute_annotation)[0]                            # get the first arg (which is the type)
                            type_safe_set        = Type_Safe__Set(expected_type)                               # create a new instance of Type_Safe__List
                            for item in value:                                                                  # next we need to convert all items (to make sure they all match the type)
                                if type(item) is dict:
                                    new_item = expected_type(**item)                                                # create new object
                                else:
                                    new_item = expected_type(item)
                                type_safe_set.add(new_item)                                                 # and add it to the new type_safe_list obejct
                            value = type_safe_set                                                              # todo: refactor out this create list code, maybe to an deserialize_from_list method
                    elif type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, list):                              # handle the case when the value is a list
                        attribute_annotation = type_safe_annotations.obj_attribute_annotation(_self, key)                          # get the annotation for this variable
                        attribute_annotation_args = get_args(attribute_annotation)
                        if attribute_annotation_args:
                            expected_type        = get_args(attribute_annotation)[0]                            # get the first arg (which is the type)
                            type_safe_list       = Type_Safe__List(expected_type)                               # create a new instance of Type_Safe__List
                            for item in value:                                                                  # next we need to convert all items (to make sure they all match the type)
                                if type(item) is dict:
                                    new_item = expected_type(**item)                                                # create new object
                                else:
                                    new_item = expected_type(item)
                                type_safe_list.append(new_item)                                                 # and add it to the new type_safe_list obejct
                            value = type_safe_list                                                              # todo: refactor out this create list code, maybe to an deserialize_from_list method
                    else:
                        if value is not None:
                            if type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, EnumMeta):            # Handle the case when the value is an Enum
                                enum_type = getattr(_self, '__annotations__').get(key)
                                if type(value) is not enum_type:                                    # If the value is not already of the target type
                                    value = enum_from_value(enum_type, value)                       # Try to resolve the value into the enum

                            # todo: refactor these special cases into a separate method to class
                            #       in fact find a better way to handle these classes that need to be converted
                            elif type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, Decimal):           # handle Decimals
                                value = Decimal(value)
                            elif type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, Safe_Id):           # handle Safe_Id
                                value = Safe_Id(value)
                            elif type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, Random_Guid):       # handle Random_Guid
                                value = Random_Guid(value)
                            elif type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, Random_Guid_Short): # handle Random_Guid_Short
                                value = Random_Guid_Short(value)
                            elif type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, Timestamp_Now    ): # handle Timestamp_Now
                                value = Timestamp_Now(value)
                            elif type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, Obj_Id           ): # handle Obj_Id
                                value = Obj_Id(value)
                            elif type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, Safe_Str__Hash   ): # handle Obj_Id
                                value = Safe_Str__Hash(value)
                            # else:
                            #     from osbot_utils.utils.Dev import pprint
                            #     pprint(value)


                    setattr(_self, key, value)                                                   # Direct assignment for primitive types and other structures

        return _self

    def deserialize_type__using_value(self, value):         # TODO: Check the security implications of this deserialisation
        if value:
            try:
                module_name, type_name = value.rsplit('.', 1)
                if module_name == 'builtins' and type_name == 'NoneType':                       # Special case for NoneType (which serialises as builtins.* , but it actually in types.* )
                    value = types.NoneType
                else:
                    module = __import__(module_name, fromlist=[type_name])
                    value = getattr(module, type_name)
                    if isinstance(value, type) is False:
                        raise ValueError(f"Security alert, in deserialize_type__using_value only classes are allowed")

                    # todo: figure out a way to do this
                    # supported_types = (Type_Safe, str, int, type, dict)
                    # if issubclass(value, supported_types)  is False:
                    #     raise ValueError(f"Security alert, in deserialize_type__using_value only class of {supported_types} are allowed and it was {value}")

            except (ValueError, ImportError, AttributeError) as e:
                raise ValueError(f"Could not reconstruct type from '{value}': {str(e)}")
        return value

    def deserialize_dict__using_key_value_annotations(self, _self, key, value):
        from osbot_utils.type_safe.Type_Safe__Dict import Type_Safe__Dict

        annotations            = type_safe_cache.get_obj_annotations(_self)
        dict_annotations_tuple = get_args(annotations.get(key))
        if not dict_annotations_tuple:                                      # happens when the value is a dict/Dict with no annotations
            return value
        if not type(value) is dict:
            return value
        key_class   = dict_annotations_tuple[0]
        value_class = dict_annotations_tuple[1]
        new_value   = Type_Safe__Dict(expected_key_type=key_class, expected_value_type=value_class)

        for dict_key, dict_value in value.items():
            key_origin = type_safe_cache.get_origin(key_class)
            if key_origin is type:
                if type(dict_key) is str:
                    dict_key = self.deserialize_type__using_value(dict_key)
                key_class_args = get_args(key_class)
                if key_class_args:
                    expected_dict_type = key_class_args[0]
                    if dict_key != expected_dict_type and not issubclass(dict_key,expected_dict_type):
                        raise TypeError(f"Expected {expected_dict_type} class for key but got instance: {dict_key}")
                else:
                    if not isinstance(dict_key, key_class):
                        raise TypeError(f"Expected {key_class} class for key but got instance: {dict_key}")
                new__dict_key = dict_key
            elif issubclass(key_class, Type_Safe):
                new__dict_key = self.deserialize_from_dict(key_class(), dict_key)
            else:
                new__dict_key = key_class(dict_key)

            if type(dict_value) == value_class:                                        # if the value is already the target, then just use it
                new__dict_value = dict_value
            elif isinstance(value_class, type) and issubclass(value_class, Type_Safe):
                if 'node_type' in dict_value:
                    value_class = type_safe_convert.get_class_from_class_name(dict_value['node_type'])

                new__dict_value = self.deserialize_from_dict(value_class(), dict_value)
            elif value_class is Any:
                new__dict_value = dict_value
            else:
                new__dict_value = value_class(dict_value)
            new_value[new__dict_key] = new__dict_value

        return new_value

    def from_json(self, _cls, json_data, raise_on_not_found=False):
        from osbot_utils.utils.Json import json_parse

        if type(json_data) is str:
            json_data = json_parse(json_data)
        if json_data:                                           # if there is no data or is {} then don't create an object (since this could be caused by bad data being provided)
            return self.deserialize_from_dict(_cls(), json_data, raise_on_not_found=raise_on_not_found)
        return _cls()

type_safe_step_from_json = Type_Safe__Step__From_Json()
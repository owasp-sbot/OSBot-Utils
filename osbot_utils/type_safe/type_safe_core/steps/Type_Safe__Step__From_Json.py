from decimal                                                                        import Decimal
from osbot_utils.type_safe.Type_Safe__Primitive                                     import Type_Safe__Primitive
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List               import Type_Safe__List
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set                import Type_Safe__Set
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Tuple              import Type_Safe__Tuple
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Annotations             import type_safe_annotations
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Cache                   import type_safe_cache
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Convert                 import type_safe_convert
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__Deserialize_Type   import type_safe_step_deserialize_type
from osbot_utils.utils.Objects                                                      import enum_from_value
from typing                                                                         import get_args, Any, ForwardRef, Union, Type


class Type_Safe__Step__From_Json:

    def deserialize_from_dict(self, _self, data, raise_on_not_found=False):
        if data is None:
            return None
        if hasattr(data, 'items') is False:
            raise ValueError(f"Expected a dictionary, but got '{type(data)}'")

        for key, value in data.items():
            if hasattr(_self, key) and isinstance(getattr(_self, key), Type_Safe):
                self.deserialize_from_dict(getattr(_self, key), value)
            else:
                if hasattr(_self, '__annotations__'):
                    if hasattr(_self, key) is False:
                        if raise_on_not_found:
                            raise ValueError(f"Attribute '{key}' not found in '{_self.__class__.__name__}'")
                        else:
                            continue

                    value = self.deserialize_attribute(_self, key, value)
                    setattr(_self, key, value)

        return _self

    def deserialize_attribute(self, _self, key, value):                                     # Deserialize a single attribute based on its annotation.
        annotation        = type_safe_annotations.obj_attribute_annotation(_self, key)
        annotation_origin = type_safe_cache.get_origin(annotation)

        if annotation_origin is Union and isinstance(value, str):
            args = get_args(annotation)
            if len(args) == 2 and type(None) in args:                               # It's Optional
                non_none_type = next(arg for arg in args if arg is not type(None))
                if non_none_type is Type:                                           # Optional[Type]
                    return self.deserialize_type__using_value(value)

        if value is not None and type(value) is dict:                                       # Handle forward references first

            if isinstance(annotation, type) and issubclass(annotation, Type_Safe__Dict):                            # Handle Type_Safe__Dict subclasses BEFORE forward references
                if hasattr(annotation, 'expected_key_type') and hasattr(annotation, 'expected_value_type'):         # Get the expected types from the subclass
                    if annotation.expected_key_type and annotation.expected_value_type:
                        dict_instance = annotation(value)                                                           # Create instance and populate it
                        return dict_instance
            forward_ref_result = self.handle_forward_references(_self, annotation, value)
            if forward_ref_result is not None:
                return forward_ref_result

        if annotation == type:                                                              # Handle type objects
            return self.deserialize_type__using_value(value)
        elif annotation_origin == type:
            return self.deserialize_type__using_value(value)

        # Handle collections
        if annotation_origin is tuple and isinstance(value, list):                          return self.handle_tuple_annotation                      (annotation, value)
        elif type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, dict):   return self.deserialize_dict__using_key_value_annotations(_self, key, value)
        elif type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, set):    return self.handle_set_annotation                        (_self, key, value)
        elif type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, list):   return self.handle_list_annotation                       (_self, key, value)

        # Handle special types and enums
        if value is not None:
            return self.handle_special_types(_self, key, annotation, value)

        return value

    def handle_forward_references(self, _self, annotation, value):                          # Handle forward references to Type_Safe classes.
        if isinstance(annotation, str):                                                     # String forward references
            if annotation == _self.__class__.__name__:
                return _self.__class__.from_json(value)
            return None                                                                     # todo: should we add logic here to resolve other forward refs if needed

        if isinstance(annotation, ForwardRef):                                              # ForwardRef objects from typing
            forward_name = annotation.__forward_arg__
            if forward_name == _self.__class__.__name__:
                return _self.__class__.from_json(value)
            return None

        if type(annotation) is type and issubclass(annotation, Type_Safe):                  # Type_Safe subclasses
            return annotation.from_json(value)

        return None

    def handle_tuple_annotation(self, annotation, value):                                   # Handle tuple type annotations.
        item_types = get_args(annotation)
        if item_types:
            return Type_Safe__Tuple(expected_types=item_types, items=value)
        else:
            return tuple(value)

    def handle_set_annotation(self, _self, key, value):                                     # Handle set type annotations.
        if value is None:
            return None
        attribute_annotation      = type_safe_annotations.obj_attribute_annotation(_self, key)
        attribute_annotation_args = get_args(attribute_annotation)

        if attribute_annotation_args:
            expected_type = attribute_annotation_args[0]
            type_safe_set = Type_Safe__Set(expected_type)

            for item in value:
                new_item = self.convert_item_to_type(expected_type, item)
                type_safe_set.add(new_item)

            return type_safe_set

        return set(value)

    def handle_list_annotation(self, _self, key, value):                                    # Handle list type annotations.
        if value is None:  # <-- Add this check
            return None
        attribute_annotation      = type_safe_annotations.obj_attribute_annotation(_self, key)
        attribute_annotation_args = get_args(attribute_annotation)

        if attribute_annotation_args:
            expected_type = attribute_annotation_args[0]

            if type_safe_cache.get_origin(expected_type) is dict:                           # Special handling for Dict from typing
                type_safe_list = Type_Safe__List(dict)
                if value:
                    for item in value:
                        type_safe_list.append(item)
                return type_safe_list

            type_safe_list = Type_Safe__List(expected_type)                                 # Regular list handling

            if value:                                                                       # Handle forward refs in lists
                if isinstance(expected_type, ForwardRef):
                    forward_name = expected_type.__forward_arg__
                    if forward_name == _self.__class__.__name__:
                        expected_type = _self.__class__

                for item in value:
                    new_item = self.convert_item_to_type(expected_type, item)
                    type_safe_list.append(new_item)

            return type_safe_list

        return list(value) if value else []

    def convert_item_to_type(self, expected_type, item):                                    # Convert a single item to the expected type.
        if type(item) is dict:
            if hasattr(expected_type, 'from_json'):                                         # Check if it's a Type_Safe class that can be instantiated from dict
                return expected_type.from_json(item)
            else:
                return expected_type(**item)
        else:
            return expected_type(item)

    def handle_special_types(self, _self, key, annotation, value):                          # Handle special types like enums and Type_Safe__Primitive subclasses."""
        enum_type = type_safe_annotations.extract_enum_from_annotation(annotation)          # Handle enums
        if enum_type:
            if type(value) is not enum_type:
                return enum_from_value(enum_type, value)
            return value



        if type(annotation) is type:                                                                # Check if the annotation is a Type_Safe__Primitive subclass

            if issubclass(annotation, Type_Safe__Primitive):                                        # Handle Type_Safe__Primitive subclasses generically
                return annotation(value)                                                            # Type_Safe__Primitive classes can be instantiated with their value

        if type_safe_annotations.obj_is_attribute_annotation_of_type(_self, key, Decimal):          # Handle Decimal as a special case (not a Type_Safe__Primitive)
            return Decimal(value)

        return value

    def deserialize_dict__using_key_value_annotations(self, _self, key, value):
        annotations            = type_safe_cache.get_obj_annotations(_self)
        dict_annotations_tuple = get_args(annotations.get(key))
        if not dict_annotations_tuple:
            return value
        if not type(value) is dict:
            return value

        key_class   = dict_annotations_tuple[0]
        value_class = dict_annotations_tuple[1]

        if isinstance(value_class, ForwardRef):                                 # Resolve forward references in value_class
            forward_name = value_class.__forward_arg__
            if forward_name == _self.__class__.__name__:
                value_class = _self.__class__
            else:
                pass                                                            # Can't resolve other forward refs easily (Would need to search in the module's namespace)
        elif isinstance(value_class, str):
            if value_class == _self.__class__.__name__:
                value_class = _self.__class__

        new_value = Type_Safe__Dict(expected_key_type=key_class, expected_value_type=value_class)

        for dict_key, dict_value in value.items():
            new__dict_key   = self.deserialize_dict_key(key_class, dict_key)
            new__dict_value = self.deserialize_dict_value(_self, value_class, dict_value)
            new_value[new__dict_key] = new__dict_value

        return new_value

    def deserialize_dict_key(self, key_class, dict_key):                # Deserialize a dictionary key based on its expected type.
        key_origin = type_safe_cache.get_origin(key_class)

        if key_origin is type:
            return self.deserialize_type_key(key_class, dict_key)
        elif issubclass(key_class, Type_Safe):
            return self.deserialize_from_dict(key_class(), dict_key)
        else:
            return key_class(dict_key)

    def deserialize_type_key(self, key_class, dict_key):                # Handle deserialization of Type[T] keys.
        if type(dict_key) is str:
            dict_key = self.deserialize_type__using_value(dict_key)

        key_class_args = get_args(key_class)
        if key_class_args:
            expected_dict_type = key_class_args[0]
            if dict_key != expected_dict_type and not issubclass(dict_key, expected_dict_type):
                raise TypeError(f"Expected {expected_dict_type} class for key but got instance: {dict_key}")
        else:
            if not isinstance(dict_key, key_class):
                raise TypeError(f"Expected {key_class} class for key but got instance: {dict_key}")

        return dict_key

    def deserialize_dict_value(self, _self, value_class, dict_value):                      # Deserialize a dictionary value based on its expected type.
        value_origin = type_safe_cache.get_origin(value_class)

        if value_origin is list:                                                    # This handles both typing.List and list
            return self.deserialize_list_in_dict_value(_self, value_class, dict_value)

        if value_origin is dict:                                                    # Handle Dict[K, V] type annotations
            return self.deserialize_nested_dict(value_class, dict_value)

        elif type(dict_value) == value_class:                                       # Value is already the correct type
            return dict_value

        elif isinstance(value_class, type) and issubclass(value_class, Type_Safe):  # Handle Type_Safe subclasses
            return self.deserialize_type_safe_value(value_class, dict_value)

        elif value_class is Any:                                                    # Handle Any type
            return dict_value

        if isinstance(value_class, ForwardRef):                                     # Handle ForwardRef in dict values
            return dict_value                                                       # For now, we can't easily resolve forward refs without context (This would need the class context to resolve properly)

        if value_origin is dict:                                                    # Handle Dict[K, V] type annotations (use lowercase dict, not Dict)
            return self.deserialize_nested_dict(value_class, dict_value)
        if value_origin is tuple:
             return tuple(dict_value)                                               # typing.Tuple cannot be invoked, so we need to use the tuple
        else:                                                                       # Default: try to instantiate with the value
            return value_class(dict_value)

    def deserialize_list_in_dict_value(self, _self, value_class, dict_value):              # Handle List[T] or list[T] types when they appear as dictionary values.
        if not isinstance(dict_value, list):
            return dict_value

        args = get_args(value_class)
        if not args:
            return dict_value                                                                       # No type info, return as-is

        item_type = args[0]

        if isinstance(item_type, ForwardRef):                                                       # Handle forward references with _self context
            if _self:
                forward_name = item_type.__forward_arg__
                if forward_name == _self.__class__.__name__:
                    item_type = _self.__class__

        type_safe_list = Type_Safe__List(item_type)

        for item in dict_value:                                                                     # Handle Type_Safe subclasses
            if isinstance(item_type, type) and issubclass(item_type, Type_Safe):
                if isinstance(item, dict):
                    type_safe_list.append(item_type.from_json(item))
                else:
                    type_safe_list.append(item)
            elif isinstance(item_type, type) and issubclass(item_type, Type_Safe__Primitive):       # Handle Type_Safe__Primitive subclasses (like Safe_Str__File__Path)
                type_safe_list.append(item_type(item))
            else:
                type_safe_list.append(item)

        return type_safe_list

    def deserialize_nested_dict(self, value_class, dict_value):                     # Handle deserialization of nested Dict[K, V] types.
        if not isinstance(dict_value, dict):
            return dict_value

        nested_args = get_args(value_class)
        if nested_args and len(nested_args) == 2:
            nested_key_type, nested_value_type = nested_args
            nested_dict = Type_Safe__Dict(expected_key_type=nested_key_type,
                                         expected_value_type=nested_value_type)
            for nk, nv in dict_value.items():
                nested_dict[nk] = nv
            return nested_dict
        else:
            return dict_value  # No type info, use raw dict

    def deserialize_type_safe_value(self, value_class, dict_value):                         # Handle deserialization of Type_Safe subclass values.
        if 'node_type' in dict_value:
            value_class = type_safe_convert.get_class_from_class_name(dict_value['node_type'])

        return self.deserialize_from_dict(value_class(), dict_value)

    def from_json(self, _cls, json_data, raise_on_not_found=False):
        from osbot_utils.utils.Json import json_parse

        if type(json_data) is str:
            json_data = json_parse(json_data)
        if json_data:                                           # if there is no data or is {} then don't create an object (since this could be caused by bad data being provided)
            return self.deserialize_from_dict(_cls(), json_data, raise_on_not_found=raise_on_not_found)
        return _cls()

    def deserialize_type__using_value(self, value):
        return type_safe_step_deserialize_type.using_value(value)


type_safe_step_from_json = Type_Safe__Step__From_Json()
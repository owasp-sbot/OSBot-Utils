# Type_Safe Class Documentation

This document provides a comprehensive analysis of the Type_Safe class, its methods, behaviors, and relationships. The class implements type safety mechanisms for Python objects through runtime type checking and validation.

## Table of Contents
1. [Class Overview](#class-overview)
2. [Core Methods](#core-methods)
3. [Utility Methods](#utility-methods)
4. [Serialization Methods](#serialization-methods)
5. [Helper Methods](#helper-methods)

## Class Overview

The Type_Safe class is a base class that provides type safety mechanisms for Python objects. It enforces type checking through annotations and provides utilities for serialization, deserialization, and object manipulation.

## Core Methods

### __init__

The constructor method implements type-safe initialization for class instances.

```python
def __init__(self, **kwargs):
    from osbot_utils.utils.Objects import raise_exception_on_obj_type_annotation_mismatch

    for (key, value) in self.__cls_kwargs__().items():                  
        if value is not None:                                           
            raise_exception_on_obj_type_annotation_mismatch(self, key, value)
        if hasattr(self, key):
            existing_value = getattr(self, key)
            if existing_value is not None:
                setattr(self, key, existing_value)
                continue
        setattr(self, key, value)

    for (key, value) in kwargs.items():                             
        if hasattr(self, key):
            if value is not None:                                   
                setattr(self, key, value)
        else:
            raise ValueError(f"{self.__class__.__name__} has no attribute '{key}' and cannot be assigned the value '{value}'. "
                             f"Use {self.__class__.__name__}.__default_kwargs__() see what attributes are available")
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
|               | `**kwargs` | `dict` | Variable keyword arguments for initialization | `{}` |
| **Returns**    | None | `None` | Constructor doesn't return a value | N/A |
| **Raises**     | `ValueError` | `Exception` | When invalid attribute name or type mismatch occurs | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `__cls_kwargs__()` | Gets class-level attributes |
|              | `raise_exception_on_obj_type_annotation_mismatch()` | Validates type safety |
|              | `hasattr()` | Checks attribute existence |
|              | `getattr()` | Gets attribute values |
|              | `setattr()` | Sets attribute values |
| **Called By**| Instance creation | During object instantiation |
|              | `from_json()` | When creating instance from JSON |

### __setattr__

The attribute setter method enforces type checking and validation for all attribute assignments.

```python
def __setattr__(self, name, value):
    from osbot_utils.utils.Objects import (convert_dict_to_value_from_obj_annotation,
                                         convert_to_value_from_obj_annotation,
                                         value_type_matches_obj_annotation_for_attr,
                                         value_type_matches_obj_annotation_for_union_and_annotated)
    from osbot_utils.type_safe.validators.Type_Safe__Validator import Type_Safe__Validator

    annotations = all_annotations(self)
    if not annotations:
        return super().__setattr__(name, value)

    if value is not None:
        if type(value) is dict:
            value = convert_dict_to_value_from_obj_annotation(self, name, value)
        elif type(value) in [int, str]:
            value = convert_to_value_from_obj_annotation(self, name, value)
        else:
            origin = get_origin(value)
            if origin is not None:
                value = origin

        check_1 = value_type_matches_obj_annotation_for_attr(self, name, value)
        check_2 = value_type_matches_obj_annotation_for_union_and_annotated(self, name, value)
        
        if (check_1 is False and check_2 is None or
            check_1 is None and check_2 is False or
            check_1 is False and check_2 is False):
            raise ValueError(f"Invalid type for attribute '{name}'. Expected '{annotations.get(name)}' but got '{type(value)}'")
    else:
        if hasattr(self, name) and annotations.get(name):
            if getattr(self, name) is not None:
                raise ValueError(f"Can't set None to a variable that is already set. Invalid type for attribute '{name}'. Expected '{self.__annotations__.get(name)}' but got '{type(value)}'")

    if hasattr(annotations, 'get'):
        annotation = annotations.get(name)
        if annotation:
            annotation_origin = get_origin(annotation)
            if annotation_origin is Annotated:
                annotation_args = get_args(annotation)
                target_type = annotation_args[0]
                for attribute in annotation_args[1:]:
                    if isinstance(attribute, Type_Safe__Validator):
                        attribute.validate(value=value, field_name=name, target_type=target_type)
            elif annotation_origin is dict:
                value = self.deserialize_dict__using_key_value_annotations(name, value)

    super().__setattr__(name, value)
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
|               | `name` | `str` | Attribute name | N/A |
|               | `value` | `Any` | Value to set | N/A |
| **Returns**    | None | `None` | Setter doesn't return a value | N/A |
| **Raises**     | `ValueError` | `Exception` | On type mismatch or validation failure | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `all_annotations()` | Gets all class annotations |
|              | `convert_dict_to_value_from_obj_annotation()` | Converts dict values |
|              | `convert_to_value_from_obj_annotation()` | Converts primitive values |
|              | `value_type_matches_obj_annotation_for_attr()` | Validates type matching |
|              | `value_type_matches_obj_annotation_for_union_and_annotated()` | Validates union types |
|              | `get_origin()` | Gets type hint origin |
|              | `get_args()` | Gets type hint arguments |
|              | `deserialize_dict__using_key_value_annotations()` | Processes dict annotations |
| **Called By**| Any attribute assignment | During any attribute setting |
|              | Most class methods | When modifying object state |

### __attr_names__

Returns a list of all attribute names in the instance.

```python
def __attr_names__(self):
    from osbot_utils.utils.Misc import list_set
    return list_set(self.__locals__())
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
| **Returns**    | `list` | `List[str]` | List of unique attribute names | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `__locals__()` | Gets local attributes |
|              | `list_set()` | Converts to unique list |
| **Called By**| Object inspection | When examining object attributes |

### __cls_kwargs__

Returns a dictionary of class-level variables and their values, including those from base classes.

```python
@classmethod
def __cls_kwargs__(cls, include_base_classes=True):
    import functools
    import inspect
    from enum import EnumMeta
    from osbot_utils.utils.Objects import obj_is_type_union_compatible

    IMMUTABLE_TYPES = (bool, int, float, complex, str, tuple, frozenset, bytes, NoneType, EnumMeta, type)

    kwargs = {}
    
    for base_cls in inspect.getmro(cls):
        if base_cls is object:
            continue
        for k, v in vars(base_cls).items():
            if not k.startswith('__') and not isinstance(v, types.FunctionType):
                if isinstance(v, classmethod):
                    continue
                if type(v) is functools._lru_cache_wrapper:
                    continue
                if isinstance(v, property):
                    continue
                if (k in kwargs) is False:
                    kwargs[k] = v

        if hasattr(base_cls,'__annotations__'):
            for var_name, var_type in base_cls.__annotations__.items():
                if hasattr(base_cls, var_name) is False:
                    if var_name in kwargs:
                        continue
                    var_value = cls.__default__value__(var_type)
                    kwargs[var_name] = var_value
                else:
                    var_value = getattr(base_cls, var_name)
                    if var_value is not None:
                        if get_origin(var_type) is Annotated:
                            continue
                        if get_origin(var_type) is type:
                            if not isinstance(var_value, type):
                                exception_message = f"variable '{var_name}' is defined as Type[T] but has value '{var_value}' which is not a type"
                                raise ValueError(exception_message)
                            type_arg = get_args(var_type)[0]
                            if not issubclass(var_value, type_arg):
                                exception_message = f"variable '{var_name}' is defined as {var_type} but value {var_value} is not a subclass of {type_arg}"
                                raise ValueError(exception_message)
                        elif var_type and not isinstance(var_value, var_type):
                            exception_message = f"variable '{var_name}' is defined as type '{var_type}' but has value '{var_value}' of type '{type(var_value)}'"
                            raise ValueError(exception_message)
                        if var_type not in IMMUTABLE_TYPES and var_name.startswith('__') is False:
                            if obj_is_type_union_compatible(var_type, IMMUTABLE_TYPES) is False:
                                if type(var_type) not in IMMUTABLE_TYPES:
                                    exception_message = f"variable '{var_name}' is defined as type '{var_type}' which is not supported by Type_Safe, with only the following immutable types being supported: '{IMMUTABLE_TYPES}'"
                                    raise ValueError(exception_message)
        if include_base_classes is False:
            break
    return kwargs
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `cls` | `Type` | Class reference | N/A |
|               | `include_base_classes` | `bool` | Whether to include base class attributes | `True` |
| **Returns**    | `dict` | `Dict[str, Any]` | Dictionary of class attributes and values | N/A |
| **Raises**     | `ValueError` | `Exception` | When type validation fails | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `__default__value__()` | Gets default values for types |
|              | `get_origin()` | Gets type hint origin |
|              | `get_args()` | Gets type hint arguments |
|              | `obj_is_type_union_compatible()` | Checks type compatibility |
| **Called By**| `__init__()` | During object initialization |
|              | Object inspection | When examining class attributes |

### __enter__ and __exit__

Context manager implementation for use in 'with' statements.

```python
def __enter__(self): return self
def __exit__(self, exc_type, exc_val, exc_tb): pass
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
| **Returns**    | `self` | `Type_Safe` | The instance itself | N/A |
| **Parameters** (__exit__)| `exc_type` | `Type` | Exception type if raised | N/A |
|               | `exc_val` | `Exception` | Exception value if raised | N/A |
|               | `exc_tb` | `TracebackType` | Exception traceback if raised | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | None | No method calls |
| **Called By**| Context manager | When using 'with' statement |

### __default__value__

Class method that returns the default value for a given type annotation.

```python
@classmethod
def __default__value__(cls, var_type):
    import typing
    from osbot_utils.type_safe.Type_Safe__List import Type_Safe__List
    from osbot_utils.type_safe.Type_Safe__Dict import Type_Safe__Dict

    if get_origin(var_type) is type:
        type_args = get_args(var_type)
        if type_args:
            if isinstance(type_args[0], ForwardRef):
                forward_name = type_args[0].__forward_arg__
                for base_cls in inspect.getmro(cls):
                    if base_cls.__name__ == forward_name:
                        return cls
            return type_args[0]

    if var_type is typing.Set:
        return set()
    if get_origin(var_type) is set:
        return set()

    if var_type is typing.Dict:
        return {}

    if get_origin(var_type) is dict:
        key_type, value_type = get_args(var_type)
        if isinstance(key_type, ForwardRef):
            forward_name = key_type.__forward_arg__
            if forward_name == cls.__name__:
                key_type = cls
        if isinstance(value_type, ForwardRef):
            forward_name = value_type.__forward_arg__
            if forward_name == cls.__name__:
                value_type = cls
        return Type_Safe__Dict(expected_key_type=key_type, expected_value_type=value_type)

    if var_type is typing.List:
        return []

    if get_origin(var_type) is list:
        item_type = get_args(var_type)[0]
        if isinstance(item_type, ForwardRef):
            forward_name = item_type.__forward_arg__
            if forward_name == cls.__name__:
                item_type = cls
        return Type_Safe__List(expected_type=item_type)
    else:
        return default_value(var_type)
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `cls` | `Type` | Class reference | N/A |
|               | `var_type` | `Type` | Type annotation to get default for | N/A |
| **Returns**    | `Any` | Type-specific | Default value for the given type | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `get_origin()` | Gets type hint origin |
|              | `get_args()` | Gets type hint arguments |
|              | `default_value()` | Gets default for basic types |
|              | `Type_Safe__Dict()` | Creates type-safe dictionary |
|              | `Type_Safe__List()` | Creates type-safe list |
| **Called By**| `__cls_kwargs__()` | Getting class attribute defaults |
|              | Type initialization | When creating new type instances |

### __default_kwargs__

Returns a dictionary of all instance attributes and their values, including those from base classes.

```python
def __default_kwargs__(self):
    import inspect
    kwargs = {}
    cls = type(self)
    for base_cls in inspect.getmro(cls):
        if base_cls is object:
            continue
        for k, v in vars(base_cls).items():
            if not k.startswith('__') and not isinstance(v, types.FunctionType):
                if not isinstance(v, classmethod):
                    kwargs[k] = v
        if hasattr(base_cls,'__annotations__'):
            for var_name, var_type in base_cls.__annotations__.items():
                var_value = getattr(self, var_name)
                kwargs[var_name] = var_value

    return kwargs
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
| **Returns**    | `dict` | `Dict[str, Any]` | Dictionary of attributes and values | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `vars()` | Gets object attributes |
|              | `getattr()` | Gets attribute values |
| **Called By**| `__kwargs__()` | Getting instance attributes |
|              | Object inspection | When examining object state |

### __kwargs__

Returns a dictionary of the current instance's attribute values including inherited class defaults.

```python
def __kwargs__(self):
    kwargs = {}
    for key, value in self.__default_kwargs__().items():
        kwargs[key] = self.__getattribute__(key)
    return kwargs
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
| **Returns**    | `dict` | `Dict[str, Any]` | Dictionary of instance attributes and values | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `__default_kwargs__()` | Gets default attributes |
|              | `__getattribute__()` | Gets attribute values |
| **Called By**| `__locals__()` | Getting local attributes |
|              | Object serialization | When converting object to dict |

### __locals__

Returns a dictionary of the current instance's attribute values.

```python
def __locals__(self):
    kwargs = self.__kwargs__()
    if not isinstance(vars(self), types.FunctionType):
        for k, v in vars(self).items():
            if not isinstance(v, types.FunctionType) and not isinstance(v,classmethod):
                if k.startswith('__') is False:
                    kwargs[k] = v
    return kwargs
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
| **Returns**    | `dict` | `Dict[str, Any]` | Dictionary of local attributes | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `__kwargs__()` | Gets all attributes |
|              | `vars()` | Gets object attributes |
| **Called By**| `__attr_names__()` | Getting attribute names |
|              | Object inspection | When examining object state |

### __schema__

Returns the class's type annotations.

```python
@classmethod
def __schema__(cls):
    if hasattr(cls,'__annotations__'):
        return cls.__annotations__
    return {}
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `cls` | `Type` | Class reference | N/A |
| **Returns**    | `dict` | `Dict[str, Type]` | Dictionary of type annotations | `{}` |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | None | Direct attribute access |
| **Called By**| Schema inspection | When examining class type information |

### bytes

Converts the object to a bytes representation using JSON serialization.

```python
def bytes(self):
    from osbot_utils.utils.Json import json_to_bytes
    return json_to_bytes(self.json())
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
| **Returns**    | `bytes` | `bytes` | Bytes representation of object | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `json()` | Gets JSON representation |
|              | `json_to_bytes()` | Converts JSON to bytes |
| **Called By**| Serialization | When byte serialization is needed |

### bytes_gz

Converts the object to a gzipped bytes representation.

```python
def bytes_gz(self):
    from osbot_utils.utils.Json import json_to_gz
    return json_to_gz(self.json())
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
| **Returns**    | `bytes` | `bytes` | Gzipped bytes representation | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `json()` | Gets JSON representation |
|              | `json_to_gz()` | Converts JSON to gzipped bytes |
| **Called By**| Compression | When compressed serialization is needed |

### json

Returns a JSON-compatible dictionary representation of the object.

```python
def json(self):
    return self.serialize_to_dict()
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
| **Returns**    | `dict` | `Dict[str, Any]` | JSON-compatible dictionary | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `serialize_to_dict()` | Converts object to dictionary |
| **Called By**| `bytes()` | Converting to bytes |
|              | `bytes_gz()` | Converting to gzipped bytes |
|              | Serialization | When JSON representation is needed |

### merge_with

Merges the current instance with another instance, preserving original attributes.

```python
def merge_with(self, target):
    original_attrs = {k: v for k, v in self.__dict__.items() if k not in target.__dict__}
    self.__dict__ = target.__dict__
    self.__dict__.update(original_attrs)
    return self
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
|               | `target` | `Type_Safe` | Target instance to merge with | N/A |
| **Returns**    | `self` | `Type_Safe` | Modified instance | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | None | Direct dictionary operations |
| **Called By**| Object merging | When combining object states |

### reset

Resets all attributes to their class-defined default values.

```python
def reset(self):
    for k,v in self.__cls_kwargs__().items():
        setattr(self, k, v)
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
| **Returns**    | None | `None` | No return value | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `__cls_kwargs__()` | Gets class defaults |
|              | `setattr()` | Sets attribute values |
| **Called By**| State reset | When resetting object state |

### update_from_kwargs

Updates instance attributes with values from provided keyword arguments.

```python
def update_from_kwargs(self, **kwargs):
    from osbot_utils.utils.Objects import value_type_matches_obj_annotation_for_attr
    for key, value in kwargs.items():
        if value is not None:
            if hasattr(self,'__annotations__'):
                if value_type_matches_obj_annotation_for_attr(self, key, value) is False:
                    raise ValueError(f"Invalid type for attribute '{key}'. Expected '{self.__annotations__.get(key)}' but got '{type(value)}'")
            setattr(self, key, value)
    return self
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
|               | `**kwargs` | `dict` | Keyword arguments to update | `{}` |
| **Returns**    | `self` | `Type_Safe` | Modified instance | N/A |
| **Raises**     | `ValueError` | `Exception` | When type validation fails | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `value_type_matches_obj_annotation_for_attr()` | Validates type matching |
|              | `setattr()` | Sets attribute values |
| **Called By**| State updates | When updating object attributes |

### deserialize_type__using_value

Reconstructs a type object from its string representation.

```python
def deserialize_type__using_value(self, value):
    if value:
        try:
            module_name, type_name = value.rsplit('.', 1)
            if module_name == 'builtins' and type_name == 'NoneType':
                value = types.NoneType
            else:
                module = __import__(module_name, fromlist=[type_name])
                value = getattr(module, type_name)
        except (ValueError, ImportError, AttributeError) as e:
            raise ValueError(f"Could not reconstruct type from '{value}': {str(e)}")
    return value
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
|               | `value` | `str` | String representation of type | N/A |
| **Returns**    | `Type` | `type` | Reconstructed type object | N/A |
| **Raises**     | `ValueError` | `Exception` | When type reconstruction fails | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `__import__()` | Imports module dynamically |
|              | `getattr()` | Gets type from module |
| **Called By**| `deserialize_from_dict()` | During object deserialization |

### deserialize_dict__using_key_value_annotations

Deserializes a dictionary using type annotations for keys and values.

```python
def deserialize_dict__using_key_value_annotations(self, key, value):
    from osbot_utils.type_safe.Type_Safe__Dict import Type_Safe__Dict
    annotations = all_annotations(self)
    dict_annotations_tuple = get_args(annotations.get(key))
    if not dict_annotations_tuple:
        return value
    if not type(value) is dict:
        return value
    key_class = dict_annotations_tuple[0]
    value_class = dict_annotations_tuple[1]
    new_value = Type_Safe__Dict(expected_key_type=key_class, expected_value_type=value_class)

    for dict_key, dict_value in value.items():
        if issubclass(key_class, Type_Safe):
            new__dict_key = key_class().deserialize_from_dict(dict_key)
        else:
            new__dict_key = key_class(dict_key)

        if type(dict_value) == value_class:
            new__dict_value = dict_value
        elif issubclass(value_class, Type_Safe):
            new__dict_value = value_class().deserialize_from_dict(dict_value)
        elif value_class is Any:
            new__dict_value = dict_value
        else:
            new__dict_value = value_class(dict_value)
        new_value[new__dict_key] = new__dict_value

    return new_value
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
|               | `key` | `str` | Dictionary attribute name | N/A |
|               | `value` | `dict` | Dictionary to deserialize | N/A |
| **Returns**    | `Type_Safe__Dict` | `Type_Safe__Dict` | Type-safe dictionary | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `all_annotations()` | Gets type annotations |
|              | `get_args()` | Gets type arguments |
|              | `Type_Safe__Dict()` | Creates type-safe dict |
|              | `deserialize_from_dict()` | Deserializes nested objects |
| **Called By**| `__setattr__()` | During attribute assignment |
|              | `deserialize_from_dict()` | During object deserialization |

### deserialize_from_dict

Deserializes an object from a dictionary representation.

```python
def deserialize_from_dict(self, data, raise_on_not_found=False):
    from decimal import Decimal
    from enum import EnumMeta
    from osbot_utils.type_safe.Type_Safe__List import Type_Safe__List
    from osbot_utils.helpers.Random_Guid import Random_Guid
    from osbot_utils.helpers.Random_Guid_Short import Random_Guid_Short
    from osbot_utils.utils.Objects import (obj_is_attribute_annotation_of_type,
                                         obj_attribute_annotation,
                                         enum_from_value)
    from osbot_utils.helpers.Safe_Id import Safe_Id
    from osbot_utils.helpers.Timestamp_Now import Timestamp_Now

    if hasattr(data, 'items') is False:
        raise ValueError(f"Expected a dictionary, but got '{type(data)}'")

    for key, value in data.items():
        if hasattr(self, key) and isinstance(getattr(self, key), Type_Safe):
            getattr(self, key).deserialize_from_dict(value)
        else:
            if hasattr(self, '__annotations__'):
                if hasattr(self, key) is False:
                    if raise_on_not_found:
                        raise ValueError(f"Attribute '{key}' not found in '{self.__class__.__name__}'")
                    else:
                        continue
                if obj_attribute_annotation(self, key) == type:
                    value = self.deserialize_type__using_value(value)
                elif obj_is_attribute_annotation_of_type(self, key, dict):
                    value = self.deserialize_dict__using_key_value_annotations(key, value)
                elif obj_is_attribute_annotation_of_type(self, key, list):
                    attribute_annotation = obj_attribute_annotation(self, key)
                    attribute_annotation_args = get_args(attribute_annotation)
                    if attribute_annotation_args:
                        expected_type = get_args(attribute_annotation)[0]
                        type_safe_list = Type_Safe__List(expected_type)
                        for item in value:
                            if type(item) is dict:
                                new_item = expected_type(**item)
                            else:
                                new_item = expected_type(item)
                            type_safe_list.append(new_item)
                        value = type_safe_list
                else:
                    if value is not None:
                        if obj_is_attribute_annotation_of_type(self, key, EnumMeta):
                            enum_type = getattr(self, '__annotations__').get(key)
                            if type(value) is not enum_type:
                                value = enum_from_value(enum_type, value)
                        elif obj_is_attribute_annotation_of_type(self, key, Decimal):
                            value = Decimal(value)
                        elif obj_is_attribute_annotation_of_type(self, key, Safe_Id):
                            value = Safe_Id(value)
                        elif obj_is_attribute_annotation_of_type(self, key, Random_Guid):
                            value = Random_Guid(value)
                        elif obj_is_attribute_annotation_of_type(self, key, Random_Guid_Short):
                            value = Random_Guid_Short(value)
                        elif obj_is_attribute_annotation_of_type(self, key, Timestamp_Now):
                            value = Timestamp_Now(value)
                setattr(self, key, value)

    return self
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
|               | `data` | `dict` | Dictionary to deserialize from | N/A |
|               | `raise_on_not_found` | `bool` | Whether to raise on missing attributes | `False` |
| **Returns**    | `self` | `Type_Safe` | Deserialized instance | N/A |
| **Raises**     | `ValueError` | `Exception` | On invalid data or missing attributes | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `deserialize_type__using_value()` | Deserializes type objects |
|              | `deserialize_dict__using_key_value_annotations()` | Deserializes dicts |
|              | `Type_Safe__List()` | Creates type-safe lists |
|              | Various type constructors | Creates typed values |
| **Called By**| `from_json()` | During JSON deserialization |
|              | Deserialization | When recreating objects |

### obj

Creates a simple object representation from the instance.

```python
def obj(self):
    from osbot_utils.utils.Objects import dict_to_obj
    return dict_to_obj(self.json())
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
| **Returns**    | `object` | `object` | Simple object representation | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `json()` | Gets JSON representation |
|              | `dict_to_obj()` | Converts dict to object |
| **Called By**| Object conversion | When simpler object form needed |

### serialize_to_dict

Converts the instance to a dictionary representation.

```python
def serialize_to_dict(self):
    return serialize_to_dict(self)
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
| **Returns**    | `dict` | `Dict[str, Any]` | Dictionary representation | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | Global `serialize_to_dict()` | Performs serialization |
| **Called By**| `json()` | During JSON conversion |
|              | Serialization | When dict form needed |

### print

Prints a pretty-formatted representation of the instance.

```python
def print(self):
    from osbot_utils.utils.Dev import pprint
    pprint(serialize_to_dict(self))
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `self` | `Type_Safe` | Instance reference | N/A |
| **Returns**    | None | `None` | No return value | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `serialize_to_dict()` | Gets dict representation |
|              | `pprint()` | Pretty prints output |
| **Called By**| Debugging | When printing object state |

### from_json

Class method that creates an instance from JSON data.

```python
@classmethod
def from_json(cls, json_data, raise_on_not_found=False):
    from osbot_utils.utils.Json import json_parse

    if type(json_data) is str:
        json_data = json_parse(json_data)
    if json_data:
        return cls().deserialize_from_dict(json_data,raise_on_not_found=raise_on_not_found)
    return cls()
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `cls` | `Type` | Class reference | N/A |
|               | `json_data` | `Union[str, dict]` | JSON data to deserialize | N/A |
|               | `raise_on_not_found` | `bool` | Whether to raise on missing attributes | `False` |
| **Returns**    | `Type_Safe` | `Type_Safe` | New instance from JSON | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `json_parse()` | Parses JSON string |
|              | `deserialize_from_dict()` | Deserializes into instance |
| **Called By**| JSON deserialization | When creating from JSON |

## Global Functions

### serialize_to_dict

Global function that handles the serialization of objects to dictionary format.

```python
def serialize_to_dict(obj):
    from decimal import Decimal
    from enum    import Enum
    from typing  import List

    if isinstance(obj, (str, int, float, bool, bytes, Decimal)) or obj is None:
        return obj
    elif isinstance(obj, Enum):
        return obj.name
    elif isinstance(obj, type):
        return f"{obj.__module__}.{obj.__name__}"
    elif isinstance(obj, list) or isinstance(obj, List):
        return [serialize_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_to_dict(value) for key, value in obj.items()}
    elif hasattr(obj, "__dict__"):
        data = {}
        for key, value in obj.__dict__.items():
            if key.startswith('__') is False:
                data[key] = serialize_to_dict(value)
        return data
    else:
        raise TypeError(f"Type {type(obj)} not serializable")
```

| **Category** | **Name** | **Type** | **Description** | **Default** |
|--------------|----------|-----------|-----------------|-------------|
| **Parameters** | `obj` | `Any` | Object to serialize | N/A |
| **Returns**    | `dict` | `Dict[str, Any]` | Serialized dictionary representation | N/A |
| **Raises**     | `TypeError` | `Exception` | When object cannot be serialized | N/A |

| **Category** | **Method/Function** | **Description** |
|--------------|-------------------|----------------|
| **Calls**    | `serialize_to_dict()` | Recursive self-calls for nested objects |
| **Called By**| Type_Safe's `serialize_to_dict()` | During object serialization |
|              | Serialization operations | When converting objects to dicts |
from enum                                                       import EnumMeta
from osbot_utils.type_safe.shared.Type_Safe__Annotations        import type_safe_annotations
from osbot_utils.type_safe.steps.Type_Safe__Step__Default_Value import type_safe_step_default_value, get_args


class Type_Safe__Step__Init:

    def init(self, __self         ,
                   __class_kwargs ,
                   **kwargs
              ) -> None:

        for (key, value) in __class_kwargs.items():                             # assign all default values to target
            if hasattr(__self, key):
                existing_value = getattr(__self, key)
                if existing_value is not None:
                    setattr(__self, key, existing_value)
                    continue
            setattr(__self, key, value)

        for (key, value) in kwargs.items():                                     # overwrite with values provided in ctor
            if hasattr(__self, key):
                if value is not None:                                           # prevent None values from overwriting existing values, which is quite common in default constructors
                    value = self.convert_value_to_type_safe_objects(__self, key, value)
                    setattr(__self, key, value)
            else:
                raise ValueError(f"{__self.__class__.__name__} has no attribute '{key}' and cannot be assigned the value '{value}'. "
                                 f"Use {__self.__class__.__name__}.__default_kwargs__() see what attributes are available")

    def convert_value_to_type_safe_objects(self, __self, key, value):
        annotation = type_safe_annotations.obj_attribute_annotation(__self, key)
        if annotation:
            if isinstance(annotation, EnumMeta) and type(value) is str:
                if value not in annotation.__members__:
                    raise ValueError(f"Invalid value '{value}' for enum {annotation.__name__}")
                value = annotation[value]
            else:

                origin = type_safe_annotations.get_origin(annotation)
                # If the value is an empty container, create proper type-safe container
                if ((isinstance(value, list ) and len(value) == 0) or
                    (isinstance(value, dict ) and len(value) == 0) or
                    (isinstance(value, set  ) and len(value) == 0) or
                    (isinstance(value, tuple) and len(value) == 0)):
                    value = type_safe_step_default_value.default_value(__self.__class__, annotation)        # Use default_value to create the proper type-safe container
                            # Handle non-empty list
                elif origin is list and isinstance(value, list):
                    from osbot_utils.type_safe.Type_Safe__List import Type_Safe__List
                    item_type = get_args(annotation)[0]
                    type_safe_list = Type_Safe__List(expected_type=item_type)
                    for item in value:
                        type_safe_list.append(item)
                    return type_safe_list

                # Handle non-empty set
                elif origin is set and isinstance(value, set):
                    from osbot_utils.type_safe.Type_Safe__Set import Type_Safe__Set
                    item_type = get_args(annotation)[0]
                    type_safe_set = Type_Safe__Set(expected_type=item_type)
                    for item in value:
                        type_safe_set.add(item)
                    return type_safe_set

                # Handle non-empty tuple
                elif origin is tuple and isinstance(value, tuple):
                    from osbot_utils.type_safe.Type_Safe__Tuple import Type_Safe__Tuple
                    item_types = get_args(annotation)
                    return Type_Safe__Tuple(expected_types=item_types, items=value)

                # Handle non-empty dict
                elif origin is dict and isinstance(value, dict):
                    from osbot_utils.type_safe.Type_Safe__Dict import Type_Safe__Dict
                    key_type, value_type = get_args(annotation)
                    type_safe_dict       = Type_Safe__Dict(expected_key_type=key_type, expected_value_type=value_type)
                    for k, v in value.items():
                        type_safe_dict[k] = v
                    return type_safe_dict


        return value

type_safe_step_init = Type_Safe__Step__Init()
from typing import get_origin, get_args, ForwardRef, Annotated, List, Tuple, Dict, Any, Optional, Type
from osbot_utils.type_safe.shared.Type_Safe__Validation import type_safe_validation
from osbot_utils.utils.Objects                          import all_annotations, obj_attribute_annotation


class Type_Safe__Step__Init:

    # def check_obj_type_annotation_mismatch(self, target, attr_name, value):
    #     if self.value_type_matches_obj_annotation_for_attr(target, attr_name, value) is False:                          # handle case with normal types
    #         if self.value_type_matches_obj_annotation_for_union_and_annotated(target, attr_name, value) is False:       #     this is done like this because value_type_matches_obj_annotation_for_union_attr will return None when there is no Union objects
    #             # todo: check if this is still needed since there is no code coverage here
    #             type_safe_raise_exception.type_mismatch_error(attr_name, target.__annotations__.get(attr_name), type(value))
    #             #raise TypeError(f"Invalid type for attribute '{attr_name}'. Expected '{target.__annotations__.get(attr_name)}' but got '{type(value)}'")


    def init(self, __self         ,
                   __class_kwargs ,
                   **kwargs
             )                   -> None:

        for (key, value) in __class_kwargs.items():                             # assign all default values to target
            # if value is not None:                                             # when the value is explicitly set to None on the class static vars, we can't check for type safety
            #     self.check_obj_type_annotation_mismatch(__self, key, value)
            if hasattr(__self, key):
                existing_value = getattr(__self, key)
                if existing_value is not None:
                    setattr(__self, key, existing_value)
                    continue
            setattr(__self, key, value)

        for (key, value) in kwargs.items():                             # overwrite with values provided in ctor
            if hasattr(__self, key):
                if value is not None:                                   # prevent None values from overwriting existing values, which is quite common in default constructors
                    setattr(__self, key, value)
            else:
                raise ValueError(f"{__self.__class__.__name__} has no attribute '{key}' and cannot be assigned the value '{value}'. "
                                 f"Use {__self.__class__.__name__}.__default_kwargs__() see what attributes are available")

type_safe_step_init = Type_Safe__Step__Init()
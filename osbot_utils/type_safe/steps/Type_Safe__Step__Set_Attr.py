from typing                                                 import get_origin, Annotated, get_args
from osbot_utils.utils.Objects                              import all_annotations
from osbot_utils.utils.Objects                              import convert_dict_to_value_from_obj_annotation
from osbot_utils.utils.Objects                              import convert_to_value_from_obj_annotation
from osbot_utils.utils.Objects                              import value_type_matches_obj_annotation_for_attr
from osbot_utils.utils.Objects                              import value_type_matches_obj_annotation_for_union_and_annotated
from osbot_utils.type_safe.validators.Type_Safe__Validator  import Type_Safe__Validator


class Type_Safe__Step__Set_Attr:

    def setattr(self, _super, _self, name, value):

        annotations = all_annotations(_self)
        if not annotations:                                             # can't do type safety checks if the class does not have annotations
            return _super.__setattr__(name, value)

        if value is not None:
            if type(value) is dict:
                value = convert_dict_to_value_from_obj_annotation(_self, name, value)
            elif type(value) in [int, str]:                                                   # for now only a small number of str and int classes are supported (until we understand the full implications of this)
                value = convert_to_value_from_obj_annotation (_self, name, value)
            else:
                origin = get_origin(value)
                if origin is not None:
                    value = origin
            check_1 = value_type_matches_obj_annotation_for_attr               (_self, name, value)
            check_2 = value_type_matches_obj_annotation_for_union_and_annotated(_self, name, value)
            if (check_1 is False and check_2 is None  or
                check_1 is None  and check_2 is False or
                check_1 is False and check_2 is False   ):          # fix for type safety assigment on Union vars
                raise ValueError(f"Invalid type for attribute '{name}'. Expected '{annotations.get(name)}' but got '{type(value)}'")
        else:
            if hasattr(_self, name) and annotations.get(name) :     # don't allow previously set variables to be set to None
                if getattr(_self, name) is not None:                         # unless it is already set to None
                    raise ValueError(f"Can't set None, to a variable that is already set. Invalid type for attribute '{name}'. Expected '{_self.__annotations__.get(name)}' but got '{type(value)}'")

        # todo: refactor this to separate method
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
                    value = _self.deserialize_dict__using_key_value_annotations(name, value)

        _super.__setattr__(name, value)


type_safe_step_set_attr = Type_Safe__Step__Set_Attr()
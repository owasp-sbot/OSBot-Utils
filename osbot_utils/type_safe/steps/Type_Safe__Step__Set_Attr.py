from typing                                                  import get_origin, Annotated, get_args, _SpecialGenericAlias
from osbot_utils.type_safe.shared.Type_Safe__Cache           import type_safe_cache
from osbot_utils.type_safe.shared.Type_Safe__Raise_Exception import type_safe_raise_exception
from osbot_utils.utils.Objects                               import all_annotations, are_types_compatible_for_assigment
from osbot_utils.utils.Objects                               import convert_dict_to_value_from_obj_annotation
from osbot_utils.utils.Objects                               import convert_to_value_from_obj_annotation
from osbot_utils.utils.Objects                               import value_type_matches_obj_annotation_for_attr
from osbot_utils.utils.Objects                               import value_type_matches_obj_annotation_for_union_and_annotated
from osbot_utils.type_safe.validators.Type_Safe__Validator   import Type_Safe__Validator


class Type_Safe__Step__Set_Attr:

    def verify_value(self, _self, annotations, name, value):                                         # refactor the logic of this method since it is confusing
        check_1 = value_type_matches_obj_annotation_for_attr               (_self, name, value)
        check_2 = value_type_matches_obj_annotation_for_union_and_annotated(_self, name, value)
        if (check_1 is False and check_2 is None  or
            check_1 is None  and check_2 is False or
            check_1 is False and check_2 is False   ):                                              # fix for type safety assigment on Union vars
            raise ValueError(f"Invalid type for attribute '{name}'. Expected '{annotations.get(name)}' but got '{type(value)}'")

    def resolve_value(self, _self, annotations, name, value):
        if type(value) is dict:
            value = self.resolve_value__dict(_self, name, value)
        elif type(value) in [int, str]:                                                   # for now only a small number of str and int classes are supported (until we understand the full implications of this)
            value = self.resolve_value__int_str(_self, name, value)
        else:
            value = self.resolve_value__from_origin(value)

        self.verify_value(_self, annotations, name, value)
        return value

    def resolve_value__dict(self, _self, name, value):
        return convert_dict_to_value_from_obj_annotation(_self, name, value)

    def resolve_value__int_str(self, _self, name, value):
        immutable_vars = type_safe_cache.get_class_immutable_vars(_self.__class__)      # get the cached value of immutable vars for this class

        if name in immutable_vars:                                                      # we only need to do the conversion if the variable is immutable
            return value

        return  convert_to_value_from_obj_annotation(_self, name, value)



    def resolve_value__from_origin(self, value):
        origin = get_origin(value)
        if origin is not None:
            value = origin
        return value

    def validate_if_value_has_been_set(self, _self, annotations, name, value):
        if hasattr(_self, name) and annotations.get(name) :     # don't allow previously set variables to be set to None
            if getattr(_self, name) is not None:                         # unless it is already set to None
                raise ValueError(f"Can't set None, to a variable that is already set. Invalid type for attribute '{name}'. Expected '{_self.__annotations__.get(name)}' but got '{type(value)}'")

    def handle_get_class__annotated(self, annotation, name, value):
        annotation_args = get_args(annotation)
        target_type = annotation_args[0]
        for attribute in annotation_args[1:]:
            if isinstance(attribute, Type_Safe__Validator):
                attribute.validate(value=value, field_name=name, target_type=target_type)

    def handle_get_class__dict(self, _self, name, value):
        # todo: refactor how this actually works since it is not good to having to use the deserialize_dict__using_key_value_annotations from here
        from osbot_utils.type_safe.steps.Type_Safe__Step__From_Json import Type_Safe__Step__From_Json               # here because of circular dependencies
        value = Type_Safe__Step__From_Json().deserialize_dict__using_key_value_annotations(_self, name, value)
        return value

    def handle_get_class(self, _self, annotations, name, value):
        if hasattr(annotations, 'get'):
            annotation = annotations.get(name)
            if annotation:
                annotation_origin = get_origin(annotation)
                if annotation_origin is Annotated:
                    self.handle_get_class__annotated(annotation, name, value)
                elif annotation_origin is dict:
                    value = self.handle_get_class__dict(_self, name, value)
        return value

    def setattr(self, _super, _self, name, value):
        if value is not None and type(value) is not _SpecialGenericAlias:                    # todo: refactor this section into a separate method
            immutable_vars = type_safe_cache.get_class_immutable_vars(_self.__class__)
            if name in immutable_vars:
                expected_type = immutable_vars[name]
                if value is not type:
                    current_type  = type(value)
                else:
                    current_type = type
                if not are_types_compatible_for_assigment(current_type, expected_type):
                    type_safe_raise_exception.type_mismatch_error(name, expected_type, current_type)
                return _super.__setattr__(name, value)

        annotations = all_annotations(_self)
        if not annotations:                                             # can't do type safety checks if the class does not have annotations
            return _super.__setattr__(name, value)

        if value is not None:
            value = self.resolve_value          (_self, annotations, name, value)
            value = self.handle_get_class(_self, annotations, name, value)
        else:
            self.validate_if_value_has_been_set(_self, annotations, name, value)

        _super.__setattr__(name, value)


type_safe_step_set_attr = Type_Safe__Step__Set_Attr()
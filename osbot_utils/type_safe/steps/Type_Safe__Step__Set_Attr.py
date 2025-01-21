from typing                                                  import get_origin, Annotated, get_args
from osbot_utils.type_safe.shared.Type_Safe__Cache           import type_safe_cache
from osbot_utils.type_safe.shared.Type_Safe__Convert         import type_safe_convert
from osbot_utils.type_safe.shared.Type_Safe__Validation      import type_safe_validation
from osbot_utils.type_safe.validators.Type_Safe__Validator   import Type_Safe__Validator

class Type_Safe__Step__Set_Attr:

    def resolve_value(self, _self, annotations, name, value):
        if type(value) is dict:
            value = self.resolve_value__dict(_self, name, value)
        elif type(value) in [int, str]:                                                   # for now only a small number of str and int classes are supported (until we understand the full implications of this)
            value = self.resolve_value__int_str(_self, name, value)
        else:
            value = self.resolve_value__from_origin(value)

        type_safe_validation.validate_type_compatibility(_self, annotations, name, value)
        return value

    def resolve_value__dict(self, _self, name, value):
        return type_safe_convert.convert_dict_to_value_from_obj_annotation(_self, name, value)

    def resolve_value__int_str(self, _self, name, value):
        immutable_vars = type_safe_cache.get_class_immutable_vars(_self.__class__)      # get the cached value of immutable vars for this class

        if name in immutable_vars:                                                      # we only need to do the conversion if the variable is immutable
            return value

        return  type_safe_convert.convert_to_value_from_obj_annotation(_self, name, value)

    def resolve_value__from_origin(self, value):
        #origin = type_safe_cache.get_origin(value)                                     # todo: figure out why this is the only place that the type_safe_cache.get_origin doesn't work (due to WeakKeyDictionary key error on value)
        origin = get_origin(value)

        if origin is not None:
            value = origin
        return value

    def handle_get_class__annotated(self, annotation, name, value):
        annotation_args = get_args(annotation)
        target_type = annotation_args[0]
        for attribute in annotation_args[1:]:
            if isinstance(attribute, Type_Safe__Validator):
                attribute.validate(value=value, field_name=name, target_type=target_type)

    def handle_get_class__dict(self, _self, name, value):
        if value:                                                                                                       # todo: see side effects of doing this here (since going into deserialize_dict__using_key_value_annotations has performance hit)
            from osbot_utils.type_safe.steps.Type_Safe__Step__From_Json import Type_Safe__Step__From_Json               # here because of circular dependencies
            value = Type_Safe__Step__From_Json().deserialize_dict__using_key_value_annotations(_self, name, value)      # todo: refactor how this actually works since it is not good to having to use the deserialize_dict__using_key_value_annotations from here
        return value

    def handle_get_class(self, _self, annotations, name, value):
        if hasattr(annotations, 'get'):
            annotation = annotations.get(name)
            if annotation:
                annotation_origin = type_safe_cache.get_origin(annotation)
                if annotation_origin is Annotated:
                    self.handle_get_class__annotated(annotation, name, value)
                elif annotation_origin is dict:
                    value = self.handle_get_class__dict(_self, name, value)
        return value

    def handle_special_generic_alias(self, _super, _self, name, value):
        immutable_vars = type_safe_cache.get_class_immutable_vars(_self.__class__)       # todo: refactor this section into a separate method
        if name in immutable_vars:
            expected_type = immutable_vars[name]
            current_type  = type if value is type else type(value)
            type_safe_validation.validate_if__types_are_compatible_for_assigment(name, current_type, expected_type)
            _super.__setattr__(name, value)
            return True
        return False

    def setattr(self, _super, _self, name, value):
        if type_safe_validation.check_if__value_is__special_generic_alias(value):
            if self.handle_special_generic_alias(_super, _self, name, value):
                return

        annotations = dict(type_safe_cache.get_obj_annotations(_self))

        if not annotations:                                             # can't do type safety checks if the class does not have annotations
            return _super.__setattr__(name, value)

        if value is not None:
            value = self.resolve_value          (_self, annotations, name, value)
            value = self.handle_get_class(_self, annotations, name, value)
        else:
            type_safe_validation.validate_if_value_has_been_set(_self, annotations, name, value)

        _super.__setattr__(name, value)


type_safe_step_set_attr = Type_Safe__Step__Set_Attr()
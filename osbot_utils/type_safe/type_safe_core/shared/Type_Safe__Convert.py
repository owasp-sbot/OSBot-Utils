from typing                                                           import get_args
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Cache     import type_safe_cache
from osbot_utils.utils.Objects                                        import base_classes_names
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict import Type_Safe__Dict


class Type_Safe__Convert:
    def convert_dict_to_value_from_obj_annotation(self, target, attr_name, value):                    # todo: refactor this with code from convert_str_to_value_from_obj_annotation since it is mostly the same
        if target is not None and attr_name is not None:
            if hasattr(target, '__annotations__'):
                obj_annotations  = target.__annotations__
                if hasattr(obj_annotations,'get'):
                    attribute_annotation = obj_annotations.get(attr_name)
                    args = get_args(attribute_annotation)
                    if len(args) == 2 and args[1] is type(None):                            # todo: find a better way to do this, since this is handling an edge case when origin_attr_type is Optional (which is an shorthand for Union[X, None] )
                        attribute_annotation = args[0]

                    if isinstance(attribute_annotation, type) and issubclass(attribute_annotation, Type_Safe__Dict):
                        return attribute_annotation(value)                                  # Convert plain dict to subclass

                    if 'Type_Safe' in base_classes_names(attribute_annotation):
                        return attribute_annotation(**value)
        return value

    def convert_to_value_from_obj_annotation(self, target, attr_name, value):                             # todo: see the side effects of doing this for all ints and floats

        if target is not None and attr_name is not None:
            if hasattr(target, '__annotations__'):
                obj_annotations  = target.__annotations__
                if hasattr(obj_annotations,'get'):
                    attribute_annotation = obj_annotations.get(attr_name)
                    if attribute_annotation:
                        origin = type_safe_cache.get_origin(attribute_annotation)                               # Add handling for Type[T] annotations
                        if origin is type and isinstance(value, str):
                            return self.get_class_from_class_name(value)
                        if isinstance(attribute_annotation, type) and issubclass(attribute_annotation, (str, int)):
                            return attribute_annotation(value)
        return value

    def get_class_from_class_name(self, value):
        try:                                                                # Convert string path to actual type
            if len(value.rsplit('.', 1)) > 1:
                module_name, class_name = value.rsplit('.', 1)
                module = __import__(module_name, fromlist=[class_name])
                return getattr(module, class_name)
        except (ValueError, ImportError, AttributeError) as e:
            raise ValueError(f"Could not convert '{value}' to type: {str(e)}")
type_safe_convert = Type_Safe__Convert()
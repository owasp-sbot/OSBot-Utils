from osbot_utils.type_safe.shared.Type_Safe__Cache import type_safe_cache
from osbot_utils.utils.Objects                     import base_classes_names


class Type_Safe__Convert:
    def convert_dict_to_value_from_obj_annotation(self, target, attr_name, value):                    # todo: refactor this with code from convert_str_to_value_from_obj_annotation since it is mostly the same
        if target is not None and attr_name is not None:
            if hasattr(target, '__annotations__'):
                obj_annotations  = target.__annotations__
                if hasattr(obj_annotations,'get'):
                    attribute_annotation = obj_annotations.get(attr_name)
                    if 'Type_Safe' in base_classes_names(attribute_annotation):
                        return attribute_annotation(**value)
        return value

    def convert_to_value_from_obj_annotation(self, target, attr_name, value):                             # todo: see the side effects of doing this for all ints and floats

        from osbot_utils.helpers.Guid           import Guid
        from osbot_utils.helpers.Timestamp_Now  import Timestamp_Now
        from osbot_utils.helpers.Random_Guid    import Random_Guid
        from osbot_utils.helpers.Safe_Id        import Safe_Id
        from osbot_utils.helpers.Str_ASCII      import Str_ASCII
        from osbot_utils.helpers.Obj_Id         import Obj_Id

        TYPE_SAFE__CONVERT_VALUE__SUPPORTED_TYPES = [Guid, Random_Guid, Safe_Id, Str_ASCII, Timestamp_Now, Obj_Id]

        if target is not None and attr_name is not None:
            if hasattr(target, '__annotations__'):
                obj_annotations  = target.__annotations__
                if hasattr(obj_annotations,'get'):
                    attribute_annotation = obj_annotations.get(attr_name)
                    if attribute_annotation:
                        origin = type_safe_cache.get_origin(attribute_annotation)                               # Add handling for Type[T] annotations
                        if origin is type and isinstance(value, str):
                            return self.get_class_from_class_name(value)
                        if attribute_annotation in TYPE_SAFE__CONVERT_VALUE__SUPPORTED_TYPES:          # for now hard-coding this to just these types until we understand the side effects
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
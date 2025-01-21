from osbot_utils.type_safe.shared.Type_Safe__Cache  import type_safe_cache


class Type_Safe__Annotations:

    def all_annotations(self, target):
        return type_safe_cache.get_obj_annotations(target)                          # use cache

    def all_annotations__in_class(self, cls):
        return type_safe_cache.get_class_annotations(cls)

    def obj_attribute_annotation(self, target, attr_name):
        return self.all_annotations(target).get(attr_name)                          # use cache

    def obj_is_attribute_annotation_of_type(self, target, attr_name, expected_type):
        attribute_annotation = self.obj_attribute_annotation(target, attr_name)
        if expected_type is attribute_annotation:
            return True
        if expected_type is type(attribute_annotation):
            return True
        if expected_type is type_safe_cache.get_origin(attribute_annotation):                         # handle genericAlias
            return True
        return False

    def get_origin(self, var_type):
        return type_safe_cache.get_origin(var_type)

type_safe_annotations = Type_Safe__Annotations()


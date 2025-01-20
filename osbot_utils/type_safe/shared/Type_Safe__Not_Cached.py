from typing import get_origin

class Type_Safe__Not_Cached:

    def all_annotations(self, target):
        annotations = {}
        if hasattr(target.__class__, '__mro__'):
            for base in reversed(target.__class__.__mro__):
                if hasattr(base, '__annotations__'):
                    annotations.update(base.__annotations__)
        return annotations

    def all_annotations__in_class(self, target):
        annotations = {}
        if hasattr(target, '__mro__'):
            for base in reversed(target.__mro__):
                if hasattr(base, '__annotations__'):
                    annotations.update(base.__annotations__)
        return annotations

    def get_origin(self, var_type):
        return get_origin(var_type)

type_safe_not_cached = Type_Safe__Not_Cached()
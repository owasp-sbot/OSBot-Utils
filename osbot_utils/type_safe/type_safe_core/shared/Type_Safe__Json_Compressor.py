from typing                                                                                 import Dict, Any, Type
from osbot_utils.type_safe.Type_Safe__Base                                                  import Type_Safe__Base
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Cache                           import type_safe_cache
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Json_Compressor__Type_Registry  import Type_Safe__Json_Compressor__Type_Registry
from osbot_utils.utils.Objects                                                              import class_full_name

class Type_Safe__Json_Compressor(Type_Safe__Base):

    def __init__(self):
        self.type_registry = Type_Safe__Json_Compressor__Type_Registry()

    def compress(self, obj: Any) -> dict:
        if not obj:
            return obj

        self.type_registry.clear()
        compressed = self.compress_object(obj)

        if self.type_registry.registry:
            return { "_type_registry": self.type_registry.reverse,
                     **compressed                                 }
        return compressed

    def compress_object(self, obj: Any) -> Any:
        if isinstance(obj, Type_Safe):
            annotations = type_safe_cache.get_obj_annotations(obj)
            return self.process_type_safe_object(obj, annotations)
        elif isinstance(obj, dict):
            return self.compress_dict(obj)
        elif isinstance(obj, list):
            return [self.compress_object(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self.compress_object(item) for item in obj)
        elif isinstance(obj, set):
            return {self.compress_object(item) for item in obj}
        return obj

    def process_type_safe_object(self, obj        : Type_Safe ,
                                       annotations: Dict
                                  ) -> Dict:
        result = {}
        for key, value in obj.__dict__.items():
            if key.startswith('_'):                                            # Skip internal attributes
                continue
            if key in annotations:
                annotation  = annotations[key]
                result[key] = self.compress_annotated_value(value, annotation)
            else:
                result[key] = self.compress_object(value)
        return result

    def compress_annotated_value(self, value      : Any ,
                                       annotation : Any
                                  ) -> Any:
        origin = type_safe_cache.get_origin(annotation)
        if origin in (type, Type):                                            # Handle Type annotations
            if value:
                return self.type_registry.register_type(class_full_name(value))
            return None
        elif origin is dict:                                                  # Handle Dict annotations
            return self.compress_dict(value)
        elif origin in (list, tuple, set):                                    # Handle sequence annotations
            return self.compress_sequence(value)
        elif isinstance(value, Type_Safe):                                    # Handle nested Type_Safe objects
            return self.compress_object(value)
        return value

    def compress_dict(self, data: Dict) -> Dict:
        if not isinstance(data, dict):
            return data

        result = {}
        for key, value in data.items():
            compressed_key         = self.compress_object(key) if isinstance(key, Type_Safe) else key
            compressed_value       = self.compress_object(value)
            result[compressed_key] = compressed_value
        return result

    def compress_sequence(self, sequence: Any) -> Any:
        if isinstance(sequence, (list, tuple, set)):
            compressed = [self.compress_object(item) for item in sequence]
            if isinstance(sequence, list):
                return compressed
            elif isinstance(sequence, tuple):
                return tuple(compressed)
            else:
                return set(compressed)
        return sequence

    def decompress(self, data: dict) -> dict:
        if not data or "_type_registry" not in data:
            return data

        registry = data.pop("_type_registry")
        return self.expand_types(data.copy(), registry)

    def expand_types(self, obj         : Any            ,
                           type_lookup : Dict[str, str]
                      ) -> Any:
        if isinstance(obj, dict):
            return {k: self.expand_value(v, type_lookup) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.expand_types(item, type_lookup) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self.expand_types(item, type_lookup) for item in obj)
        elif isinstance(obj, set):
            return {self.expand_types(item, type_lookup) for item in obj}
        return obj

    def expand_value(self, value       : Any           ,
                           type_lookup : Dict[str, str]
                      ) -> Any:
        if isinstance(value, str) and value.startswith('@'):
            return type_lookup.get(value, value)
        return self.expand_types(value, type_lookup)

    def register_type(self, type_path: str) -> str:
        return self.type_registry.register_type(type_path)
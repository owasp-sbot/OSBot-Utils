from typing import Dict, Optional


class Type_Safe__Json_Compressor__Type_Registry:

    registry : Dict[str, str]
    reverse  : Dict[str, str]

    def __init__(self):
        self.registry = {}
        self.reverse = {}

    def create_reference_name(self, type_path: str) -> str:
        parts      = type_path.split('.')
        class_name = parts[-1]
        parts     = class_name.split('__')

        if len(parts) > 1:
            name_parts = []
            for part in parts:
                name_parts.append(part.lower())
            return f"@{'_'.join(name_parts)}"

        return f"@{class_name.lower()}"

    def register_type(self, type_path: str)-> str:
        if type_path not in self.registry:
            ref                      = self.create_reference_name(type_path)
            self.registry[type_path] = ref
            self.reverse[ref]        = type_path
            return ref
        return self.registry[type_path]

    def get_type(self, ref: str) -> Optional[str]:
        return self.reverse.get(ref)

    def clear(self):
        self.registry.clear()
        self.reverse.clear()
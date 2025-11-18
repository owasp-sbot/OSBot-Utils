import hashlib
import json
from typing                                                                                   import List
from osbot_utils.helpers.cache.schemas.Schema__Cache__Hash__Config                            import Schema__Cache__Hash__Config
from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.enums.Enum__Hash__Algorithm        import Enum__Hash__Algorithm
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash      import Safe_Str__Cache_Hash
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Json__Field_Path import Safe_Str__Json__Field_Path


class Cache__Hash__Generator(Type_Safe):                                           # Generate consistent hashes from various input types
    config: Schema__Cache__Hash__Config

    def calculate(self, data: bytes) -> Safe_Str__Cache_Hash:                      # Calculate hash from raw bytes
        if self.config.algorithm == Enum__Hash__Algorithm.MD5:
            hash_full = hashlib.md5(data).hexdigest()
        elif self.config.algorithm == Enum__Hash__Algorithm.SHA256:
            hash_full = hashlib.sha256(data).hexdigest()
        elif self.config.algorithm == Enum__Hash__Algorithm.SHA384:
            hash_full = hashlib.sha384(data).hexdigest()

        return Safe_Str__Cache_Hash(hash_full[:self.config.length])

    def from_string(self, data: str) -> Safe_Str__Cache_Hash:                       # Hash from string
        return self.calculate(data.encode('utf-8'))

    def from_bytes(self, data: bytes) -> Safe_Str__Cache_Hash:                      # Hash from bytes
        return self.calculate(data)

    def from_json(self, data      : dict     ,                                      # Hash JSON with optional field exclusion
                        exclude_fields: List[str] = None
                   ) -> Safe_Str__Cache_Hash:
        if exclude_fields:
            data = {k: v for k, v in data.items() if k not in exclude_fields}
        json_str = json.dumps(data, sort_keys=True)
        return self.from_string(json_str)

    def from_type_safe(self, obj           : Type_Safe     ,                      # Hash Type_Safe object
                             exclude_fields : List[str] = None
                        ) -> Safe_Str__Cache_Hash:
        return self.from_json(obj.json(), exclude_fields)

    def from_json_field(self, data      : dict,
                              json_field: Safe_Str__Json__Field_Path
                         ) -> Safe_Str__Cache_Hash:

        field_value = self.extract_field_value(data, json_field)                                                                    # Extract field value using dot notation

        if field_value is None:
            raise ValueError(f"Field '{json_field}' not found in data")

        if   isinstance(field_value, str):                      return self.from_string(           field_value )                    # Convert field value to string representation
        elif isinstance(field_value, (int, float, bool)):       return self.from_string(str       (field_value))
        elif isinstance(field_value, dict):                     return self.from_json  (           field_value )
        elif isinstance(field_value, list):                     return self.from_string(json.dumps(field_value, sort_keys=True))    # Hash the JSON representation of the list
        else:
            raise ValueError(f"Unsupported field type: {type(field_value)}")

    def extract_field_value(self, data: dict, json_field: Safe_Str__Json__Field_Path):
        parts  = json_field.split('.')
        current = data

        for part in parts:
            if not isinstance(current, dict):
                return None
            current = current.get(part)
            if current is None:
                return None

        return current
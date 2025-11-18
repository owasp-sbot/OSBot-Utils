import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__FIELD_PATH__REGEX      = re.compile(r'[^a-zA-Z0-9_\-.]')  # Allow dots for nesting
TYPE_SAFE_STR__FIELD_PATH__MAX_LENGTH = 256                              # Longer to support deep nesting

class Safe_Str__Json__Field_Path(Safe_Str):
    regex           = TYPE_SAFE_STR__FIELD_PATH__REGEX
    max_length      = TYPE_SAFE_STR__FIELD_PATH__MAX_LENGTH
    trim_whitespace = True

    def __new__(cls, value: str = None):
        if value:
            if '..' in value:                                                                       # Don't allow consecutive dots
                raise ValueError(f"Field path cannot contain consecutive dots: '{value}'")

            if value.startswith('.') or value.endswith('.'):                                        # Don't allow leading/trailing dots
                raise ValueError(f"Field path cannot start or end with a dot: '{value}'")

            segments = value.split('.')                                                             # Each segment should be non-empty after splitting
            for segment in segments:
                if not segment:
                    raise ValueError(f"Field path has empty segment: '{value}'")

        return Safe_Str.__new__(cls, value)
import re
from typing                                                                 import Optional
from osbot_utils.type_safe.Type_Safe__Primitive                             import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode

TYPE_SAFE__STR__REGEX__SAFE_STR = re.compile(r'[^a-zA-Z0-9]')    # Only allow alphanumerics and numbers
TYPE_SAFE__STR__MAX_LENGTH      = 512


class Safe_Str(Type_Safe__Primitive, str):
    allow_all_replacement_char: bool                       = True
    allow_empty               : bool                       = True                # note: making this False does cause some side effects on .json() on cases like auto serialization in environments like FastAPI (like it requires more explict value setting), so all have now been converted into a value of True
    exact_length              : bool                       = False               # If True, require exact length match, not just max length
    max_length                : int                        = TYPE_SAFE__STR__MAX_LENGTH
    regex                     : re.Pattern                 = TYPE_SAFE__STR__REGEX__SAFE_STR
    regex_mode                : Enum__Safe_Str__Regex_Mode = Enum__Safe_Str__Regex_Mode.REPLACE
    replacement_char          : str                        = '_'
    strict_validation         : bool                       = False               # If True, don't replace invalid chars, raise an error instead
    to_lower_case             : bool                       = False               # If True, convert string to lowercase
    trim_whitespace           : bool                       = False

    def __new__(cls, value: Optional[str] = None) -> 'Safe_Str':

        if value is None:                                                                                               # Validate inputs
            if cls.allow_empty:
                value = ""
            else:
                raise ValueError(f"in {cls.__name__}, value cannot be None when allow_empty is False") from None

        if not isinstance(value, str):                                                                                  # Convert to string if not already
            value = str(value)

        if cls.to_lower_case:
            value = value.lower()                                                                                       # to make this more useful do the lowercase action as soon as possible

        if cls.trim_whitespace:                                                                                         # Trim whitespace if requested
            value = value.strip()

        if not cls.allow_empty and (value is None or value == ""):                                                      # Check for empty string if not allowed
            raise ValueError(f"in {cls.__name__}, value cannot be empty when allow_empty is False")

        if cls.exact_length and len(value) and len(value) != cls.max_length:
            raise ValueError(f"in {cls.__name__}, value must be exactly {cls.max_length} characters long (was {len(value)})")
        elif not cls.exact_length and len(value) > cls.max_length:                                                      # Check max length
            raise ValueError(f"in {cls.__name__}, value exceeds maximum length of {cls.max_length} characters (was {len(value)})")

        if cls.allow_empty and value =='':
            return str.__new__(cls, '')

        sanitized_value = cls.validate_and_sanitize(value)


        return str.__new__(cls, sanitized_value)

    @classmethod
    def validate_and_sanitize(cls, value):
        if cls.strict_validation:
            if cls.regex_mode == Enum__Safe_Str__Regex_Mode.MATCH:               # For 'match' mode, regex defines the valid pattern (like version numbers)
                if not cls.regex.match(value):
                    raise ValueError(f"in {cls.__name__}, value does not match required pattern: {cls.regex.pattern}")
                return value
            elif cls.regex_mode == Enum__Safe_Str__Regex_Mode.REPLACE:           # For 'replace' mode, regex defines invalid characters to replace
                if cls.regex.search(value) is not None:
                    raise ValueError(f"in {cls.__name__}, value contains invalid characters (must not match pattern: {cls.regex.pattern})")
                return value
            else:
                raise ValueError(f"in {cls.__name__}, regex_mode value cannot be None when strict_validation is True")
        else:
            if cls.regex_mode == Enum__Safe_Str__Regex_Mode.MATCH:               # Cannot do replacement when regex defines valid pattern
                raise ValueError(f"in {cls.__name__}, cannot use regex_mode='match' without strict_validation=True")
            else:                                                                # assume the default Enum__Safe_Str__Regex_Mode.MATCH
                sanitized_value =  cls.regex.sub(cls.replacement_char, value)

                if not cls.allow_all_replacement_char and set(sanitized_value) == {
                    cls.replacement_char} and sanitized_value:
                    raise ValueError(f"in {cls.__name__}, sanitized value consists entirely of '{cls.replacement_char}' characters")

                return sanitized_value

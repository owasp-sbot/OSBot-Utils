import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__GITHUB__REPO_OWNER__REGEX = re.compile(r'[^a-zA-Z0-9\-]')
TYPE_SAFE_STR__GITHUB__REPO_OWNER__MAX_LENGTH = 39

class Safe_Str__GitHub__Repo_Owner(Safe_Str):
    """
    Safe string class for GitHub repository owners (users or organizations).

    GitHub username/organization rules:
    - May only contain alphanumeric characters or hyphens
    - Cannot have multiple consecutive hyphens
    - Cannot begin or end with a hyphen
    - Maximum length of 39 characters
    """
    regex                      = TYPE_SAFE_STR__GITHUB__REPO_OWNER__REGEX
    max_length                 = TYPE_SAFE_STR__GITHUB__REPO_OWNER__MAX_LENGTH
    allow_empty                = True
    trim_whitespace            = True
    allow_all_replacement_char = False

    def __new__(cls, value=None):
        result = super().__new__(cls, value)


        if result:                                                                                  # Additional GitHub-specific validation
            if result.startswith('-') or result.endswith('-'):                                      # Check for leading/trailing hyphens
                raise ValueError(f"in {cls.__name__}, gitHub owner name cannot start or end with a hyphen: {result}")

            if '--' in result:                                                                      # Check for consecutive hyphens
                raise ValueError(f"in {cls.__name__}, gitHub owner name cannot contain consecutive hyphens: {result}")

            if result.replace('_', '') == '':                                                       # Check for all underscores (sanitized invalid input)
                raise ValueError(f"in {cls.__name__}, invalid GitHub owner name: {result}")

        return result



import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__GITHUB__REPO_NAME__REGEX      = re.compile(r'[^a-zA-Z0-9\-_.]')
TYPE_SAFE_STR__GITHUB__REPO_NAME__MAX_LENGTH = 100

class Safe_Str__GitHub__Repo_Name(Safe_Str):
    """
    Safe string class for GitHub repository names.

    GitHub repository name rules:
    - May contain alphanumeric characters, hyphens, underscores, and periods
    - Maximum length of 100 characters
    - Cannot be empty
    """
    regex                      = TYPE_SAFE_STR__GITHUB__REPO_NAME__REGEX
    max_length                 = TYPE_SAFE_STR__GITHUB__REPO_NAME__MAX_LENGTH
    allow_empty                = True
    trim_whitespace            = True
    allow_all_replacement_char = False

    def __new__(cls, value=None):
        result = super().__new__(cls, value)

        # Additional validation
        if result:
            # Check if it's just periods (reserved names)
            if result in ['.', '..']:
                raise ValueError(f"in {cls.__name__}, invalid repository name: {result}")

            # Check for all replacement characters
            if set(result) == {'_'} and len(result) > 0:
                raise ValueError(f"in {cls.__name__}, invalid repository name: {result}")

        return result

from osbot_utils.type_safe.primitives.core.Safe_Str                                       import Safe_Str
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__SHA1        import Safe_Str__SHA1
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__SHA1__Short import Safe_Str__SHA1__Short
from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Branch          import Safe_Str__Git__Branch
from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Tag             import Safe_Str__Git__Tag

class Safe_Str__Git__Ref(Safe_Str):
    """
    Safe string class for any valid Git reference (branch, tag, or commit SHA).

    This class validates that a string is a syntactically valid Git reference
    without attempting to classify what type of reference it is.

    A value is accepted if it passes validation as ANY of:
    - A 40-character SHA (Safe_Str__SHA1)
    - A 7-character short SHA (Safe_Str__SHA1__Short)
    - A valid Git branch name (Safe_Str__Git__Branch)
    - A valid Git tag name (Safe_Str__Git__Tag)

    Used in GitHub API calls like:
    - /repos/{owner}/{repo}/zipball/{ref}
    - /repos/{owner}/{repo}/git/ref/{ref}
    - /repos/{owner}/{repo}/commits/{ref}
    """
    max_length      = 255
    allow_empty     = True
    trim_whitespace = True

    def __new__(cls, value=None):
        # First, do basic Safe_Str processing
        if value is None:
            if cls.allow_empty:
                value = ""
            else:
                raise ValueError(f"in {cls.__name__}, value cannot be None when allow_empty is False")

        if not isinstance(value, str):
            value = str(value)

        if cls.trim_whitespace:
            value = value.strip()

        if not cls.allow_empty and (value is None or value == ""):
            raise ValueError("Value cannot be empty when allow_empty is False")

        if len(value) > cls.max_length:
            raise ValueError(f"Value exceeds maximum length of {cls.max_length} characters (was {len(value)})")


        validators = [('SHA'      , Safe_Str__SHA1        ),     # we will try to validate as different ref types
                      ('short SHA', Safe_Str__SHA1__Short ),     # If ANY of these validation succeeds, accept the value
                      ('branch'   , Safe_Str__Git__Branch ),
                      ('tag'      , Safe_Str__Git__Tag    )]

        for validator_name, validator_class in validators:
            try:
                sanitized_value = validator_class(value)                                            # Validation succeeded - use the sanitized value
                return str.__new__(cls, sanitized_value)                                            # return since it is a valid ref
            except ValueError:
                continue                                                                            # This validator didn't accept it, try the next one

        raise ValueError(f"Invalid Git ref: '{value}' is not a valid SHA, branch, or tag name")     # None of the validators accepted it - it's not a valid ref
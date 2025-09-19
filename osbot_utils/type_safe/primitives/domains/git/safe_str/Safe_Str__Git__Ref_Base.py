import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


TYPE_SAFE_STR__GIT_REF__REGEX      = re.compile(r'[\x00-\x1f\x7f ~^:?*\\[\]]')

TYPE_SAFE_STR__GIT_REF__MAX_LENGTH = 255

class Safe_Str__Git__Ref_Base(Safe_Str):
    """
    Base class for Git references following git-check-ref-format rules.

    Git reference rules (from git-check-ref-format https://git-scm.com/docs/git-check-ref-format):
    1. Can include slash `/` for hierarchical grouping, but no slash-separated
       component can begin with a dot `.` or end with `.lock`
    2. Cannot have two consecutive dots `..` anywhere
    3. Cannot have ASCII control characters, space, tilde `~`, caret `^`,
       colon `:`, question-mark `?`, asterisk `*`, or open bracket `[`
    4. Cannot begin or end with a slash `/` or contain multiple consecutive slashes
    5. Cannot end with a dot `.`
    6. Cannot contain a sequence `@{`
    7. Cannot be the single character `@`
    8. Cannot contain a backslash `\`
    """
    regex                      = TYPE_SAFE_STR__GIT_REF__REGEX
    max_length                 = TYPE_SAFE_STR__GIT_REF__MAX_LENGTH
    allow_empty                = True
    trim_whitespace            = True
    allow_all_replacement_char = True

    def __new__(cls, value=None):
        result = super().__new__(cls, value)

        if result:
            # Rule: Cannot be the single character '@'
            if result == '@':
                raise ValueError(f"Reference cannot be the single character '@': {result}")

            # Rule: Cannot have two consecutive dots '..'
            if '..' in result:
                raise ValueError(f"Reference cannot contain consecutive dots '..': {result}")

            # Rule: Cannot contain sequence '@{'
            if '@{' in result:
                raise ValueError(f"Reference cannot contain '@{{': {result}")

            # Rule: Cannot begin or end with a slash
            if result.startswith('/') or result.endswith('/'):
                raise ValueError(f"Reference cannot start or end with slash: {result}")

            # Rule: Cannot contain multiple consecutive slashes
            if '//' in result:
                raise ValueError(f"Reference cannot contain consecutive slashes: {result}")

            # Rule: Cannot end with a dot
            if result.endswith('.'):
                raise ValueError(f"Reference cannot end with dot: {result}")

            # Rule: No slash-separated component can begin with '.' or end with '.lock'
            if '/' in result:
                components = result.split('/')
                for component in components:
                    if component.startswith('.'):
                        raise ValueError(f"Path component cannot start with dot: {component}")
                    if component.endswith('.lock'):
                        raise ValueError(f"Path component cannot end with '.lock': {component}")
            else:
                # Single component (no slashes)
                if result.startswith('.'):
                    raise ValueError(f"Reference cannot start with dot: {result}")
                if result.endswith('.lock'):
                    raise ValueError(f"Reference cannot end with '.lock': {result}")

        return result
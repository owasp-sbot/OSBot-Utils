from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Ref_Base import Safe_Str__Git__Ref_Base

class Safe_Str__Git__Branch(Safe_Str__Git__Ref_Base):
    """
    Safe string class for GitHub branch names.

    Follows git-check-ref-format rules with additional branch-specific restrictions:
    - Cannot start with a dash '-' (branch-specific rule)

    Examples:
    - "main", "master", "develop"
    - "feature/oauth-login"
    - "bugfix/issue-123"
    - "release/v2.0"
    """

    def __new__(cls, value=None):
        result = super().__new__(cls, value)

        if result:
            # Additional branch-specific rule: cannot start with dash
            # (from git check-ref-format --branch documentation)
            if result.startswith('-'):
                raise ValueError(f"Branch name cannot start with dash: {result}")

        return result
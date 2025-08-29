import pytest
from unittest                                                                      import TestCase
from osbot_utils.type_safe.Type_Safe__Primitive                                    import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.safe_str.Safe_Str                            import Safe_Str
from osbot_utils.type_safe.primitives.safe_str.github.Safe_Str__GitHub__Repo_Owner import Safe_Str__GitHub__Repo_Owner, TYPE_SAFE_STR__GITHUB__REPO_OWNER__MAX_LENGTH
from osbot_utils.utils.Objects                                                     import __, base_types


class test_Safe_Str__GitHub__Repo_Owner(TestCase):

    def test_Safe_Str__GitHub__Repo_Owner_class(self):
        # Valid GitHub usernames/organizations
        assert str(Safe_Str__GitHub__Repo_Owner('octocat'   )) == 'octocat'
        assert str(Safe_Str__GitHub__Repo_Owner('github'    )) == 'github'
        assert str(Safe_Str__GitHub__Repo_Owner('microsoft' )) == 'microsoft'
        assert str(Safe_Str__GitHub__Repo_Owner('owasp-sbot')) == 'owasp-sbot'
        assert str(Safe_Str__GitHub__Repo_Owner('user-123'  )) == 'user-123'
        assert str(Safe_Str__GitHub__Repo_Owner('ABC123'    )) == 'ABC123'
        assert str(Safe_Str__GitHub__Repo_Owner('a'         )) == 'a'  # Single character is valid

        # Maximum length (39 characters)
        assert str(Safe_Str__GitHub__Repo_Owner('a' * 39)) == 'a' * 39

        # Whitespace trimming
        assert str(Safe_Str__GitHub__Repo_Owner('  octocat  ')) == 'octocat'
        assert str(Safe_Str__GitHub__Repo_Owner('\toctocat\n')) == 'octocat'

        # Invalid characters get replaced
        assert str(Safe_Str__GitHub__Repo_Owner('user.name'  )) == 'user_name'
        assert str(Safe_Str__GitHub__Repo_Owner('user@github')) == 'user_github'
        assert str(Safe_Str__GitHub__Repo_Owner('user name'  )) == 'user_name'
        assert str(Safe_Str__GitHub__Repo_Owner('user/name')  ) == 'user_name'
        assert str(Safe_Str__GitHub__Repo_Owner('user_name'  )) == 'user_name'  # Underscore becomes underscore

        # Edge cases: leading/trailing hyphens
        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Owner, gitHub owner name cannot start or end with a hyphen"):
            Safe_Str__GitHub__Repo_Owner('-username')

        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Owner, gitHub owner name cannot start or end with a hyphen"):
            Safe_Str__GitHub__Repo_Owner('username-')

        # Consecutive hyphens
        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Owner, gitHub owner name cannot contain consecutive hyphens"):
            Safe_Str__GitHub__Repo_Owner('user--name')

        # Empty or None
        #with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Owner, value cannot be None when allow_empty is False"):
        assert Safe_Str__GitHub__Repo_Owner(None) == ''

        #with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Owner, value cannot be empty when allow_empty is False"):
        assert Safe_Str__GitHub__Repo_Owner('') == ''

        # Exceeds max length
        with pytest.raises(ValueError, match=f"in Safe_Str__GitHub__Repo_Owner, value exceeds maximum length of {TYPE_SAFE_STR__GITHUB__REPO_OWNER__MAX_LENGTH}"):
            Safe_Str__GitHub__Repo_Owner('a' * 40)

        # All invalid characters
        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Owner, sanitized value consists entirely of '_' characters"):
            Safe_Str__GitHub__Repo_Owner('!@#$%')

    def test_inheritance(self):
        owner = Safe_Str__GitHub__Repo_Owner('octocat')
        assert isinstance(owner, Safe_Str__GitHub__Repo_Owner)
        assert isinstance(owner, Safe_Str)
        assert isinstance(owner, Type_Safe__Primitive)
        assert isinstance(owner, str)
        assert base_types(owner) == [Safe_Str, Type_Safe__Primitive, str, object, object]





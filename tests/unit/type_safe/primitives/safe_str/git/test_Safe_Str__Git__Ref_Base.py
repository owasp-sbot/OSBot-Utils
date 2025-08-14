import pytest
from unittest                                                              import TestCase
from osbot_utils.type_safe.Type_Safe                                       import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                            import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.safe_str.Safe_Str                    import Safe_Str
from osbot_utils.type_safe.primitives.safe_str.git.Safe_Str__Git__Ref_Base import Safe_Str__Git__Ref_Base, TYPE_SAFE_STR__GIT_REF__MAX_LENGTH
from osbot_utils.utils.Objects                                             import __, base_types


class test_Safe_Str__Git__Ref_Base(TestCase):
    """Test the base Git reference validation following git-check-ref-format rules."""

    def test_valid_git_refs(self):
        """Test valid Git reference patterns."""
        # Simple valid refs
        assert str(Safe_Str__Git__Ref_Base('main')) == 'main'
        assert str(Safe_Str__Git__Ref_Base('master')) == 'master'
        assert str(Safe_Str__Git__Ref_Base('develop')) == 'develop'
        assert str(Safe_Str__Git__Ref_Base('v1.0.0')) == 'v1.0.0'
        assert str(Safe_Str__Git__Ref_Base('release-1.0')) == 'release-1.0'

        # Refs with slashes (hierarchical)
        assert str(Safe_Str__Git__Ref_Base('feature/new-feature')) == 'feature/new-feature'
        assert str(Safe_Str__Git__Ref_Base('bugfix/issue-123')) == 'bugfix/issue-123'
        assert str(Safe_Str__Git__Ref_Base('release/v2.0')) == 'release/v2.0'
        assert str(Safe_Str__Git__Ref_Base('users/john/feature')) == 'users/john/feature'

        # Refs with dots (but not violating rules)
        assert str(Safe_Str__Git__Ref_Base('v1.2.3')) == 'v1.2.3'
        assert str(Safe_Str__Git__Ref_Base('release.final')) == 'release.final'
        assert str(Safe_Str__Git__Ref_Base('my.branch.name')) == 'my.branch.name'

        # Refs with underscores and hyphens
        assert str(Safe_Str__Git__Ref_Base('my_branch')) == 'my_branch'
        assert str(Safe_Str__Git__Ref_Base('my-branch')) == 'my-branch'
        assert str(Safe_Str__Git__Ref_Base('my_branch-123')) == 'my_branch-123'

        # Numeric refs
        assert str(Safe_Str__Git__Ref_Base('123')) == '123'
        assert str(Safe_Str__Git__Ref_Base('2024')) == '2024'
        assert str(Safe_Str__Git__Ref_Base('3.14159')) == '3.14159'

        # Mixed case
        assert str(Safe_Str__Git__Ref_Base('MyBranch')) == 'MyBranch'
        assert str(Safe_Str__Git__Ref_Base('UPPERCASE')) == 'UPPERCASE'
        assert str(Safe_Str__Git__Ref_Base('camelCase')) == 'camelCase'

        # Refs starting with dash (allowed for tags, but not branches)
        # Note: Git__Ref_Base allows this, Git__Branch would reject it
        assert str(Safe_Str__Git__Ref_Base('-tag')) == '-tag'
        assert str(Safe_Str__Git__Ref_Base('-v1.0')) == '-v1.0'

        # Whitespace trimming
        assert str(Safe_Str__Git__Ref_Base('  main  ')) == 'main'
        assert str(Safe_Str__Git__Ref_Base('\ttag\n')) == 'tag'

    def test_invalid_git_refs_special_chars(self):
        """Test that forbidden characters are replaced with underscore."""
        # Space
        assert str(Safe_Str__Git__Ref_Base('my branch')) == 'my_branch'
        assert str(Safe_Str__Git__Ref_Base('feature name')) == 'feature_name'

        # Tilde
        assert str(Safe_Str__Git__Ref_Base('branch~1')) == 'branch_1'
        assert str(Safe_Str__Git__Ref_Base('~temp')) == '_temp'

        # Caret
        assert str(Safe_Str__Git__Ref_Base('branch^')) == 'branch_'
        assert str(Safe_Str__Git__Ref_Base('tag^2')) == 'tag_2'

        # Colon
        assert str(Safe_Str__Git__Ref_Base('branch:name')) == 'branch_name'
        assert str(Safe_Str__Git__Ref_Base('origin:master')) == 'origin_master'

        # Question mark
        assert str(Safe_Str__Git__Ref_Base('branch?')) == 'branch_'
        assert str(Safe_Str__Git__Ref_Base('what?')) == 'what_'

        # Asterisk
        assert str(Safe_Str__Git__Ref_Base('branch*')) == 'branch_'
        assert str(Safe_Str__Git__Ref_Base('*temp*')) == '_temp_'

        # Square brackets
        assert str(Safe_Str__Git__Ref_Base('branch[1]')) == 'branch_1_'
        assert str(Safe_Str__Git__Ref_Base('[tag]')) == '_tag_'

        # Backslash
        assert str(Safe_Str__Git__Ref_Base('branch\\name')) == 'branch_name'
        assert str(Safe_Str__Git__Ref_Base('path\\to\\ref')) == 'path_to_ref'

        # Control characters
        assert str(Safe_Str__Git__Ref_Base('branch\x00name')) == 'branch_name'
        assert str(Safe_Str__Git__Ref_Base('branch\x1fname')) == 'branch_name'
        assert str(Safe_Str__Git__Ref_Base('branch\x7fname')) == 'branch_name'

    def test_invalid_git_refs_structural_rules(self):
        """Test structural rules that should raise exceptions."""

        # Rule: Cannot be the single character '@'
        with pytest.raises(ValueError, match="Reference cannot be the single character '@'"):
            Safe_Str__Git__Ref_Base('@')

        # Rule: Cannot contain consecutive dots '..'
        with pytest.raises(ValueError, match="Reference cannot contain consecutive dots"):
            Safe_Str__Git__Ref_Base('branch..name')
        with pytest.raises(ValueError, match="Reference cannot contain consecutive dots"):
            Safe_Str__Git__Ref_Base('..leading')
        with pytest.raises(ValueError, match="Reference cannot contain consecutive dots"):
            Safe_Str__Git__Ref_Base('trailing..')

        # Rule: Cannot contain '@{'
        with pytest.raises(ValueError, match="Reference cannot contain '@{'"):
            Safe_Str__Git__Ref_Base('branch@{1}')
        with pytest.raises(ValueError, match="Reference cannot contain '@{'"):
            Safe_Str__Git__Ref_Base('HEAD@{upstream}')

        # Rule: Cannot start with slash
        with pytest.raises(ValueError, match="Reference cannot start or end with slash"):
            Safe_Str__Git__Ref_Base('/branch')
        with pytest.raises(ValueError, match="Reference cannot start or end with slash"):
            Safe_Str__Git__Ref_Base('/feature/branch')

        # Rule: Cannot end with slash
        with pytest.raises(ValueError, match="Reference cannot start or end with slash"):
            Safe_Str__Git__Ref_Base('branch/')
        with pytest.raises(ValueError, match="Reference cannot start or end with slash"):
            Safe_Str__Git__Ref_Base('feature/branch/')

        # Rule: Cannot have consecutive slashes
        with pytest.raises(ValueError, match="Reference cannot contain consecutive slashes"):
            Safe_Str__Git__Ref_Base('feature//branch')
        with pytest.raises(ValueError, match="Reference cannot contain consecutive slashes"):
            Safe_Str__Git__Ref_Base('a///b')

        # Rule: Cannot end with dot
        with pytest.raises(ValueError, match="Reference cannot end with dot"):
            Safe_Str__Git__Ref_Base('branch.')
        with pytest.raises(ValueError, match="Reference cannot end with dot"):
            Safe_Str__Git__Ref_Base('v1.0.')

    def test_invalid_git_refs_path_components(self):
        """Test rules for slash-separated path components."""

        # Rule: Path component cannot start with dot
        with pytest.raises(ValueError, match="Path component cannot start with dot"):
            Safe_Str__Git__Ref_Base('feature/.hidden')
        with pytest.raises(ValueError, match="Path component cannot start with dot"):
            Safe_Str__Git__Ref_Base('a/b/.c')
        with pytest.raises(ValueError, match="Path component cannot start with dot"):
            Safe_Str__Git__Ref_Base('.hidden/feature')

        # Rule: Path component cannot end with .lock
        with pytest.raises(ValueError, match="Path component cannot end with '.lock'"):
            Safe_Str__Git__Ref_Base('feature/branch.lock')
        with pytest.raises(ValueError, match="Path component cannot end with '.lock'"):
            Safe_Str__Git__Ref_Base('a/b.lock/c')
        with pytest.raises(ValueError, match="Path component cannot end with '.lock'"):
            Safe_Str__Git__Ref_Base('branch.lock/feature')

    def test_invalid_git_refs_single_component(self):
        """Test rules for refs without slashes (single component)."""

        # Rule: Single component cannot start with dot
        with pytest.raises(ValueError, match="Reference cannot start with dot"):
            Safe_Str__Git__Ref_Base('.branch')
        with pytest.raises(ValueError, match="Reference cannot start with dot"):
            Safe_Str__Git__Ref_Base('.tag')

        # Rule: Single component cannot end with .lock
        with pytest.raises(ValueError, match="Reference cannot end with '.lock'"):
            Safe_Str__Git__Ref_Base('branch.lock')
        with pytest.raises(ValueError, match="Reference cannot end with '.lock'"):
            Safe_Str__Git__Ref_Base('master.lock')

    def test_empty_and_none(self):
        """Test empty and None values."""
        with pytest.raises(ValueError, match="in Safe_Str__Git__Ref_Base, value cannot be None when allow_empty is False"):
            Safe_Str__Git__Ref_Base(None)

        with pytest.raises(ValueError, match="Value cannot be empty when allow_empty is False"):
            Safe_Str__Git__Ref_Base('')

        with pytest.raises(ValueError, match="Value cannot be empty when allow_empty is False"):
            Safe_Str__Git__Ref_Base('   ')  # Just whitespace (gets trimmed)

    def test_max_length(self):
        """Test maximum length constraint."""
        # Valid: exactly at max length
        max_ref = 'a' * TYPE_SAFE_STR__GIT_REF__MAX_LENGTH
        assert str(Safe_Str__Git__Ref_Base(max_ref)) == max_ref

        # Invalid: exceeds max length
        with pytest.raises(ValueError, match=f"Value exceeds maximum length of {TYPE_SAFE_STR__GIT_REF__MAX_LENGTH}"):
            Safe_Str__Git__Ref_Base('a' * (TYPE_SAFE_STR__GIT_REF__MAX_LENGTH + 1))

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Single character refs (valid)
        assert str(Safe_Str__Git__Ref_Base('a')) == 'a'
        assert str(Safe_Str__Git__Ref_Base('1')) == '1'
        assert str(Safe_Str__Git__Ref_Base('-')) == '-'
        assert str(Safe_Str__Git__Ref_Base('_')) == '_'

        # Two character refs with dots (valid if not consecutive)
        assert str(Safe_Str__Git__Ref_Base('a.b')) == 'a.b'
        assert str(Safe_Str__Git__Ref_Base('1.2')) == '1.2'

        # @ symbol in various positions (valid except as single char)
        assert str(Safe_Str__Git__Ref_Base('@branch')) == '@branch'
        assert str(Safe_Str__Git__Ref_Base('branch@')) == 'branch@'
        assert str(Safe_Str__Git__Ref_Base('bra@nch')) == 'bra@nch'

        # Complex valid patterns
        assert str(Safe_Str__Git__Ref_Base('refs/heads/main')) == 'refs/heads/main'
        assert str(Safe_Str__Git__Ref_Base('refs/tags/v1.0.0')) == 'refs/tags/v1.0.0'
        assert str(Safe_Str__Git__Ref_Base('refs/remotes/origin/master')) == 'refs/remotes/origin/master'

    def test_inheritance(self):
        """Test class inheritance chain."""
        ref = Safe_Str__Git__Ref_Base('main')
        assert isinstance(ref, Safe_Str__Git__Ref_Base)
        assert isinstance(ref, Safe_Str)
        assert isinstance(ref, Type_Safe__Primitive)
        assert isinstance(ref, str)
        assert base_types(ref) == [Safe_Str, Type_Safe__Primitive, str, object, object]

    def test_usage_in_Type_Safe(self):
        """Test integration with Type_Safe classes."""
        class Git_Config(Type_Safe):
            default_ref: Safe_Str__Git__Ref_Base  = Safe_Str__Git__Ref_Base('main')
            tracking_ref: Safe_Str__Git__Ref_Base = None

        # Test instantiation with default
        config = Git_Config()
        assert str(config.default_ref) == 'main'
        assert str(config.tracking_ref) == 'None'
        assert type(config.default_ref) is Safe_Str__Git__Ref_Base

        # Test updating
        config.tracking_ref = Safe_Str__Git__Ref_Base('origin/develop')
        assert str(config.tracking_ref) == 'origin/develop'

        # Test serialization
        config_json = config.json()
        assert config_json == {
            'default_ref': 'main',
            'tracking_ref': 'origin/develop'
        }

        # Round trip test
        config_round_trip = Git_Config.from_json(config_json)
        assert config_round_trip.obj() == config.obj()
        assert type(config_round_trip.default_ref) is Safe_Str__Git__Ref_Base
        assert type(config_round_trip.tracking_ref) is Safe_Str__Git__Ref_Base

    def test_string_representation(self):
        """Test string representation methods."""
        ref = Safe_Str__Git__Ref_Base('feature/new-feature')
        assert str(ref) == 'feature/new-feature'
        assert f'Branch: {ref}' == 'Branch: feature/new-feature'
        assert repr(ref) == "Safe_Str__Git__Ref_Base('feature/new-feature')"

        # With sanitization
        ref_sanitized = Safe_Str__Git__Ref_Base('my branch')
        assert str(ref_sanitized) == 'my_branch'
        assert repr(ref_sanitized) == "Safe_Str__Git__Ref_Base('my_branch')"

    def test_realistic_git_refs(self):
        """Test with realistic Git reference patterns."""
        # Standard Git refs paths
        assert str(Safe_Str__Git__Ref_Base('refs/heads/master')) == 'refs/heads/master'
        assert str(Safe_Str__Git__Ref_Base('refs/tags/v1.0.0')) == 'refs/tags/v1.0.0'
        assert str(Safe_Str__Git__Ref_Base('refs/remotes/origin/main')) == 'refs/remotes/origin/main'
        assert str(Safe_Str__Git__Ref_Base('refs/pull/123/head')) == 'refs/pull/123/head'
        assert str(Safe_Str__Git__Ref_Base('refs/merge-requests/456/head')) == 'refs/merge-requests/456/head'

        # Stash refs
        assert str(Safe_Str__Git__Ref_Base('refs/stash')) == 'refs/stash'

        # Notes refs
        assert str(Safe_Str__Git__Ref_Base('refs/notes/commits')) == 'refs/notes/commits'

        # Bisect refs
        assert str(Safe_Str__Git__Ref_Base('refs/bisect/bad')) == 'refs/bisect/bad'
        assert str(Safe_Str__Git__Ref_Base('refs/bisect/good-abc1234')) == 'refs/bisect/good-abc1234'
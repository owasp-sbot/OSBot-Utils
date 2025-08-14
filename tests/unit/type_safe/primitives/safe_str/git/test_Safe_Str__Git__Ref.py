import pytest
from unittest                                                                            import TestCase
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                          import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.safe_str.Safe_Str                                  import Safe_Str
from osbot_utils.type_safe.primitives.safe_str.cryptography.hashes.Safe_Str__SHA1        import Safe_Str__SHA1
from osbot_utils.type_safe.primitives.safe_str.cryptography.hashes.Safe_Str__SHA1__Short import Safe_Str__SHA1__Short
from osbot_utils.type_safe.primitives.safe_str.git.Safe_Str__Git__Branch                 import Safe_Str__Git__Branch
from osbot_utils.type_safe.primitives.safe_str.git.Safe_Str__Git__Ref                    import Safe_Str__Git__Ref
from osbot_utils.type_safe.primitives.safe_str.git.Safe_Str__Git__Tag                    import Safe_Str__Git__Tag
from osbot_utils.utils.Objects                                                           import base_types


class test_Safe_Str__Git__Ref(TestCase):
    """Test the general ref class that accepts any valid ref type."""
    
    def test_accepts_all_ref_types(self):
        """Test that all valid ref types are accepted."""
        # Full SHA (40 hex chars)
        ref = Safe_Str__Git__Ref('7fd1a60b01f91b314f59955a4e4d4e80d8edf11d')
        assert str(ref) == '7fd1a60b01f91b314f59955a4e4d4e80d8edf11d'

        # Short SHA (7 hex chars)
        ref = Safe_Str__Git__Ref('abc1234')
        assert str(ref) == 'abc1234'

        # Branch names
        ref = Safe_Str__Git__Ref('main')
        assert str(ref) == 'main'

        ref = Safe_Str__Git__Ref('feature/oauth')
        assert str(ref) == 'feature/oauth'

        ref = Safe_Str__Git__Ref('develop')
        assert str(ref) == 'develop'

        # Tag names
        ref = Safe_Str__Git__Ref('v1.0.0')
        assert str(ref) == 'v1.0.0'

        ref = Safe_Str__Git__Ref('release-2.0')
        assert str(ref) == 'release-2.0'

        # Tags can start with dash (branches cannot)
        ref = Safe_Str__Git__Ref('-tag')
        assert str(ref) == '-tag'

    def test_validation_through_specialized_classes(self):
        """Test that invalid refs are rejected."""
        # Invalid refs that fail all validators
        with pytest.raises(ValueError, match="Invalid Git ref"):
            Safe_Str__Git__Ref('.hidden')  # Can't start with period

        with pytest.raises(ValueError, match="Invalid Git ref"):
            Safe_Str__Git__Ref('branch.lock')  # Can't end with .lock

        with pytest.raises(ValueError, match="Invalid Git ref"):
            Safe_Str__Git__Ref('feature//oauth')  # No consecutive slashes

        with pytest.raises(ValueError, match="Invalid Git ref"):
            Safe_Str__Git__Ref('branch..name')  # Consecutive dots

        with pytest.raises(ValueError, match="Invalid Git ref"):
            Safe_Str__Git__Ref('@')  # Single @ character

        with pytest.raises(ValueError, match="Invalid Git ref"):
            Safe_Str__Git__Ref('branch@{1}')  # Contains @{

        # Empty or None
        with pytest.raises(ValueError, match="in Safe_Str__Git__Ref, value cannot be None when allow_empty is False"):
            Safe_Str__Git__Ref(None)

        with pytest.raises(ValueError, match="Value cannot be empty when allow_empty is False"):
            Safe_Str__Git__Ref('')

    def test_usage_in_github_api(self):
        """Test usage in GitHub API path construction."""
        owner = 'octocat'
        repo = 'Hello-World'

        # Test with branch-like ref
        ref = Safe_Str__Git__Ref('main')
        path = f'/repos/{owner}/{repo}/zipball/{ref}'
        assert path == '/repos/octocat/Hello-World/zipball/main'

        # Test with tag-like ref
        ref = Safe_Str__Git__Ref('v1.0.0')
        path = f'/repos/{owner}/{repo}/zipball/{ref}'
        assert path == '/repos/octocat/Hello-World/zipball/v1.0.0'

        # Test with short SHA
        ref = Safe_Str__Git__Ref('7fd1a60')
        path = f'/repos/{owner}/{repo}/zipball/{ref}'
        assert path == '/repos/octocat/Hello-World/zipball/7fd1a60'

        # Test with full SHA
        ref = Safe_Str__Git__Ref('7fd1a60b01f91b314f59955a4e4d4e80d8edf11d')
        path = f'/repos/{owner}/{repo}/commits/{ref}'
        assert path == '/repos/octocat/Hello-World/commits/7fd1a60b01f91b314f59955a4e4d4e80d8edf11d'

    def test_usage_in_Type_Safe(self):
        """Test integration with Type_Safe classes."""
        class GitHub_Deploy_Config(Type_Safe):
            source_ref  : Safe_Str__Git__Ref     = Safe_Str__Git__Ref('main')
            target_sha  : Safe_Str__SHA1         = None
            short_sha   : Safe_Str__SHA1__Short  = None
            branch      : Safe_Str__Git__Branch  = None
            tag         : Safe_Str__Git__Tag     = None

        # Test instantiation
        config = GitHub_Deploy_Config()
        assert str(config.source_ref) == 'main'

        # Set specific types
        config.target_sha = Safe_Str__SHA1('7fd1a60b01f91b314f59955a4e4d4e80d8edf11d')
        config.short_sha  = Safe_Str__SHA1__Short('abc1234')
        config.branch     = Safe_Str__Git__Branch('develop')
        config.tag        = Safe_Str__Git__Tag('v2.0.0')

        assert str(config.target_sha) == '7fd1a60b01f91b314f59955a4e4d4e80d8edf11d'
        assert str(config.short_sha) == 'abc1234'
        assert str(config.branch) == 'develop'
        assert str(config.tag) == 'v2.0.0'

        # Test serialization
        config_json = config.json()
        assert config_json == {
            'source_ref': 'main',
            'target_sha': '7fd1a60b01f91b314f59955a4e4d4e80d8edf11d',
            'short_sha': 'abc1234',
            'branch': 'develop',
            'tag': 'v2.0.0'
        }

        # Round trip test
        config_round_trip = GitHub_Deploy_Config.from_json(config_json)
        assert config_round_trip.obj() == config.obj()
        assert type(config_round_trip.source_ref) is Safe_Str__Git__Ref
        assert type(config_round_trip.target_sha) is Safe_Str__SHA1
        assert type(config_round_trip.short_sha) is Safe_Str__SHA1__Short
        assert type(config_round_trip.branch) is Safe_Str__Git__Branch
        assert type(config_round_trip.tag) is Safe_Str__Git__Tag

    def test_inheritance(self):
        """Test class inheritance chains."""
        # General ref
        ref = Safe_Str__Git__Ref('main')
        assert isinstance(ref, Safe_Str__Git__Ref)
        assert isinstance(ref, Safe_Str)
        assert base_types(ref) == [Safe_Str, Type_Safe__Primitive, str, object, object]

        # SHA
        sha = Safe_Str__SHA1('7fd1a60b01f91b314f59955a4e4d4e80d8edf11d')
        assert isinstance(sha, Safe_Str__SHA1)
        assert isinstance(sha, Safe_Str)
        assert base_types(sha) == [Safe_Str, Type_Safe__Primitive, str, object, object]

        # Short SHA
        short_sha = Safe_Str__SHA1__Short('abc1234')
        assert isinstance(short_sha, Safe_Str__SHA1__Short)
        assert isinstance(short_sha, Safe_Str)

        # Branch
        branch = Safe_Str__Git__Branch('develop')
        assert isinstance(branch, Safe_Str__Git__Branch)
        assert isinstance(branch, Safe_Str)

        # Tag
        tag = Safe_Str__Git__Tag('v1.0.0')
        assert isinstance(tag, Safe_Str__Git__Tag)
        assert isinstance(tag, Safe_Str)

    def test_string_representation(self):
        """Test string representation methods."""
        # SHA
        sha = Safe_Str__SHA1('7fd1a60b01f91b314f59955a4e4d4e80d8edf11d')
        assert str(sha) == '7fd1a60b01f91b314f59955a4e4d4e80d8edf11d'
        assert f'Commit: {sha}' == 'Commit: 7fd1a60b01f91b314f59955a4e4d4e80d8edf11d'
        assert repr(sha) == "Safe_Str__SHA1('7fd1a60b01f91b314f59955a4e4d4e80d8edf11d')"

        # Short SHA
        short_sha = Safe_Str__SHA1__Short('abc1234')
        assert str(short_sha) == 'abc1234'
        assert repr(short_sha) == "Safe_Str__SHA1__Short('abc1234')"

        # Branch
        branch = Safe_Str__Git__Branch('develop')
        assert str(branch) == 'develop'
        assert repr(branch) == "Safe_Str__Git__Branch('develop')"

        # Tag
        tag = Safe_Str__Git__Tag('v1.0.0')
        assert str(tag) == 'v1.0.0'
        assert repr(tag) == "Safe_Str__Git__Tag('v1.0.0')"

        # General ref
        ref = Safe_Str__Git__Ref('main')
        assert str(ref) == 'main'
        assert repr(ref) == "Safe_Str__Git__Ref('main')"

    def test_edge_cases(self):
        """Test edge cases and ambiguous refs."""
        # Branch that looks like a short SHA but has non-hex chars
        ref = Safe_Str__Git__Ref('main123')  # Has 'main' which is not all hex
        assert str(ref) == 'main123'

        # Valid branch name that happens to be 5 hex chars
        ref = Safe_Str__Git__Ref('abc12')
        assert str(ref) == 'abc12'

        # Branch that's 7 chars but contains non-hex
        ref = Safe_Str__Git__Ref('abc123g')
        assert str(ref) == 'abc123g'

        # Numeric branch name
        ref = Safe_Str__Git__Ref('2024')
        assert str(ref) == '2024'

        # Common names that could be either branch or tag
        ref = Safe_Str__Git__Ref('stable')
        assert str(ref) == 'stable'

        ref = Safe_Str__Git__Ref('latest')
        assert str(ref) == 'latest'

        ref = Safe_Str__Git__Ref('beta')
        assert str(ref) == 'beta'

    def test_character_sanitization(self):
        """Test that invalid characters get sanitized consistently."""
        # Spaces get replaced with underscores
        ref = Safe_Str__Git__Ref('my branch')
        assert str(ref) == 'my_branch'

        # Special characters get replaced
        ref = Safe_Str__Git__Ref('branch~name')
        assert str(ref) == 'branch_name'

        ref = Safe_Str__Git__Ref('branch^name')
        assert str(ref) == 'branch_name'

        ref = Safe_Str__Git__Ref('branch:name')
        assert str(ref) == 'branch_name'

    def test_whitespace_handling(self):
        """Test whitespace trimming."""
        ref = Safe_Str__Git__Ref('  main  ')
        assert str(ref) == 'main'

        ref = Safe_Str__Git__Ref('\tdevelop\n')
        assert str(ref) == 'develop'

        ref = Safe_Str__Git__Ref('  v1.0.0  ')
        assert str(ref) == 'v1.0.0'
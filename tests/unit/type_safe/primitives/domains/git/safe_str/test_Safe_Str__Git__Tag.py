import pytest
from unittest                                                                  import TestCase
from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Tag  import Safe_Str__Git__Tag


class test_Safe_Str__Git__Tag(TestCase):                        # Test tag name validation following git-check-ref-format rules.

    def test_valid_tag_names(self):
        # Version tags
        assert str(Safe_Str__Git__Tag('v1.0.0')) == 'v1.0.0'
        assert str(Safe_Str__Git__Tag('v2.3.4')) == 'v2.3.4'
        assert str(Safe_Str__Git__Tag('v1.0')) == 'v1.0'
        assert str(Safe_Str__Git__Tag('v1')) == 'v1'

        # Release tags
        assert str(Safe_Str__Git__Tag('release-1.0.0')) == 'release-1.0.0'
        assert str(Safe_Str__Git__Tag('release/2.0')) == 'release/2.0'

        # Date-based tags
        assert str(Safe_Str__Git__Tag('2024.01.15')) == '2024.01.15'
        assert str(Safe_Str__Git__Tag('2024-01-15')) == '2024-01-15'

        # Other tag formats
        assert str(Safe_Str__Git__Tag('stable')) == 'stable'
        assert str(Safe_Str__Git__Tag('latest')) == 'latest'
        assert str(Safe_Str__Git__Tag('beta-1')) == 'beta-1'
        assert str(Safe_Str__Git__Tag('alpha.2')) == 'alpha.2'

        # Tags CAN start with dash (unlike branches)
        assert str(Safe_Str__Git__Tag('-tag')) == '-tag'
        assert str(Safe_Str__Git__Tag('-v1.0')) == '-v1.0'

        # Whitespace trimming
        assert str(Safe_Str__Git__Tag('  v1.0.0  ')) == 'v1.0.0'

    def test_invalid_tag_names_git_rules(self):
        # Cannot be single '@'
        with pytest.raises(ValueError, match="Reference cannot be the single character '@'"):
            Safe_Str__Git__Tag('@')

        # Cannot have consecutive dots
        with pytest.raises(ValueError, match="Reference cannot contain consecutive dots"):
            Safe_Str__Git__Tag('tag..name')

        # Cannot contain '@{'
        with pytest.raises(ValueError, match="Reference cannot contain '@{'"):
            Safe_Str__Git__Tag('tag@{1}')

        # Cannot end with dot
        with pytest.raises(ValueError, match="Reference cannot end with dot"):
            Safe_Str__Git__Tag('tag.')

        # Path component cannot start with dot
        with pytest.raises(ValueError, match="Path component cannot start with dot"):
            Safe_Str__Git__Tag('release/.hidden')

        # Path component cannot end with .lock
        with pytest.raises(ValueError, match="Path component cannot end with '.lock'"):
            Safe_Str__Git__Tag('release/v1.lock')

        # Single component cannot start with dot
        with pytest.raises(ValueError, match="Reference cannot start with dot"):
            Safe_Str__Git__Tag('.tag')

        # Single component cannot end with .lock
        with pytest.raises(ValueError, match="Reference cannot end with '.lock'"):
            Safe_Str__Git__Tag('tag.lock')

        # Cannot have consecutive slashes
        with pytest.raises(ValueError, match="Reference cannot contain consecutive slashes"):
            Safe_Str__Git__Tag('release//v1')

        # Cannot start with slash
        with pytest.raises(ValueError, match="Reference cannot start or end with slash"):
            Safe_Str__Git__Tag('/tag')

        # Cannot end with slash
        with pytest.raises(ValueError, match="Reference cannot start or end with slash"):
            Safe_Str__Git__Tag('tag/')

        # Empty or None
        #with pytest.raises(ValueError, match="in Safe_Str__Git__Tag, value cannot be None when allow_empty is False"):
        assert Safe_Str__Git__Tag(None) == ''

        #with pytest.raises(ValueError, match="in Safe_Str__Git__Tag, value cannot be empty when allow_empty is False"):
        assert Safe_Str__Git__Tag('') == ''

    def test_tag_forbidden_characters(self):
        # Test forbidden characters (should be replaced with _)
        assert str(Safe_Str__Git__Tag('my tag')) == 'my_tag'  # space
        assert str(Safe_Str__Git__Tag('tag~name')) == 'tag_name'  # tilde
        assert str(Safe_Str__Git__Tag('tag^name')) == 'tag_name'  # caret
        assert str(Safe_Str__Git__Tag('tag:name')) == 'tag_name'  # colon
        assert str(Safe_Str__Git__Tag('tag?name')) == 'tag_name'  # question
        assert str(Safe_Str__Git__Tag('tag*name')) == 'tag_name'  # asterisk
        assert str(Safe_Str__Git__Tag('tag[name]')) == 'tag_name_'  # brackets




import pytest
from unittest                                                                    import TestCase
from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Branch import Safe_Str__Git__Branch


class test_Safe_Str__Git__Branch(TestCase):         # Test branch name validation following git-check-ref-format rules.

    def test_valid_branch_names(self):
        # Common branch names
        assert str(Safe_Str__Git__Branch('main')) == 'main'
        assert str(Safe_Str__Git__Branch('master')) == 'master'
        assert str(Safe_Str__Git__Branch('develop')) == 'develop'
        assert str(Safe_Str__Git__Branch('staging')) == 'staging'

        # Feature branches
        assert str(Safe_Str__Git__Branch('feature/oauth-login')) == 'feature/oauth-login'
        assert str(Safe_Str__Git__Branch('feature/JIRA-1234')) == 'feature/JIRA-1234'

        # Branches with various valid characters
        assert str(Safe_Str__Git__Branch('my-branch')) == 'my-branch'
        assert str(Safe_Str__Git__Branch('my_branch')) == 'my_branch'
        assert str(Safe_Str__Git__Branch('my.branch')) == 'my.branch'
        assert str(Safe_Str__Git__Branch('branch-123')) == 'branch-123'
        assert str(Safe_Str__Git__Branch('123-branch')) == '123-branch'  # Can start with number

        # Nested branches
        assert str(Safe_Str__Git__Branch('feature/team/oauth')) == 'feature/team/oauth'
        assert str(Safe_Str__Git__Branch('bugfix/2024/security')) == 'bugfix/2024/security'

        # Whitespace trimming
        assert str(Safe_Str__Git__Branch('  main  ')) == 'main'

    def test_invalid_branch_names_git_rules(self):
        # Branch-specific: Cannot start with dash
        with pytest.raises(ValueError, match="Branch name cannot start with dash"):
            Safe_Str__Git__Branch('-branch')

        # Cannot be single '@'
        with pytest.raises(ValueError, match="Reference cannot be the single character '@'"):
            Safe_Str__Git__Branch('@')

        # Cannot have consecutive dots
        with pytest.raises(ValueError, match="Reference cannot contain consecutive dots"):
            Safe_Str__Git__Branch('branch..name')

        # Cannot contain '@{'
        with pytest.raises(ValueError, match="Reference cannot contain '@{'"):
            Safe_Str__Git__Branch('branch@{1}')

        # Cannot end with dot
        with pytest.raises(ValueError, match="Reference cannot end with dot"):
            Safe_Str__Git__Branch('branch.')

        # Path component cannot start with dot
        with pytest.raises(ValueError, match="Path component cannot start with dot"):
            Safe_Str__Git__Branch('feature/.hidden')

        # Path component cannot end with .lock
        with pytest.raises(ValueError, match="Path component cannot end with '.lock'"):
            Safe_Str__Git__Branch('feature/branch.lock')

        # Single component cannot start with dot
        with pytest.raises(ValueError, match="Reference cannot start with dot"):
            Safe_Str__Git__Branch('.branch')

        # Single component cannot end with .lock
        with pytest.raises(ValueError, match="Reference cannot end with '.lock'"):
            Safe_Str__Git__Branch('branch.lock')

        # Cannot have consecutive slashes
        with pytest.raises(ValueError, match="Reference cannot contain consecutive slashes"):
            Safe_Str__Git__Branch('feature//login')

        # Cannot start with slash
        with pytest.raises(ValueError, match="Reference cannot start or end with slash"):
            Safe_Str__Git__Branch('/branch')

        # Cannot end with slash
        with pytest.raises(ValueError, match="Reference cannot start or end with slash"):
            Safe_Str__Git__Branch('branch/')

        # Empty or None
        #with pytest.raises(ValueError, match="in Safe_Str__Git__Branch, value cannot be None when allow_empty is False"):
        assert Safe_Str__Git__Branch(None) == ''

        #with pytest.raises(ValueError, match="in Safe_Str__Git__Branch, value cannot be empty when allow_empty is False"):
        assert Safe_Str__Git__Branch('') == ''

    def test_branch_forbidden_characters(self):
        # Test forbidden characters (should be replaced with _)
        assert str(Safe_Str__Git__Branch('my branch')) == 'my_branch'  # space
        assert str(Safe_Str__Git__Branch('branch~name')) == 'branch_name'  # tilde
        assert str(Safe_Str__Git__Branch('branch^name')) == 'branch_name'  # caret
        assert str(Safe_Str__Git__Branch('branch:name')) == 'branch_name'  # colon
        assert str(Safe_Str__Git__Branch('branch?name')) == 'branch_name'  # question
        assert str(Safe_Str__Git__Branch('branch*name')) == 'branch_name'  # asterisk
        assert str(Safe_Str__Git__Branch('branch[name]')) == 'branch_name_'  # brackets

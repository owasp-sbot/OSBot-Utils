import pytest
from unittest                                                                     import TestCase
from osbot_utils.type_safe.primitives.safe_str.github.Safe_Str__GitHub__Repo_Name import Safe_Str__GitHub__Repo_Name, TYPE_SAFE_STR__GITHUB__REPO_NAME__MAX_LENGTH


class test_Safe_Str__GitHub__Repo_Name(TestCase):

    def test_Safe_Str__GitHub__Repo_Name_class(self):
        # Valid repository names
        assert str(Safe_Str__GitHub__Repo_Name('Hello-World'   )) == 'Hello-World'
        assert str(Safe_Str__GitHub__Repo_Name('my_project'    )) == 'my_project'
        assert str(Safe_Str__GitHub__Repo_Name('repo.name'     )) == 'repo.name'
        assert str(Safe_Str__GitHub__Repo_Name('OSBot-Utils'   )) == 'OSBot-Utils'
        assert str(Safe_Str__GitHub__Repo_Name('project-1.0'   )) == 'project-1.0'
        assert str(Safe_Str__GitHub__Repo_Name('test_repo_2023')) == 'test_repo_2023'
        assert str(Safe_Str__GitHub__Repo_Name('a'             )) == 'a'  # Single character

        # Maximum length (100 characters)
        assert str(Safe_Str__GitHub__Repo_Name('a' * 100)) == 'a' * 100

        # Whitespace trimming
        assert str(Safe_Str__GitHub__Repo_Name('  my-repo  ')) == 'my-repo'

        # Invalid characters get replaced
        assert str(Safe_Str__GitHub__Repo_Name('repo name')) == 'repo_name'
        assert str(Safe_Str__GitHub__Repo_Name('repo/name')) == 'repo_name'
        assert str(Safe_Str__GitHub__Repo_Name('repo@name')) == 'repo_name'
        assert str(Safe_Str__GitHub__Repo_Name('repo#name')) == 'repo_name'
        assert str(Safe_Str__GitHub__Repo_Name('repo!name')) == 'repo_name'

        # Reserved names
        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Name, invalid repository name"):
            Safe_Str__GitHub__Repo_Name('.')

        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Name, invalid repository name"):
            Safe_Str__GitHub__Repo_Name('..')

        # Empty or None
        #with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Name, value cannot be None when allow_empty is False"):
        assert Safe_Str__GitHub__Repo_Name(None) == ''

        #with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Name, value cannot be empty when allow_empty is False"):
        assert Safe_Str__GitHub__Repo_Name('') == ''

        # Exceeds max length
        with pytest.raises(ValueError, match=f"in Safe_Str__GitHub__Repo_Name, value exceeds maximum length of {TYPE_SAFE_STR__GITHUB__REPO_NAME__MAX_LENGTH}"):
            Safe_Str__GitHub__Repo_Name('a' * 101)

        # All invalid characters
        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Name, sanitized value consists entirely of '_' characters"):
            Safe_Str__GitHub__Repo_Name('!@#$%^&*()')

    def test_common_repo_names(self):
        # Common patterns in GitHub repository names
        assert str(Safe_Str__GitHub__Repo_Name('awesome-python')) == 'awesome-python'
        assert str(Safe_Str__GitHub__Repo_Name('learn-go')) == 'learn-go'
        assert str(Safe_Str__GitHub__Repo_Name('vue.js')) == 'vue.js'
        assert str(Safe_Str__GitHub__Repo_Name('react-native')) == 'react-native'
        assert str(Safe_Str__GitHub__Repo_Name('machine_learning_101')) == 'machine_learning_101'
        assert str(Safe_Str__GitHub__Repo_Name('project-v2.0.1')) == 'project-v2.0.1'

import pytest
from unittest                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo import Safe_Str__GitHub__Repo, TYPE_SAFE_STR__GITHUB__REPO__MAX_LENGTH
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Name import Safe_Str__GitHub__Repo_Name
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Owner import Safe_Str__GitHub__Repo_Owner


class test_Safe_Str__GitHub__Repo(TestCase):

    def test_Safe_Str__GitHub__Repo_class(self):
        # Valid full repository identifiers
        assert str(Safe_Str__GitHub__Repo('octocat/Hello-World'     )) == 'octocat/Hello-World'
        assert str(Safe_Str__GitHub__Repo('microsoft/vscode'        )) == 'microsoft/vscode'
        assert str(Safe_Str__GitHub__Repo('owasp-sbot/OSBot-Utils'  )) == 'owasp-sbot/OSBot-Utils'
        assert str(Safe_Str__GitHub__Repo('user-123/my_project.v2'  )) == 'user-123/my_project.v2'
        assert str(Safe_Str__GitHub__Repo('org/repo'                )) == 'org/repo'
        assert str(Safe_Str__GitHub__Repo('a/b'                     )) == 'a/b'  # Minimum valid

        # Whitespace trimming
        assert str(Safe_Str__GitHub__Repo('  octocat/Hello-World  ')) == 'octocat/Hello-World'

        # Invalid characters get replaced
        assert str(Safe_Str__GitHub__Repo('user name/repo name')) == 'user_name/repo_name'
        assert str(Safe_Str__GitHub__Repo('user@org/repo#1')) == 'user_org/repo_1'

        # Missing slash
        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo, gitHub repository must be in 'owner/repo' format"):
            Safe_Str__GitHub__Repo('justreponame')

        # Multiple slashes
        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo, gitHub repository must be in 'owner/repo' format"):
            Safe_Str__GitHub__Repo('owner/repo/extra')

        # Empty owner - will fail in Safe_Str__GitHub__Repo_Owner validation
        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo, missing owner, gitHub repository must be in 'owner/repo' format: /reponame"):
            Safe_Str__GitHub__Repo('/reponame')

        # Empty repo - will fail in Safe_Str__GitHub__Repo_Name validation
        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo, missing name, gitHub repository must be in 'owner/repo' format: owner/"):
            Safe_Str__GitHub__Repo('owner/')

        # The error messages will now come from the underlying classes
        # Owner with leading hyphen
        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Owner, gitHub owner name cannot start or end with a hyphen: -owner"):
            Safe_Str__GitHub__Repo('-owner/repo')

        # Owner with trailing hyphen
        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Owner, gitHub owner name cannot start or end with a hyphen: owner-"):
            Safe_Str__GitHub__Repo('owner-/repo')

        # Owner with consecutive hyphens
        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Owner, gitHub owner name cannot contain consecutive hyphens"):
            Safe_Str__GitHub__Repo('own--er/repo')

        # Reserved repo names
        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Name, invalid repository name"):
            Safe_Str__GitHub__Repo('owner/.')

        with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo_Name, invalid repository name"):
            Safe_Str__GitHub__Repo('owner/..')

        # Empty or None
        #with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo, value cannot be None when allow_empty is False"):
        assert Safe_Str__GitHub__Repo(None) == ''

        #with pytest.raises(ValueError, match="in Safe_Str__GitHub__Repo, value cannot be empty when allow_empty is False"):
        assert Safe_Str__GitHub__Repo('') == ''

        # Exceeds max length
        with pytest.raises(ValueError, match=f"in Safe_Str__GitHub__Repo, value exceeds maximum length of {TYPE_SAFE_STR__GITHUB__REPO__MAX_LENGTH}"):
            Safe_Str__GitHub__Repo('a' * 50 + '/' + 'b' * 100)  # Exceeds combined limit

    def test_property_methods(self):
        # Test owner and repo_name properties return proper Safe_Str types
        repo = Safe_Str__GitHub__Repo('octocat/Hello-World')

        # Check owner property
        owner = repo.repo_owner
        assert type(owner) is Safe_Str__GitHub__Repo_Owner
        assert str(owner) == 'octocat'

        # Check repo_name property
        name = repo.repo_name
        assert type(name) is Safe_Str__GitHub__Repo_Name
        assert str(name) == 'Hello-World'

        # Test with different repos
        repo = Safe_Str__GitHub__Repo('microsoft/vscode')
        assert type(repo.repo_owner) is Safe_Str__GitHub__Repo_Owner
        assert str (repo.repo_owner) == 'microsoft'
        assert type(repo.repo_name ) is Safe_Str__GitHub__Repo_Name
        assert str (repo.repo_name ) == 'vscode'

        repo = Safe_Str__GitHub__Repo('owasp-sbot/OSBot-Utils')
        assert type(repo.repo_owner) is Safe_Str__GitHub__Repo_Owner
        assert str (repo.repo_owner) == 'owasp-sbot'
        assert type(repo.repo_name ) is Safe_Str__GitHub__Repo_Name
        assert str (repo.repo_name  ) == 'OSBot-Utils'

    def test_usage_in_Type_Safe(self):
        class GitHub_Config(Type_Safe):
            main_repo: Safe_Str__GitHub__Repo = Safe_Str__GitHub__Repo('octocat/Hello-World')
            fork_repo: Safe_Str__GitHub__Repo = None

        # Test instantiation with default
        config = GitHub_Config()
        assert str(config.main_repo) == 'octocat/Hello-World'
        assert str(config.fork_repo ) == 'None'
        assert type(config.main_repo) is Safe_Str__GitHub__Repo

        # Test updating with valid value
        config.fork_repo = Safe_Str__GitHub__Repo('myuser/Hello-World')
        assert str(config.fork_repo) == 'myuser/Hello-World'

        # Test property access
        assert type(config.main_repo.repo_owner) is Safe_Str__GitHub__Repo_Owner
        assert str(config.main_repo.repo_owner) == 'octocat'
        assert type(config.main_repo.repo_name) is Safe_Str__GitHub__Repo_Name
        assert str(config.main_repo.repo_name) == 'Hello-World'
        assert type(config.fork_repo.repo_owner) is Safe_Str__GitHub__Repo_Owner
        assert str(config.fork_repo.repo_owner) == 'myuser'
        assert type(config.fork_repo.repo_name) is Safe_Str__GitHub__Repo_Name
        assert str(config.fork_repo.repo_name) == 'Hello-World'

        # Test serialization
        config_json = config.json()
        assert config_json == {
            'main_repo': 'octocat/Hello-World',
            'fork_repo': 'myuser/Hello-World'
        }

        # Round trip test
        config_round_trip = GitHub_Config.from_json(config_json)
        assert config_round_trip.obj() == config.obj()
        assert type(config_round_trip.main_repo) is Safe_Str__GitHub__Repo
        assert type(config_round_trip.fork_repo) is Safe_Str__GitHub__Repo

    def test_string_representation(self):
        # Full repo
        repo = Safe_Str__GitHub__Repo("octocat/Hello-World")
        assert str(repo) == "octocat/Hello-World"
        assert f"Repository: {repo}" == "Repository: octocat/Hello-World"
        assert repr(repo) == "Safe_Str__GitHub__Repo('octocat/Hello-World')"

        # Owner
        owner = Safe_Str__GitHub__Repo_Owner("octocat")
        assert str(owner) == "octocat"
        assert f"Owner: {owner}" == "Owner: octocat"
        assert repr(owner) == "Safe_Str__GitHub__Repo_Owner('octocat')"

        # Repo name
        name = Safe_Str__GitHub__Repo_Name("Hello-World")
        assert str(name) == "Hello-World"
        assert f"Name: {name}" == "Name: Hello-World"
        assert repr(name) == "Safe_Str__GitHub__Repo_Name('Hello-World')"

    def test_concatenation(self):
        # Test concatenation behavior
        owner = Safe_Str__GitHub__Repo_Owner('octocat')
        repo_name = Safe_Str__GitHub__Repo_Name('Hello-World')

        # Owner + string
        result = owner + '/'
        assert type(result) is Safe_Str__GitHub__Repo_Owner
        assert result == 'octocat_'

        # Repo name + string
        result = repo_name + '.git'
        assert type(result) is Safe_Str__GitHub__Repo_Name
        assert result == 'Hello-World.git'

        # Full repo + string
        full_repo = Safe_Str__GitHub__Repo('octocat/Hello-World')
        result = full_repo + '.git'
        assert type(result) is Safe_Str__GitHub__Repo
        assert result == 'octocat/Hello-World.git'
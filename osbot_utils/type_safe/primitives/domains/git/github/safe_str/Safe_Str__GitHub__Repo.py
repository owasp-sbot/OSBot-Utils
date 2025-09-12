import re
from osbot_utils.type_safe.primitives.core.Safe_Str                            import Safe_Str
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Name import Safe_Str__GitHub__Repo_Name
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Owner import Safe_Str__GitHub__Repo_Owner

TYPE_SAFE_STR__GITHUB__REPO__REGEX      = re.compile(r'[^a-zA-Z0-9\-_./]')
TYPE_SAFE_STR__GITHUB__REPO__MAX_LENGTH = 140  # 39 (owner) + 1 (/) + 100 (repo)

class Safe_Str__GitHub__Repo(Safe_Str):
    """
    Safe string class for full GitHub repository identifiers in owner/repo format.
    
    Examples:
    - "octocat/Hello-World"
    - "microsoft/vscode"
    - "owasp-sbot/OSBot-Utils"
    
    This class leverages Safe_Str__GitHub__Repo_Owner and Safe_Str__GitHub__Repo_Name
    for validation of the individual components.
    """
    regex                      = TYPE_SAFE_STR__GITHUB__REPO__REGEX
    max_length                 = TYPE_SAFE_STR__GITHUB__REPO__MAX_LENGTH
    allow_empty                = True
    trim_whitespace            = True
    allow_all_replacement_char = False
    repo_owner                 : Safe_Str__GitHub__Repo_Owner = None                                 # note: due to the str override these will not show in the Pycharm code hints (but they will work)
    repo_name                  : Safe_Str__GitHub__Repo_Name  = None

    def __new__(cls, value=None):
        result = super().__new__(cls, value)
        
        if result:
            if '/' not in result:                                                                   # Check for the required forward slash
                raise ValueError(f"in {cls.__name__}, gitHub repository must be in 'owner/repo' format: {result}")
            

            parts = result.split('/')                                                               # Split and validate components using the dedicated classes
            if len(parts) != 2:
                raise ValueError(f"in {cls.__name__}, gitHub repository must be in 'owner/repo' format: {result}")
            
            owner_part, repo_part = parts

            result.repo_owner = Safe_Str__GitHub__Repo_Owner(owner_part)                            # Validate using the dedicated classes (and store the references)
            result.repo_name  = Safe_Str__GitHub__Repo_Name(repo_part  )
            if not result.repo_owner:
                raise ValueError(f"in {cls.__name__}, missing owner, gitHub repository must be in 'owner/repo' format: {result}")
            if not result.repo_name:
                raise ValueError(f"in {cls.__name__}, missing name, gitHub repository must be in 'owner/repo' format: {result}")
        
        return result

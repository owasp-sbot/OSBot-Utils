from typing                                                   import Union, List, Dict
from osbot_utils.helpers.html.schemas.Schema__HTML_Node__Data import Schema__HTML_Node__Data
from osbot_utils.type_safe.Type_Safe                          import Type_Safe


class Schema__HTML_Node(Type_Safe):
    attrs    : Dict[str, str]                                               # HTML attributes (e.g., {'class': 'container'})
    nodes    : List[Union['Schema__HTML_Node', Schema__HTML_Node__Data]]    # Child nodes (recursive structure)
    tag      : str                                                          # HTML tag name (e.g., 'div', 'meta', 'title')


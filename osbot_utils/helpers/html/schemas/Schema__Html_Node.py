from typing import Union, List, Dict, Optional
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data import Schema__Html_Node__Data
from osbot_utils.type_safe.Type_Safe                          import Type_Safe


class Schema__Html_Node(Type_Safe):
    attrs    : Dict[str, Optional[str]]                                               # HTML attributes (e.g., {'class': 'container'})
    nodes    : List[Union['Schema__Html_Node', Schema__Html_Node__Data]]    # Child nodes (recursive structure)
    tag      : str                                                          # HTML tag name (e.g., 'div', 'meta', 'title')


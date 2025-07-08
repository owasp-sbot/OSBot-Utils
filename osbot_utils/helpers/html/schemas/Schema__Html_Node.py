from typing                                                   import List, Dict, Optional
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data import Schema__Html_Node__Data
from osbot_utils.type_safe.Type_Safe                          import Type_Safe


class Schema__Html_Node(Type_Safe):
    attrs       : Dict[str, str           ]                   # HTML attributes (e.g., {'class': 'container'})
    child_nodes : List['Schema__Html_Node']                   # Element nodes only
    text_nodes  : List[Schema__Html_Node__Data]               # Text nodes only
    tag         : str                                         # HTML tag name (e.g., 'div', 'meta', 'title')
    position    : int = -1                                    # Position in parent's nodes list (-1 for root)


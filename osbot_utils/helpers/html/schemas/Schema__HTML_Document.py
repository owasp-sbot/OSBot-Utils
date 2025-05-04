from typing                                             import Dict, List
from osbot_utils.helpers.html.schemas.Schema__HTML_Node import Schema__HTML_Node
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class Schema__HTML_Document(Type_Safe):
    attrs    : Dict[str, str]                           # Root level attributes (e.g., {'lang': 'en'})
    children : List[Schema__HTML_Node]                  # Top-level child nodes
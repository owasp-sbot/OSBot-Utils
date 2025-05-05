from osbot_utils.helpers.Timestamp_Now                  import Timestamp_Now
from osbot_utils.helpers.html.schemas.Schema__HTML_Node import Schema__HTML_Node
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class Schema__HTML_Document(Type_Safe):
    root_node : Schema__HTML_Node                        # Top-level child nodes
    timestamp: Timestamp_Now
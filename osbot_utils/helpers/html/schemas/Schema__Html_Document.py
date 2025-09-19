from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now   import Timestamp_Now
from osbot_utils.helpers.html.schemas.Schema__Html_Node                            import Schema__Html_Node
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe

class Schema__Html_Document(Type_Safe):
    root_node : Schema__Html_Node                        # Top-level child nodes
    timestamp: Timestamp_Now
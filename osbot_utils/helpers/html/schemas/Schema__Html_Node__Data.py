from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data__Type import Schema__Html_Node__Data__Type
from osbot_utils.type_safe.Type_Safe                                import Type_Safe

class Schema__Html_Node__Data(Type_Safe):
    data     : str                                                                   # Text content
    type     : Schema__Html_Node__Data__Type  = Schema__Html_Node__Data__Type.TEXT   # Always 'text' for text nodes
    position : int                                                                   # Position in parent's nodes list

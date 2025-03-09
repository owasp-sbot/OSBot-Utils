from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Role import Schema__LLM_Request__Message__Role
from osbot_utils.type_safe.Type_Safe                                     import Type_Safe

class Schema__LLM_Request__Message__Content(Type_Safe):                # Schema for message content in LLM requests.
    role   : Schema__LLM_Request__Message__Role                       # Message role (system, user, assistant)
    content: str                                                     # Message content

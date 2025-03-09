from typing                                                                 import Dict, Any, Optional, Tuple, Type, List
from osbot_utils.helpers.llms.actions.Type_Safe__Schema_For__LLMs           import Type_Safe__Schema_For__LLMs
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data             import Schema__LLM_Request__Data
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Function_Call    import Schema__LLM_Request__Function_Call
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Content import Schema__LLM_Request__Message__Content
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Role    import Schema__LLM_Request__Message__Role
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                             import type_safe

class LLM_Request_Builder(Type_Safe):
    schema_generator: Type_Safe__Schema_For__LLMs
    llm_request     : Schema__LLM_Request__Data

    @type_safe
    def add_message(self, role    : Schema__LLM_Request__Message__Role,
                          content : str
                     ) -> Schema__LLM_Request__Message__Content:
        message = Schema__LLM_Request__Message__Content(role=role, content=content)
        self.llm_request.messages.append(message)
        return self

    def add_message__assistant(self, content : str): return self.add_message(role=Schema__LLM_Request__Message__Role.ASSISTANT, content=content)
    def add_message__system   (self, content : str): return self.add_message(role=Schema__LLM_Request__Message__Role.SYSTEM   , content=content)
    def add_message__user     (self, content : str): return self.add_message(role=Schema__LLM_Request__Message__Role.USER     , content=content)

    @type_safe
    def set_function_call(self, parameters    : Type[Type_Safe],
                                   function_name : str,
                                   description   : str   = ''
                           ) -> Schema__LLM_Request__Function_Call:
        function_call = Schema__LLM_Request__Function_Call(parameters   = parameters,
                                                          function_name = function_name,
                                                          description   = description)
        self.llm_request.function_call = function_call
        return self


    @type_safe
    def build_request_payload(self) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement this method")
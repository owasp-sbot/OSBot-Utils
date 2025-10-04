from typing                                                                  import Dict, Any, Type
from osbot_utils.type_safe.primitives.domains.llm.safe_str.Safe_Str__LLM__Model_Id   import Safe_Str__LLM__Model_Id
from osbot_utils.helpers.llms.actions.Type_Safe__Schema_For__LLMs            import Type_Safe__Schema_For__LLMs
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request                    import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data              import Schema__LLM_Request__Data
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Function_Call     import Schema__LLM_Request__Function_Call
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Content  import Schema__LLM_Request__Message__Content
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Role     import Schema__LLM_Request__Message__Role
from osbot_utils.type_safe.Type_Safe                                         import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text           import Safe_Str__Text
from osbot_utils.type_safe.type_safe_core.decorators.type_safe               import type_safe


class LLM_Request__Builder(Type_Safe):
    schema_generator : Type_Safe__Schema_For__LLMs
    llm_request_data : Schema__LLM_Request__Data

    @type_safe
    def add_message(self, role    : Schema__LLM_Request__Message__Role,
                          content : str = None                        ):
        if content:
            message = Schema__LLM_Request__Message__Content(role=role, content=content)
            self.llm_request_data.messages.append(message)
        return self

    def add_message__assistant(self, content : str = None): return self.add_message(role=Schema__LLM_Request__Message__Role.ASSISTANT, content=content)
    def add_message__system   (self, content : str = None): return self.add_message(role=Schema__LLM_Request__Message__Role.SYSTEM   , content=content)
    def add_message__user     (self, content : str = None): return self.add_message(role=Schema__LLM_Request__Message__Role.USER     , content=content)

    def llm_request(self) -> Schema__LLM_Request:
        return Schema__LLM_Request(request_data=self.llm_request_data)

    @type_safe
    def set__function_call(self, parameters    : Type[Type_Safe],
                                 function_name : str            ,
                                 description   : str   = ''     ):
        function_call = Schema__LLM_Request__Function_Call(parameters   = parameters,
                                                          function_name = function_name,
                                                          description   = description)
        self.llm_request_data.function_call = function_call
        return self

    def set__model              (self, model   : Safe_Str__LLM__Model_Id  ): self.llm_request_data.model    = model   ; return self
    def set__platform           (self, platform: Safe_Str__Text           ): self.llm_request_data.platform = platform; return self
    def set__provider           (self, provider: Safe_Str__Text           ): self.llm_request_data.provider = provider; return self
    def set__model__gpt_4o      (self                                     ): return self.set__model('gpt-4o'      )
    def set__model__gpt_4o_mini (self                                     ): return self.set__model('gpt-4o-mini' )
    def set__model__gpt_4_1     (self                                     ): return self.set__model('gpt-4.1'     )
    def set__model__gpt_4_1_mini(self                                     ): return self.set__model('gpt-4.1-mini')
    def set__model__gpt_4_1_nano(self                                     ): return self.set__model('gpt-4.1-nano')


    @type_safe
    def build_request_payload(self) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement this method")
from typing                                                      import Dict, Any, Optional
from osbot_utils.helpers.llms.builders.LLM_Request_Builder       import LLM_Request_Builder
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data  import Schema__LLM_Request__Data
from osbot_utils.type_safe.decorators.type_safe            import type_safe
from osbot_utils.utils.Json                                import json_dumps


class LLM_Request_Builder__Open_AI(LLM_Request_Builder):

    @type_safe
    def build_request_payload(self) -> Dict[str, Any]:
        payload = { "model"          : self.llm_request.model                                                             ,
                    "messages"       : [{"role"  : msg.role.value, "content": msg.content} for msg in self.llm_request.messages]}
        if self.llm_request.function_call:
            schema = self.schema_generator.export(self.llm_request.function_call.parameters)
            schema["additionalProperties"] = False                                  # needs to be False when using structured outputs
            payload["response_format"    ] =  { "type"       : "json_schema",
                                                "json_schema": { "name"  : self.llm_request.function_call.function_name,
                                                                 "schema": schema                                      ,
                                                                 'strict': True                                        }}

        if self.llm_request.temperature is not None: payload["temperature"] = self.llm_request.temperature
        if self.llm_request.top_p       is not None: payload["top_p"      ] = self.llm_request.top_p
        if self.llm_request.max_tokens  is not None: payload["max_tokens" ] = self.llm_request.max_tokens

        return payload

    # @type_safe
    # def build_request_with_json_mode(self, request: Schema__LLM_Request
    #                                 ) -> Dict[str, Any]:
    #     """
    #     Builds request using OpenAI's JSON mode rather than function calling.
    #     This is an alternative approach for structured outputs that doesn't use the tools API.
    #     """
    #     payload = {
    #         "model": request.model,
    #         "messages": [
    #             {"role": msg.role, "content": msg.content}
    #             for msg in request.messages
    #         ],
    #         "response_format": {"type": "json_object"}
    #     }
    #
    #     if request.temperature is not None:
    #         payload["temperature"] = request.temperature
    #     if request.top_p is not None:
    #         payload["top_p"] = request.top_p
    #     if request.max_tokens is not None:
    #         payload["max_tokens"] = request.max_tokens
    #
    #     return payload

    # @type_safe
    # def build_request_json(self, request: Schema__LLM_Request
    #                       ) -> str:
    #     payload = self.build_request_payload(request)
    #     return json_dumps(payload)
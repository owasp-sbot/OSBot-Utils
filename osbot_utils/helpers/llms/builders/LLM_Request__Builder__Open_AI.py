from typing                                                     import Dict, Any
from osbot_utils.helpers.llms.builders.LLM_Request__Builder     import LLM_Request__Builder
from osbot_utils.type_safe.type_safe_core.decorators.type_safe  import type_safe


class LLM_Request__Builder__Open_AI(LLM_Request__Builder):

    @type_safe
    def build_request_payload(self) -> Dict[str, Any]:
        payload = { "model"          : self.llm_request_data.model                                                             ,
                    "messages"       : [{"role"  : msg.role.value, "content": msg.content} for msg in self.llm_request_data.messages]}
        if self.llm_request_data.function_call:
            schema = self.schema_generator.export(self.llm_request_data.function_call.parameters)
            self.add_additional_properties_to_schema(schema)
            payload["response_format"    ] =  { "type"       : "json_schema",
                                                "json_schema": { "name"  : self.llm_request_data.function_call.function_name,
                                                                 "schema": schema                                      ,
                                                                 'strict': True                                        }}

        if self.llm_request_data.temperature is not None: payload["temperature"] = self.llm_request_data.temperature
        if self.llm_request_data.top_p       is not None: payload["top_p"      ] = self.llm_request_data.top_p
        if self.llm_request_data.max_tokens  is not None: payload["max_tokens" ] = self.llm_request_data.max_tokens

        return payload

    def add_additional_properties_to_schema(self, schema: dict) -> dict: # Recursively ensures every nested object in the schema has "additionalProperties": False.
        if schema.get("type") == "object":
            schema["additionalProperties"] = False
            for prop_schema in schema.get("properties", {}).values():
                self.add_additional_properties_to_schema(prop_schema)

        elif schema.get("type") == "array":
            items_schema = schema.get("items", {})
            self.add_additional_properties_to_schema(items_schema)

        return schema

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
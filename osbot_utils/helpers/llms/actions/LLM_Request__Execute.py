from osbot_utils.helpers.llms.actions.LLM_Request__Cache            import LLM_Request__Cache
from osbot_utils.helpers.llms.builders.LLM_Request__Builder import LLM_Request__Builder
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI   import API__LLM__Open_AI
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request           import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response          import Schema__LLM_Response
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                     import type_safe
from osbot_utils.utils.Dev import pprint


class LLM_Request__Execute(Type_Safe):
    llm_cache      : LLM_Request__Cache
    llm_api        : API__LLM__Open_AI
    use_cache      : bool = True
    request_builder: LLM_Request__Builder

    @type_safe
    def execute(self, llm_request: Schema__LLM_Request) -> Schema__LLM_Response:

        if self.use_cache:                                                                  # Check cache if enabled
            cached_response = self.llm_cache.get(llm_request)
            if cached_response:
                return cached_response

        self.request_builder.llm_request_data = llm_request.request_data

        llm_payload = self.request_builder.build_request_payload()

        response_data = self.llm_api.execute(llm_payload)                      # Make API call

        llm_response = Schema__LLM_Response(response_data=response_data)                    # Create response object

        if self.use_cache:                                                                  # Cache the response if enabled
            self.llm_cache.add(llm_request, llm_response)

        return llm_response
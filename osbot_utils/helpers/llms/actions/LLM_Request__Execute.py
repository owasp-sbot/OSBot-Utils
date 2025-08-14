from osbot_utils.helpers.duration.decorators.capture_duration       import capture_duration
from osbot_utils.helpers.llms.cache.LLM_Request__Cache              import LLM_Request__Cache
from osbot_utils.helpers.llms.builders.LLM_Request__Builder         import LLM_Request__Builder
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI   import API__LLM__Open_AI
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request           import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response          import Schema__LLM_Response
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe      import type_safe


class LLM_Request__Execute(Type_Safe):
    llm_cache      : LLM_Request__Cache
    llm_api        : API__LLM__Open_AI
    use_cache      : bool                 = True
    refresh_cache  : bool                 = False
    request_builder: LLM_Request__Builder           # todo: fix the use of LLM_Request__Builder since it not good when we when overwrite it at self.request_builder.llm_request_data = llm_request.request_data

    @type_safe
    def execute(self, llm_request: Schema__LLM_Request) -> Schema__LLM_Response:

        if self.use_cache is True and self.refresh_cache is False:                                                                          # Check cache if enabled
            cached_response = self.llm_cache.get(llm_request)
            if cached_response:
                return cached_response

        self.request_builder.llm_request_data = llm_request.request_data
        llm_payload                           = self.request_builder.build_request_payload()
        with capture_duration() as duration:
            response_data                     = self.llm_api.execute(llm_payload)                   # Make API call
        llm_response                          = Schema__LLM_Response(response_data=response_data)   # Create response object

        if self.use_cache:                                                                          # Cache the response if enabled
            kwargs_add = dict(request  = llm_request     ,
                              response = llm_response    ,
                              payload  = llm_payload     ,
                              duration = duration.seconds)
            self.llm_cache.add(**kwargs_add)

        return llm_response
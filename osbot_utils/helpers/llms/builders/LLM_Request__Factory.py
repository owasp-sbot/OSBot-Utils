from typing                                                                       import Type, Optional, Dict, Any
from osbot_utils.helpers.llms.builders.LLM_Request__Builder                       import LLM_Request__Builder
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data                   import Schema__LLM_Request__Data
from osbot_utils.type_safe.Type_Safe                                              import Type_Safe
from osbot_utils.type_safe.primitives.domains.llm.safe_float.Safe_Float__LLM__Temperature import Safe_Float__LLM__Temperature
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                    import type_safe


class LLM_Request__Factory(Type_Safe):                              # Factory class for creating common LLM request patterns.
    request_builder : LLM_Request__Builder

    @type_safe
    def create_simple_chat_request(self, model        : str                                 ,   # Model identifier
                                         provider     : str                                 ,   # Provider name (openai, anthropic)
                                         platform     : str                                 ,   # Platform name
                                         user_message : str                                 ,   # User message content
                                         system_prompt: str                          = None ,   # Optional system prompt
                                         temperature  : Safe_Float__LLM__Temperature = None     # Temperature
                                   ):                                                           # Create a simple chat request with optional system prompt.

        with self.request_builder as _:
            _.llm_request_data.model       = model
            _.llm_request_data.provider    = provider
            _.llm_request_data.platform    = platform
            _.llm_request_data.temperature = temperature

            _.add_message__system(content=system_prompt)                                # Add system prompt
            _.add_message__user  (content=user_message )                                # Add user message
        return self

    @type_safe
    def create_function_calling_request(self, model          : str                  ,                # Model identifier
                                              provider       : str                  ,                # Provider name (openai, anthropic)
                                              platform       : str                  ,                # Platform name
                                              parameters     : Type[Type_Safe]      ,                # Parameters schema class
                                              function_name  : str                  ,                # Function name
                                              function_desc  : str                  ,                # Function description
                                              user_message   : str                  ,                # User message
                                              system_prompt  : str                          = None , # Optional system prompt
                                              temperature    : Safe_Float__LLM__Temperature = None   # Temperature
                                         ):                                                          # Create a request that uses function calling with the specified schema.

        with self.request_builder as _:
            _.set__function_call(parameters    = parameters,  # Create the function call
                                 function_name = function_name,
                                 description   = function_desc)

            _.add_message__system(content=system_prompt)
            _.add_message__user  (content=user_message )
            _.llm_request_data.model       = model
            _.llm_request_data.provider    = provider
            _.llm_request_data.platform    = platform
            _.llm_request_data.temperature = temperature
        return self

    @type_safe
    def create_entity_extraction_request(self, model             : str                  ,              # Model identifier
                                               provider          : str                  ,              # Provider name
                                               platform          : str                  ,              # Platform name
                                               entity_class      : Type[Type_Safe]      ,              # Entity schema class
                                               text_to_analyze   : str                  ,              # Text to extract entities from
                                               system_instruction: Optional[str] = None ,              # Optional system instructions
                                               function_name     : str = "extract_entities",           # Function name
                                               temperature       : Safe_Float__LLM__Temperature = 0.0  # Low temperature for precision
                                        )                        -> Schema__LLM_Request__Data:
        """Create a specialized request for entity extraction using the provided schema."""
        # Default system instruction if none provided
        if system_instruction is None:
            system_instruction = (
                "You are an expert at analyzing text and extracting structured information. "
                "Extract entities mentioned in the text according to the specified schema. "
                "Be precise and only include information explicitly mentioned in the text."
            )

        # User message prompting for extraction
        user_message = f"Extract key entities from this text: {text_to_analyze}"

        # Create the function calling request
        return self.create_function_calling_request(
            model=model,
            provider=provider,
            platform=platform,
            parameters=entity_class,
            function_name=function_name,
            function_desc="Extract entities from text",
            system_prompt=system_instruction,
            user_message=user_message,
            temperature=temperature
        )

    def request_data(self) -> Schema__LLM_Request__Data:
        return self.request_builder.llm_request_data

    @type_safe
    def build_request_payload(self) -> Dict[str, Any]:                     # Build a provider-specific request payload from a Schema__LLM_Request.
        return self.request_builder.build_request_payload()
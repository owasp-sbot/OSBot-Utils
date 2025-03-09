from typing                                                     import Type, List, Optional, Dict, Any

from osbot_utils.helpers.llms.builders.LLM_Request_Builder import LLM_Request_Builder
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data import Schema__LLM_Request__Data
from osbot_utils.type_safe.Type_Safe                            import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                 import type_safe


class LLM_Request_Factory(Type_Safe):                              # Factory class for creating common LLM request patterns.
    builder : LLM_Request_Builder

    @type_safe
    def create_simple_chat_request(self, model        : str                  ,          # Model identifier
                                         provider     : str                  ,          # Provider name (openai, anthropic)
                                         platform     : str                  ,          # Platform name
                                         user_message : str                  ,          # User message content
                                         system_prompt: Optional[str] = None ,          # Optional system prompt
                                         temperature  : Optional[float] = None          # Temperature
                                   )                  -> Schema__LLM_Request__Data:           # Create a simple chat request with optional system prompt.

        messages = []                                                                   # Create empty list of messages

        if system_prompt:                                                               # Add system message if provided
            messages.append(self.builder.create_message(role="system", content=system_prompt))

        # Add user message
        messages.append(self.builder.create_message(role="user", content=user_message))

        # Create and return the request
        return self.builder.create_request(model       = model      ,
                                           provider    = provider   ,
                                           platform    = platform   ,
                                           messages    = messages   ,
                                           temperature = temperature)

    @type_safe
    def create_function_calling_request(self, model          : str                  ,          # Model identifier
                                              provider       : str                  ,          # Provider name (openai, anthropic)
                                              platform       : str                  ,          # Platform name
                                              parameters     : Type[Type_Safe]      ,          # Parameters schema class
                                              function_name  : str                  ,          # Function name
                                              function_desc  : str                  ,          # Function description
                                              user_message   : str                  ,          # User message
                                              system_prompt  : Optional[str] = None ,          # Optional system prompt
                                              temperature    : Optional[float] = None          # Temperature
                                         ) -> Schema__LLM_Request__Data:
        """Create a request that uses function calling with the specified schema."""
        # Create the function call
        function_call = self.builder.create_function_call(
            parameters=parameters,
            function_name=function_name,
            description=function_desc
        )

        # Create empty list of messages
        messages = []

        # Add system message if provided
        if system_prompt:
            messages.append(self.builder.create_message(role="system", content=system_prompt))

        # Add user message
        messages.append(self.builder.create_message(role="user", content=user_message))

        # Create and return the request
        return self.builder.create_request(
            model=model,
            provider=provider,
            platform=platform,
            messages=messages,
            function_call=function_call,
            temperature=temperature
        )

    @type_safe
    def create_entity_extraction_request(self, model             : str                  ,          # Model identifier
                                               provider          : str                  ,          # Provider name
                                               platform          : str                  ,          # Platform name
                                               entity_class      : Type[Type_Safe]      ,          # Entity schema class
                                               text_to_analyze   : str                  ,          # Text to extract entities from
                                               system_instruction: Optional[str] = None ,          # Optional system instructions
                                               function_name     : str = "extract_entities",       # Function name
                                               temperature       : Optional[float] = 0.2          # Low temperature for precision
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

    @type_safe
    def build_request_payload(self, request: Schema__LLM_Request__Data  # Request schema to build payload from
                              )              -> Dict[str, Any]:
        """Build a provider-specific request payload from a Schema__LLM_Request."""
        return self.builder.build_request_payload(request)
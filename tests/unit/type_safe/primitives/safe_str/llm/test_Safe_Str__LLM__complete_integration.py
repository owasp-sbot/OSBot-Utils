from typing                                                                     import Dict, Any, List
from unittest                                                                   import TestCase
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.safe_str.llm.Safe_Str__LLM__Description   import Safe_Str__LLM__Description
from osbot_utils.type_safe.primitives.safe_str.llm.Safe_Str__LLM__Modality      import Safe_Str__LLM__Modality
from osbot_utils.type_safe.primitives.safe_str.llm.Safe_Str__LLM__Model_ID      import Safe_Str__LLM__Model_ID
from osbot_utils.type_safe.primitives.safe_str.llm.Safe_Str__LLM__Model_Name    import Safe_Str__LLM__Model_Name
from osbot_utils.type_safe.primitives.safe_str.llm.Safe_Str__LLM__Model_Slug    import Safe_Str__LLM__Model_Slug
from osbot_utils.type_safe.primitives.safe_str.llm.Safe_Str__LLM__Tokenizer     import Safe_Str__LLM__Tokenizer
from osbot_utils.type_safe.primitives.safe_str.web.Safe_Str__API__Parameter     import Safe_Str__API__Parameter


class test_Safe_Str__LLM__complete_integration(TestCase):                       # Integration tests using all LLM Safe_Str types together

    def test_complete_model_schema(self):                                       # Test all types in a schema
        class Schema__LLM__Model(Type_Safe):
            model_id    : Safe_Str__LLM__Model_ID
            model_name  : Safe_Str__LLM__Model_Name
            model_slug  : Safe_Str__LLM__Model_Slug
            description : Safe_Str__LLM__Description
            modality    : Safe_Str__LLM__Modality
            tokenizer   : Safe_Str__LLM__Tokenizer

        with Schema__LLM__Model() as model:
            # Assign values with auto-conversion
            model.model_id    = 'openai/gpt-4-turbo'
            model.model_name  = 'GPT-4 Turbo (Latest)'
            model.model_slug  = 'gpt-4-turbo'
            model.description = 'OpenAI\'s most capable model with 128k context window.'
            model.modality    = 'text->text'
            model.tokenizer   = 'cl100k_base'

            # Verify types
            assert type(model.model_id)    is Safe_Str__LLM__Model_ID
            assert type(model.model_name)  is Safe_Str__LLM__Model_Name
            assert type(model.model_slug)  is Safe_Str__LLM__Model_Slug
            assert type(model.description) is Safe_Str__LLM__Description
            assert type(model.modality)    is Safe_Str__LLM__Modality
            assert type(model.tokenizer)   is Safe_Str__LLM__Tokenizer

            # Test JSON serialization
            json_data = model.json()
            assert json_data == {'model_id'   : 'openai/gpt-4-turbo'    ,
                                 'model_name' : 'GPT-4 Turbo (Latest)'  ,
                                 'model_slug' : 'gpt-4-turbo'           ,
                                 'description': 'OpenAI\'s most capable model with 128k context window.',
                                 'modality'   : 'text->text'            ,
                                 'tokenizer'  : 'cl100k_base'           }

            # Test round-trip
            restored = Schema__LLM__Model.from_json(json_data)
            assert restored.obj() == model.obj()

    def test_api_request_schema(self):                                          # Test API parameter usage
        class Schema__LLM__Request(Type_Safe):
            model       : Safe_Str__LLM__Model_ID
            parameters  : Dict[Safe_Str__API__Parameter, Any]

        with Schema__LLM__Request() as request:
            request.model = 'claude-3-opus'
            request.parameters = {  Safe_Str__API__Parameter('temperature')    : 0.7    ,
                                    Safe_Str__API__Parameter('max_tokens')     : 4096   ,
                                    Safe_Str__API__Parameter('top_p')          : 0.9    ,
                                    Safe_Str__API__Parameter('stream')         : False  }

            assert type(request.model) is Safe_Str__LLM__Model_ID
            assert 'temperature' in str(list(request.parameters.keys())[0])

    def test_model_catalog_entry(self):                                         # Test complete catalog entry
        class Schema__Model__Catalog__Entry(Type_Safe):
            id          : Safe_Str__LLM__Model_ID
            name        : Safe_Str__LLM__Model_Name
            slug        : Safe_Str__LLM__Model_Slug
            description : Safe_Str__LLM__Description
            modality    : Safe_Str__LLM__Modality
            tokenizer   : Safe_Str__LLM__Tokenizer
            supported_params : List[Safe_Str__API__Parameter]

        with Schema__Model__Catalog__Entry() as entry:
            entry.id          = 'anthropic/claude-3-opus@20240229'
            entry.name        = 'Claude 3 Opus (February 2024)'
            entry.slug        = 'claude-3-opus'
            entry.description = """Claude 3 Opus - Our most intelligent model
Superior performance on complex tasks.
- 200K context window
- Advanced reasoning"""
            entry.modality    = 'text+image->text'
            entry.tokenizer   = 'Claude Tokenizer'
            entry.supported_params = [
                'temperature',
                'max_tokens',
                'top_p',
                'top_k',
                'stream'
            ]

            # Verify all fields are correct type
            assert type(entry.id)          is Safe_Str__LLM__Model_ID
            assert type(entry.name)        is Safe_Str__LLM__Model_Name
            assert type(entry.slug)        is Safe_Str__LLM__Model_Slug
            assert type(entry.description) is Safe_Str__LLM__Description
            assert type(entry.modality)    is Safe_Str__LLM__Modality
            assert type(entry.tokenizer)   is Safe_Str__LLM__Tokenizer

            # Auto-conversion in list
            for param in entry.supported_params:
                assert type(param) is Safe_Str__API__Parameter

            # Verify values
            assert '@' in entry.id                                      # @ preserved in model ID
            assert '+' in entry.modality                                # + preserved
            assert '->' in entry.modality                               # -> preserved

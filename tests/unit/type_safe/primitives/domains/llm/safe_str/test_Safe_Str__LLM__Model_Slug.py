from unittest                                                                           import TestCase
from osbot_utils.utils.Objects                                                          import __, base_classes
from osbot_utils.type_safe.Type_Safe__Primitive                                         import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Str                                     import Safe_Str
from osbot_utils.type_safe.primitives.domains.llm.safe_str.Safe_Str__LLM__Model_Slug    import Safe_Str__LLM__Model_Slug


class test_Safe_Str__LLM__Model_Slug(TestCase):

    def test__init__(self):                                                       # Test initialization
        with Safe_Str__LLM__Model_Slug() as _:
            assert type(_)         is Safe_Str__LLM__Model_Slug
            assert base_classes(_) == [Safe_Str, Type_Safe__Primitive, str, object, object]
            assert _               == ''
            assert _.max_length    == 256

    def test_valid_slugs(self):                                                  # Test URL-safe slugs
        assert Safe_Str__LLM__Model_Slug('gpt-4-turbo')         == 'gpt-4-turbo'
        assert Safe_Str__LLM__Model_Slug('claude-3-opus')       == 'claude-3-opus'
        assert Safe_Str__LLM__Model_Slug('llama-3.1-70b')       == 'llama-3.1-70b'
        assert Safe_Str__LLM__Model_Slug('command_r_plus')      == 'command_r_plus'
        assert Safe_Str__LLM__Model_Slug('models/gemini-pro')   == 'models/gemini-pro'

        # Invalid chars replaced
        assert Safe_Str__LLM__Model_Slug('model name')          == 'model_name'
        assert Safe_Str__LLM__Model_Slug('model@test')          == 'model_test'
        assert Safe_Str__LLM__Model_Slug('model:v1')            == 'model_v1'




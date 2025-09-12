from unittest                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe__Primitive                                     import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Str                                 import Safe_Str
from osbot_utils.utils.Objects                                                      import __, base_classes
from osbot_utils.type_safe.primitives.domains.llm.safe_str.Safe_Str__LLM__Tokenizer import Safe_Str__LLM__Tokenizer


class test_Safe_Str__LLM__Tokenizer(TestCase):

    def test__init__(self):                                                      # Test initialization
        with Safe_Str__LLM__Tokenizer() as _:
            assert type(_)         is Safe_Str__LLM__Tokenizer
            assert base_classes(_) == [Safe_Str, Type_Safe__Primitive, str, object, object]
            assert _               == ''
            assert _.max_length    == 64

    def test_valid_tokenizers(self):                                            # Test tokenizer names
        # Common tokenizers
        assert Safe_Str__LLM__Tokenizer('cl100k_base')          == 'cl100k_base'
        assert Safe_Str__LLM__Tokenizer('tiktoken')             == 'tiktoken'
        assert Safe_Str__LLM__Tokenizer('sentencepiece')        == 'sentencepiece'
        assert Safe_Str__LLM__Tokenizer('BPE')                  == 'BPE'
        assert Safe_Str__LLM__Tokenizer('WordPiece')            == 'WordPiece'

        # With descriptive names
        assert Safe_Str__LLM__Tokenizer('GPT-4 Tokenizer')      == 'GPT-4 Tokenizer'
        assert Safe_Str__LLM__Tokenizer('Claude Tokenizer')     == 'Claude Tokenizer'
        assert Safe_Str__LLM__Tokenizer('Llama_tokenizer')      == 'Llama_tokenizer'

        # With version numbers
        assert Safe_Str__LLM__Tokenizer('tokenizer_v2')         == 'tokenizer_v2'
        assert Safe_Str__LLM__Tokenizer('bpe-50k')              == 'bpe-50k'

        # Invalid chars replaced
        assert Safe_Str__LLM__Tokenizer('tokenizer@v1')         == 'tokenizer_v1'
        assert Safe_Str__LLM__Tokenizer('tokenizer.v2')         == 'tokenizer_v2'



from unittest                                                                   import TestCase
from osbot_utils.type_safe.Type_Safe__Primitive                                 import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.safe_str.Safe_Str                         import Safe_Str
from osbot_utils.utils.Objects                                                  import __, base_classes
from osbot_utils.type_safe.primitives.safe_str.llm.Safe_Str__LLM__Modality      import Safe_Str__LLM__Modality


class test_Safe_Str__LLM__Modality(TestCase):

    def test__init__(self):                                                      # Test initialization
        with Safe_Str__LLM__Modality() as _:
            assert type(_)         is Safe_Str__LLM__Modality
            assert base_classes(_) == [Safe_Str, Type_Safe__Primitive, str, object, object]
            assert _               == ''
            assert _.max_length    == 128

    def test_valid_modalities(self):                                            # Test modality descriptors
        # Single modality
        assert Safe_Str__LLM__Modality('text')                  == 'text'
        assert Safe_Str__LLM__Modality('image')                 == 'image'
        assert Safe_Str__LLM__Modality('audio')                 == 'audio'
        assert Safe_Str__LLM__Modality('video')                 == 'video'
        assert Safe_Str__LLM__Modality('multimodal')            == 'multimodal'

        # Transformations
        assert Safe_Str__LLM__Modality('text->image')           == 'text->image'
        assert Safe_Str__LLM__Modality('image->text')           == 'image->text'
        assert Safe_Str__LLM__Modality('audio->text')           == 'audio->text'
        assert Safe_Str__LLM__Modality('text->audio')           == 'text->audio'

        # Combinations
        assert Safe_Str__LLM__Modality('text+image')            == 'text+image'
        assert Safe_Str__LLM__Modality('text+image->text')      == 'text+image->text'
        assert Safe_Str__LLM__Modality('image+text->image')     == 'image+text->image'

        # With spaces
        assert Safe_Str__LLM__Modality('text + vision')         == 'text + vision'
        assert Safe_Str__LLM__Modality('audio + text')          == 'audio + text'

        # Invalid chars replaced
        assert Safe_Str__LLM__Modality('text|image')            == 'text_image'
        assert Safe_Str__LLM__Modality('text&image')            == 'text_image'
        assert Safe_Str__LLM__Modality('text/image')            == 'text_image'


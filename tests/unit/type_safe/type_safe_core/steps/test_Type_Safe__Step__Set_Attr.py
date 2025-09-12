import re
import pytest
from unittest                                                               import TestCase
from typing                                                                 import Literal
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid       import Random_Guid
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Annotations     import type_safe_annotations
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__Set_Attr   import Type_Safe__Step__Set_Attr, type_safe_step_set_attr
from osbot_utils.utils.Misc                                                 import random_guid


class test_Type_Safe__Step__Set_Attr(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.step_set_attr = Type_Safe__Step__Set_Attr()

    # def setUp(self):
    #     print()


    # @trace_calls(include          = ['*'],
    #              show_internals   = True ,
    #              show_duration    = True ,
    #              duration_padding = 130  ,
    #              show_class       = True )
    def test_class__one_int(self):
        class Class__One_int:
            an_int: int
        one_int = Class__One_int()
        one_int.an_int = 0
        assert one_int.__class__.__mro__ == (Class__One_int, object)
        assert type_safe_annotations.all_annotations(one_int)  == {'an_int': int}
        assert self.step_set_attr.setattr(one_int, one_int, 'an_int', 42) is None
        assert one_int.an_int == 42
        #pprint()
        assert self.step_set_attr.setattr(one_int, one_int, 'an_int', 42) is None
        #pprint()
        assert self.step_set_attr.setattr(one_int, one_int, 'an_int', 42) is None

    def test_class__random_guid(self):
        print()
        class Class__Random_Guid:
            an_str : str
            an_guid: Random_Guid
        with_random_guid = Class__Random_Guid()

        value_1 = random_guid()
        assert self.step_set_attr.setattr(with_random_guid, with_random_guid, 'an_guid',  value_1) is None
        assert with_random_guid.an_guid       == value_1
        assert type(with_random_guid.an_guid) is Random_Guid

        value_2 = f'{random_guid()}'
        assert self.step_set_attr.setattr(with_random_guid, with_random_guid, 'an_guid',  value_2) is None
        assert with_random_guid.an_guid       == value_2
        assert type(with_random_guid.an_guid) is Random_Guid

        value_3 = f'{random_guid()}'
        assert self.step_set_attr.setattr(with_random_guid, with_random_guid, 'an_str', value_3) is None
        assert with_random_guid.an_str == value_3
        assert type(with_random_guid.an_str) is str

        value_4 = random_guid()
        assert self.step_set_attr.setattr(with_random_guid, with_random_guid, 'an_str', value_4) is None
        assert with_random_guid.an_str == value_4
        assert type(with_random_guid.an_str) is str

    def test_validate_literal_value(self):
        from typing import Literal
        from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__Set_Attr import type_safe_step_set_attr

        # Test valid Literal values
        annotations = {'status': Literal[200, 404, 500]}
        type_safe_step_set_attr.validate_literal_value(object, annotations, 'status', 200)  # Should pass
        type_safe_step_set_attr.validate_literal_value(object, annotations, 'status', 404)  # Should pass
        type_safe_step_set_attr.validate_literal_value(object, annotations, 'status', 500)  # Should pass

        # Test invalid Literal value
        with pytest.raises(ValueError, match=re.escape("On type, invalid value for 'status': must be one of [200, 404, 500], got 201")):
            type_safe_step_set_attr.validate_literal_value(object, annotations, 'status', 201)

        # Test mixed type Literals
        annotations = {'mixed': Literal["text", 42, True, None]}
        type_safe_step_set_attr.validate_literal_value(object, annotations, 'mixed', "text")  # Should pass
        type_safe_step_set_attr.validate_literal_value(object, annotations, 'mixed', 42)      # Should pass
        type_safe_step_set_attr.validate_literal_value(object, annotations, 'mixed', True)    # Should pass
        type_safe_step_set_attr.validate_literal_value(object, annotations, 'mixed', None)    # Should pass

        with pytest.raises(ValueError, match=re.escape("On type, invalid value for 'mixed': must be one of ['text', 42, True, None], got 'other'")):
            type_safe_step_set_attr.validate_literal_value(object, annotations, 'mixed', "other")

        # Test non-Literal annotations (should pass silently)
        annotations = {'regular': str}
        type_safe_step_set_attr.validate_literal_value(object, annotations, 'regular', "any string")  # Should pass

        # Test missing annotation (should pass silently)
        type_safe_step_set_attr.validate_literal_value(object, {}, 'nonexistent', "anything")  # Should pass

    def test_resolve_value_with_literals(self):

        class Test_Class(Type_Safe):
            format_type: Literal["json", "xml", "yaml"] = "json"
            status_code: Literal[200, 404, 500] = 200
            regular_str: str = "test"
            regular_int: int = 42

        test_obj = Test_Class()
        annotations = test_obj.__annotations__

        # Test valid Literal assignment
        resolved = type_safe_step_set_attr.resolve_value(test_obj, annotations, 'format_type', 'xml')
        assert resolved == 'xml'

        resolved = type_safe_step_set_attr.resolve_value(test_obj, annotations, 'status_code', 404)
        assert resolved == 404

        # Test invalid Literal assignment (should raise user-friendly error)
        with pytest.raises(ValueError, match=re.escape("On Test_Class, invalid value for 'format_type': must be one of ['json', 'xml', 'yaml'], got 'pdf'")):
            type_safe_step_set_attr.resolve_value(test_obj, annotations, 'format_type', 'pdf')

        with pytest.raises(ValueError, match=re.escape("On Test_Class, invalid value for 'status_code': must be one of [200, 404, 500], got 201")):
            type_safe_step_set_attr.resolve_value(test_obj, annotations, 'status_code', 201)

        # Test regular types still work
        resolved = type_safe_step_set_attr.resolve_value(test_obj, annotations, 'regular_str', 'new_value')
        assert resolved == 'new_value'

        resolved = type_safe_step_set_attr.resolve_value(test_obj, annotations, 'regular_int', 100)
        assert resolved == 100

        # Test type conversion for int/str types
        with pytest.raises(ValueError, match=re.escape("On Test_Class, invalid type for attribute 'regular_int'. Expected '<class 'int'>' but got '<class 'str'>")):
            type_safe_step_set_attr.resolve_value(test_obj, annotations, 'regular_int', '99')


        # Test invalid type for regular field (should raise generic type error)
        with pytest.raises(ValueError, match=re.escape("On Test_Class, invalid type for attribute 'regular_str'. Expected '<class 'str'>' but got '<class 'int'>'")):
            type_safe_step_set_attr.resolve_value(test_obj, annotations, 'regular_str', 123)
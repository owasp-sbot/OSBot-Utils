from unittest                                                               import TestCase
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Annotations     import type_safe_annotations
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__Set_Attr   import Type_Safe__Step__Set_Attr
from osbot_utils.utils.Misc                                                 import random_guid
from osbot_utils.helpers.Random_Guid                                        import Random_Guid
#from osbot_utils.helpers.trace.Trace_Call                   import trace_calls


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
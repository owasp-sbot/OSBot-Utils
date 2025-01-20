from unittest                                                  import TestCase
from osbot_utils.type_safe.steps.Type_Safe__Step__Class_Kwargs import Type_Safe__Step__Class_Kwargs
from osbot_utils.helpers.trace.Trace_Call                      import trace_calls


class test_Type_Safe__Step__Class_Kwargs(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.step_class_kwargs = Type_Safe__Step__Class_Kwargs()

    #@trace_calls(include=['*'], show_internals=True, show_duration=True, duration_padding=60)
    def test_class__empty(self):
        class Class__Empty: pass
        assert self.step_class_kwargs.get_cls_kwargs(Class__Empty) == {}

    #@trace_calls(include=['*'], show_internals=True, show_duration=True, duration_padding=60, show_class=True)
    def test_class__with_one_int(self):
        class Class__One_int:
            an_int : int
        assert self.step_class_kwargs.get_cls_kwargs(Class__One_int) == {'an_int': 0}
        #Class__One_int()
        #Class__One_int()
        #Class__One_int()

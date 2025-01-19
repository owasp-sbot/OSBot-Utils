from unittest                                                  import TestCase
from osbot_utils.context_managers.capture_duration             import capture_duration
from osbot_utils.helpers.trace.Trace_Call                      import trace_calls
from osbot_utils.utils.Dev                                     import pprint
from osbot_utils.type_safe.steps.Type_Safe__Step__Class_Kwargs import Type_Safe__Step__Class_Kwargs


class test_Type_Safe__Step__Class_Kwargs(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.step_class_kwargs = Type_Safe__Step__Class_Kwargs()

    #@trace_calls(include=['*'], show_internals=True, show_duration=True, duration_padding=60)
    def test_empty_class(self):
        class EmptyClass: pass
        with capture_duration() as duration:
            assert self.step_class_kwargs.get_cls_kwargs(EmptyClass) == {}

        #pprint(duration.json())
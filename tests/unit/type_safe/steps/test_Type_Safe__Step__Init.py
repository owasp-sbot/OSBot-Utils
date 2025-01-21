from unittest                                                   import TestCase
from osbot_utils.helpers.trace.Trace_Call                       import trace_calls
from osbot_utils.type_safe.Type_Safe                            import Type_Safe
from osbot_utils.type_safe.steps.Type_Safe__Step__Class_Kwargs  import Type_Safe__Step__Class_Kwargs
from osbot_utils.type_safe.steps.Type_Safe__Step__Init          import Type_Safe__Step__Init


class test_Type_Safe__Step__Class_Kwargs(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.step_class_kwargs = Type_Safe__Step__Class_Kwargs()
        cls.step_init         = Type_Safe__Step__Init        ()

    #@trace_calls(include=['*'], show_internals=True, show_duration=True, duration_padding=60)
    def test_init__class__empty(self):
        class Class__Empty: pass
        empty_class = Class__Empty()
        class_kwargs = {}
        kwargs       = {}
        self.step_init.init(empty_class, class_kwargs, **kwargs)
        assert empty_class.__dict__ == {}

    #@trace_calls(include=['*'], show_internals=True, show_duration=True, duration_padding=80)
    def test_init__class_one_int__no_kwargs(self):
        class Class__One_int:
            an_int: int

        one_int = Class__One_int()
        class_kwargs = {'an_int': 0}
        kwargs       = {}
        self.step_init.init(one_int, class_kwargs, **kwargs)
        assert one_int.__dict__ == {'an_int': 0}
        assert one_int.an_int   == 0

    #@trace_calls(include=['*'], show_internals=True, show_duration=True, duration_padding=80)
    def test_init__class_one_int__with_value__no_kwargs(self):
        class Class__One_int:
            an_int: int

        one_int = Class__One_int()
        one_int.an_int = 42
        class_kwargs = {'an_int': 0}
        kwargs       = {}
        self.step_init.init(one_int, class_kwargs, **kwargs)
        assert one_int.__dict__ == {'an_int': 42}
        assert one_int.an_int   == 42

    #@trace_calls(include=['*'], show_internals=True, show_duration=True, duration_padding=80)
    def test_init__class_one_int__no_value__no_kwargs(self):
        class Class__One_int:
            pass

        one_int = Class__One_int()

        class_kwargs = {'an_int': 0}
        kwargs       = {}
        self.step_init.init(one_int, class_kwargs, **kwargs)
        assert one_int.__dict__ == {'an_int': 0}
        assert one_int.an_int   == 0

    @trace_calls(include=['*'], show_internals=True, show_duration=True, duration_padding=80)
    def test_init__class_one_int__with_kwargs(self):
        class Class__One_int:
            an_int: int
        one_int      = Class__One_int()
        class_kwargs = {'an_int': 0 }
        kwargs       = {'an_int': 42}
        self.step_init.init(one_int, class_kwargs, **kwargs)
        assert one_int.__dict__ == {'an_int': 42}
        assert one_int.an_int   == 42


    #@trace_calls(include=['*'], show_internals=True, show_duration=True, duration_padding=80)
    def test_init__type_safe__class_one_int__no_kwargs(self):
        class Class__One_int(Type_Safe):
            an_int: int

        one_int = Class__One_int()

        # assert one_int.__dict__ == {'an_int': 0}
        # assert one_int.an_int   == 0


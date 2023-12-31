import sys
from pprint import pprint
from unittest import TestCase

#from py._code.code import Frame

from osbot_utils.testing.Profiler import Profiler
from osbot_utils.utils.Misc import under_debugger


class An_Class:
    def __init__(self):
        self.local_var = 42

    def an_function(self):
        return self.local_var

class test_Profiler(TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test___enter___exit(self):
        profiler = Profiler()
        profiler.__enter__().__exit__(None, None, None)
        assert len(profiler.events) == 0

    def test_current_profiler(self):
        with Profiler() as profiler:
            assert An_Class().an_function() == 42
            assert profiler.current_profiler() == profiler.profiling_function

        assert profiler.current_profiler() is profiler.previous_profiler
        assert len(profiler.events)      == 4
        assert profiler.events.pop()['f_locals']['self'].local_var == 42

    def test_profiling_function(self):
        frame = sys._getframe(0)  # get current frame
        event = {}
        arg = {}

        profiler = Profiler()
        profiler.profiling_function(frame, event, arg)
        assert len(profiler.events) == 1

    def test_set_on_event(self):
        def on_event(self, frame, event, arg):
            if event == 'return':
                #assert frame.f_locals['self'].local_var == 42          # for this to work we need to handle the two return calls
                frame.f_locals['self'].local_var = 123
                assert frame.f_locals['self'].local_var == 123

        with Profiler() as profiler:
            profiler.set_on_event(on_event)
            assert 123 == An_Class().an_function()

        profiler = Profiler().set_on_event(on_event)
        profiler.profiling_function(sys._getframe(0), {}, {})
        assert profiler.events.pop()['f_locals']['on_event'] == on_event



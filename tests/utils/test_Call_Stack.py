import sys
import traceback
from unittest import TestCase
from unittest.mock import call

from osbot_utils.testing.Patch_Print import Patch_Print
from osbot_utils.utils.Call_Stack import call_stack_current_frame, call_stack_format_stack, call_stack_frames, \
    call_stack_frames_data, Call_Stack
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Objects import obj_info, obj_data


class test_Call_Stack(TestCase):


    def setUp(self):
        self.call_stack = Call_Stack()

    def test_capture(self):
        with self.call_stack:
            def an_method():
                a = self.call_stack.capture()
            an_method()

        with Patch_Print() as _:
            self.call_stack.print()
        assert _.call_args_list() == [call(),
                                      call('┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐'),
                                      call('│ caller_line                   │ depth │ function_name │ line_number │ local_self                      │ method_line             │ module          │'),
                                      call('├───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤'),
                                      call('│ a = self.call_stack.capture() │ 0     │ an_method     │ 23          │ test_Call_Stack.test_Call_Stack │ def an_method():        │ test_Call_Stack │'),
                                      call('│ an_method()                   │ 1     │ test_capture  │ 24          │ test_Call_Stack.test_Call_Stack │ def test_capture(self): │ test_Call_Stack │'),
                                      call('└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘')]






    # static methods

    def test_call_stack_current_frame(self):
        frame = call_stack_current_frame()

        assert list_set(obj_data(frame)) == ['clear', 'f_back', 'f_builtins', 'f_code',
                                             'f_globals', 'f_lasti', 'f_lineno', 'f_locals',
                                             'f_trace', 'f_trace_lines', 'f_trace_opcodes']

    def test_call_stack_format_stack(self):
        formated_stack = call_stack_format_stack(depth=2)
        assert len(formated_stack) ==2
        for item in formated_stack:
            assert type(item) is str

    def test_call_stack_frames(self):
        assert len(call_stack_frames(       )) > 20
        assert len(call_stack_frames(depth=1)) == 1
        assert len(call_stack_frames(depth=2)) == 2
        assert len(call_stack_frames(depth=5)) == 5

    def test_call_stack_frames_data(self):
        frames_data = call_stack_frames_data(depth=4)
        for frame_data in frames_data:
            assert list_set(frame_data) == ['filename', 'line', 'lineno', 'locals', 'name']

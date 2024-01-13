import sys
import traceback
from unittest import TestCase
from unittest.mock import call

from osbot_utils.testing.Patch_Print import Patch_Print
from osbot_utils.utils.Call_Stack import call_stack_current_frame, call_stack_format_stack, call_stack_frames, \
    call_stack_frames_data, Call_Stack, PRINT_STACK_COLOR_THEMES
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Objects import obj_info, obj_data



class test_Call_Stack(TestCase):


    def setUp(self):
        self.call_stack = Call_Stack()

    def test_print(self):

        with self.call_stack:
            def level_1():
                level_2()

            def level_2():
                level_3()

            def level_3():
                a = self.call_stack.capture(skip_caller=False)
            level_1()
        with Patch_Print() as _:
            self.call_stack.print()
        assert _.call_args_list() == [call(),
                                      call(),
                                      call('\x1b[34m┌ test_Call_Stack.level_3\x1b[0m'),
                                      call('\x1b[0m│ test_Call_Stack.level_2\x1b[0m'),
                                      call('\x1b[0m│ test_Call_Stack.level_1\x1b[0m'),
                                      call('\x1b[32m└ test_Call_Stack.test_print\x1b[0m')]

    def test_print_table(self):
        with self.call_stack:
            def an_method():
                a = self.call_stack.capture(skip_caller=False)
            an_method()

        with Patch_Print() as _:
            self.call_stack.print_table()
        assert _.call_args_list() == [call(),
                                      call('┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐'),
                                      call('│ module          │ method_name      │ caller_line                                    │ method_line                 │ local_self                      │ line_number │ depth │'),
                                      call('├───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤'),
                                      call('│ test_Call_Stack │ an_method        │ a = self.call_stack.capture(skip_caller=False) │ def an_method():            │ test_Call_Stack.test_Call_Stack │ 45          │ 0     │'),
                                      call('│ test_Call_Stack │ test_print_table │ an_method()                                    │ def test_print_table(self): │ test_Call_Stack.test_Call_Stack │ 46          │ 1     │'),
                                      call('└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘')]



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

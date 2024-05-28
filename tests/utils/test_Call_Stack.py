import sys
import traceback
from unittest import TestCase
from unittest.mock import call

import pytest

from osbot_utils.testing.Patch_Print import Patch_Print
from osbot_utils.utils.Call_Stack import call_stack_current_frame, call_stack_format_stack, call_stack_frames, \
    call_stack_frames_data, Call_Stack, PRINT_STACK_COLOR_THEMES
from osbot_utils.utils.Env import platform_darwin, env__terminal_xterm
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Objects import obj_info, obj_data



class test_Call_Stack(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if env__terminal_xterm():
            pytest.skip('Skipping tests that require terminal_xterm')  # todo: figure out why multiple of these were failing inside docker


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

        assert _.call_args_list() == [call('\x1b[34m┌ test_Call_Stack.level_3\x1b[0m'),
                                      call('\x1b[0m│ test_Call_Stack.level_2\x1b[0m'),
                                      call('\x1b[0m│ test_Call_Stack.level_1\x1b[0m'),
                                      call('\x1b[32m└ test_Call_Stack.test_print\x1b[0m')]

    @pytest.mark.skip("needs fixing (started failing on new python versions") # todo: fix test
    def test_print_table(self):
        with self.call_stack:
            def an_method():
                a = self.call_stack.capture(skip_caller=False)
            an_method()
        headers_to_hide = ['line_number']

        with Patch_Print() as _:
            self.call_stack.print_table(headers_to_hide)

        assert _.call_args_list() == [call(),
                                      call('┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐'),
                                      call('│ module          │ method_name      │ caller_line                                    │ method_line                 │ local_self                      │ depth │'),
                                      call('├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤'),
                                      call('│ test_Call_Stack │ an_method        │ a = self.call_stack.capture(skip_caller=False) │ def an_method():            │ test_Call_Stack.test_Call_Stack │ 0     │'),
                                      call('│ test_Call_Stack │ test_print_table │ an_method()                                    │ def test_print_table(self): │ test_Call_Stack.test_Call_Stack │ 1     │'),
                                      call('└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘')]

    @pytest.mark.skip("needs fixing (started failing on new python versions")  # todo: fix test
    def test_stack_lines__source_code(self):
        with self.call_stack:
            def level_1():
                level_2()

            def level_2():
                level_3()

            def level_3():
                self.call_stack.capture(skip_caller=False)

            level_1()

        calls_source_code = self.call_stack.calls__source_code()
        assert calls_source_code == [ 'self.call_stack.capture(skip_caller=False)',
                                      'level_3()',
                                      'level_2()',
                                      'level_1()']
        with Patch_Print() as _:
            self.call_stack.print__source_code()

        assert _.call_args_list() == [call('\x1b[34m┌ self.call_stack.capture(skip_caller=False)\x1b[0m'),
                                      call('\x1b[0m│ level_3()\x1b[0m'),
                                      call('\x1b[0m│ level_2()\x1b[0m'),
                                      call('\x1b[32m└ level_1()\x1b[0m')]




    # static methods
    # todo: refactor these static methods to be in a separate class

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
            assert list_set(frame_data) == ['colno', 'end_colno', 'end_lineno', 'filename', 'line', 'lineno', 'locals', 'name']


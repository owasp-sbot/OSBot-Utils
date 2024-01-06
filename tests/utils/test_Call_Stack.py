import sys
import traceback
from unittest import TestCase

from osbot_utils.utils.Call_Stack import call_stack_current_frame, call_stack_format_stack, call_stack_frames, \
    call_stack_frames_data
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Objects import obj_info, obj_data


class test_Call_Stack(TestCase):


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

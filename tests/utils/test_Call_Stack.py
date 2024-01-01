import sys
import traceback
from unittest import TestCase

from osbot_utils.utils.Call_Stack import Call_Stack
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Objects import obj_info, obj_data


class test_Call_Stack(TestCase):

    def setUp(self):
        self.call_stack = Call_Stack()

    def test_current_frame(self):
        frame = self.call_stack.current_frame()

        assert list_set(obj_data(frame)) == ['clear', 'f_back', 'f_builtins', 'f_code',
                                             'f_globals', 'f_lasti', 'f_lineno', 'f_locals',
                                             'f_trace', 'f_trace_lines', 'f_trace_opcodes']

    def test_format_stack(self):
        formated_stack = self.call_stack.format_stack(depth=2)
        assert len(formated_stack) ==2
        for item in formated_stack:
            assert type(item) is str

    def test_frames(self):
        assert len(self.call_stack.frames(       )) > 20
        assert len(self.call_stack.frames(depth=1)) == 1
        assert len(self.call_stack.frames(depth=2)) == 2
        assert len(self.call_stack.frames(depth=5)) == 5

    def test_frames_data(self):
        frames_data = self.call_stack.frames_data(depth=4)
        for frame_data in frames_data:
            assert list_set(frame_data) == ['filename', 'line', 'lineno', 'locals', 'name']

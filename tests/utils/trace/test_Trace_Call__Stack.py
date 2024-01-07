from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.Misc import random_string, random_int

from osbot_utils.utils.trace.Trace_Call__Stack import Trace_Call__Stack
from osbot_utils.utils.trace.Trace_Call__Stack_Node import Trace_Call__Stack_Node


class test_Trace_Call__Stack(TestCase):

    def setUp(self):
        self.stack = Trace_Call__Stack()

    def test_add_node(self):

        title      = random_string()
        call_index = random_int   ()
        with self.stack as _:
            assert _.size() == 0
            assert _.add_node(title, call_index) is True
            assert _.size() == 1
            assert _.bottom() == _.top()
            assert _.top().info() == f'Stack_Node: call_index:{call_index} | name: {title} | children: 0 | source_code: True'
            assert _.top()        == Trace_Call__Stack_Node(call_index=call_index, name=title)
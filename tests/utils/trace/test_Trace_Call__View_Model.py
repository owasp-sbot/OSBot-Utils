from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.trace.Trace_Call import Trace_Call
from osbot_utils.utils.trace.Trace_Call__Stack_Node import Trace_Call__Stack_Node

from osbot_utils.utils.trace.Trace_Call__View_Model import Trace_Call__View_Model
from tests.utils.trace.test_Trace_Call import dummy_function, another_function


class test_Trace_Call__View_Model(TestCase):

    def test_create(self):
        trace_call = Trace_Call()
        trace_call.trace_call_handler.config.trace_capture_start_with = ['test']
        trace_call.start()
        dummy_function()
        another_function()
        trace_call.stop()


        handler               = trace_call.trace_call_handler
        trace_call_view_model = trace_call.trace_call_view_model
        stack                 = handler.stack
        trace_call_view_model.create(stack)  # Process data to create the view model
        trace_call_view_model.fix_view_mode()  # Fix the view mode for the last node

        view_model = trace_call_view_model.view_model
        assert len(view_model) == 4, "Four function calls should be traced"
        assert view_model[0]['method_name'] == handler.trace_title    , "First function in view_model should be 'traces'"
        assert view_model[1]['method_name'] == 'dummy_function'          , "2nd function in view_model should be 'dummy_function'"
        assert view_model[2]['method_name'] == 'another_function'        , "3rd function in view_model should be 'another_function'"
        assert view_model[3]['method_name'] == 'dummy_function'          , "4th function in view_model should be 'dummy_function'"


    @patch('builtins.print')
    def test_create__via_Trace_Call_with(self, builtins_print):
        with Trace_Call() as trace_call:
            trace_call.trace_call_handler.config.trace_capture_start_with = ['tests']
            trace_call.trace_call_print_traces.config.print_on_exit = True  # To hit the 'print_traces' line in __exit__
            trace_call.trace_call_print_traces.config.show_parent_info = False
            dummy_function()
            another_function()

        handler               = trace_call.trace_call_handler
        trace_call_view_model = trace_call.trace_call_view_model
        view_model            = trace_call_view_model.view_model
        assert len(view_model) == 4, "Four function calls should be traced"
        assert view_model[0]['method_name'] == handler.trace_title    , "First function in view_model should be 'traces'"
        assert view_model[1]['method_name'] == 'dummy_function'          , "2nd function in view_model should be 'dummy_function'"
        assert view_model[2]['method_name'] == 'another_function'        , "3rd function in view_model should be 'another_function'"
        assert view_model[3]['method_name'] == 'dummy_function'          , "4th function in view_model should be 'dummy_function'"

        assert builtins_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 4 traces captured\n'),
                                                 call('\x1b[1m📦  Trace Session\x1b[0m'),
                                                 call('\x1b[1m│   ├── 🧩️ dummy_function\x1b[0m'),
                                                 call('\x1b[1m│   └── 🔗️ another_function\x1b[0m'),
                                                 call('\x1b[1m└────── 🧩️ dummy_function\x1b[0m')]


    def test_fix_view_mode(self):
        trace_call_view_model = Trace_Call__View_Model()
        trace_node_1          = Trace_Call__Stack_Node()
        trace_node_2          = Trace_Call__Stack_Node()
        trace_node_1.children.append(trace_node_2)
        stack_data            = [trace_node_1]
        trace_call_view_model.create(stack_data)

        view_model = trace_call_view_model.view_model
        assert len(view_model) == 2, "Two functions should be in the created view_model"
        trace_call_view_model.fix_view_mode()
        assert view_model[-1]['prefix'] == '└───', "Last node prefix should be updated"
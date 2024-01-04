import inspect
from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import base_classes
from osbot_utils.utils.trace.Trace_Call import Trace_Call


def dummy_function():
    pass

def another_function():
    dummy_function()

class test_Trace_Call(TestCase):

    def test___default_kwargs(self):
        assert Trace_Call.__default_kwargs__() == dict(title                   = None  ,
                                                       print_on_exit           = False ,
                                                       print_locals            = False ,
                                                       capture_source_code     = False ,
                                                       ignore_start_with       = None  ,
                                                       capture_start_with      = None  ,
                                                       print_max_string_length = None  ,
                                                       show_parent_info        = True  ,
                                                       show_caller             = False ,
                                                       show_method_parent      = False ,
                                                       show_source_code_path   = False )

    def test___init__(self):
        trace_call = Trace_Call()
        assert Kwargs_To_Self in base_classes(Trace_Call)
        assert trace_call.__locals__() == {  **trace_call.__default_kwargs__(),
                                             'call_index'                   : 0,
                                             'prev_trace_function'          : None,
                                             'print_max_string_length'      : 100,
                                             'print_show_caller'            : False,
                                             'print_show_locals'            : False,
                                             'print_show_method_parent'     : False,
                                             'print_show_parent_info'       : True,
                                             'print_show_source_code_path'  : False,
                                             'print_traces_on_exit'         : False,
                                             'stack'                        : [{'call_index': 0, 'children': [], 'name': 'Trace Session'}],
                                             'trace_capture_all'            : False,
                                             'trace_capture_source_code'    : False,
                                             'trace_capture_start_with'     : ['cbr_website_beta'],
                                             'trace_ignore_internals'       : True,
                                             'trace_ignore_start_with'      : [],
                                             'trace_title'                  : 'Trace Session',
                                             'view_model'                   : []}

    @patch('builtins.print')
    def test_trace_call(self, builtins_print):

        # Test the initialization and its attributes
        trace_call = Trace_Call()
        assert trace_call.prev_trace_function  is None      , "prev_trace_function should be None initially"
        assert trace_call.call_index           == 0         , "call_index should be 0 initially"
        assert trace_call.view_model           == []        , "view_model should be empty initially"
        assert trace_call.print_traces_on_exit is False     , "print_traces_on_exit should be False initially"
        assert trace_call.stack                == [{"name": trace_call.trace_title, "children": [], "call_index": 0}], "Initial stack state not correct"

        # Test the enter and exit methods
        with Trace_Call() as trace_call:
            trace_call.trace_capture_start_with   = ['test_Trace_Call']
            trace_call.print_traces_on_exit = True                          # To hit the 'print_traces' line in __exit__
            dummy_function()
            another_function()

        assert len(trace_call.view_model) == 4, "Four function calls should be traced"
        assert trace_call.view_model[0]['method_name'] == trace_call.trace_title    , "First function in view_model should be 'traces'"
        assert trace_call.view_model[1]['method_name'] == 'dummy_function'          , "2nd function in view_model should be 'dummy_function'"
        assert trace_call.view_model[2]['method_name'] == 'another_function'        , "3rd function in view_model should be 'another_function'"
        assert trace_call.view_model[3]['method_name'] == 'dummy_function'          , "4th function in view_model should be 'dummy_function'"

        # Test the create_view_model function
        stack_data = [{"name": "some_function", "children": [{"name": "child_function", "children": []}]}]
        view_model = trace_call.create_view_model(stack_data)
        assert len(view_model) == 2, "Two functions should be in the created view_model"

        # Test fix_view_mode function
        trace_call.view_model = view_model
        trace_call.fix_view_mode()
        assert trace_call.view_model[-1]['prefix'] == '└───', "Last node prefix should be updated"

        assert builtins_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 4 traces captured\n'),
                                                 call('\x1b[1m📦  Trace Session\x1b[0m'),
                                                 call('\x1b[1m│   ├── 🧩️ dummy_function\x1b[0m                                    test_Trace_Call'),
                                                 call('\x1b[1m│   └── 🔗️ another_function\x1b[0m                                  test_Trace_Call'),
                                                 call('\x1b[1m└────── 🧩️ dummy_function\x1b[0m                                    test_Trace_Call')] != []

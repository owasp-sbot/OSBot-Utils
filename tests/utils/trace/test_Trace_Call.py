import inspect
import os
import sys
from pprint import pprint
from unittest import TestCase
from unittest.mock import patch, call

from dotenv import load_dotenv

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.Dict_To_Attr import Dict_To_Attr
from osbot_utils.utils.Functions import method_line_number
from osbot_utils.utils.Misc import random_value

from osbot_utils.utils.Objects import base_classes, obj_info
from osbot_utils.utils.trace.Trace_Call import Trace_Call, trace_calls


def dummy_function():
    a=12
    pass

def another_function():
    dummy_function()

class test_Trace_Call(TestCase):


    def setUp(self):
        self.trace_call = Trace_Call()
        self.handler    = self.trace_call.trace_call_handler

    def test___default_kwargs(self):
        assert Trace_Call.__default_kwargs__() == dict(print_on_exit           = False ,
                                                       print_locals            = False ,
                                                       capture_source_code     = False ,
                                                       ignore_start_with       = None  ,
                                                       capture_start_with      = None  ,
                                                       print_max_string_length = None  ,
                                                       title                   = None  ,
                                                       show_parent_info        = True  ,
                                                       show_caller             = False ,
                                                       show_method_parent      = False ,
                                                       show_source_code_path   = False )

    def test___init__(self):
        assert Kwargs_To_Self in base_classes(Trace_Call)
        assert self.trace_call.__locals__() == { **self.trace_call.__default_kwargs__(),
                                                 'prev_trace_function'          : None,
                                                 'print_max_string_length'      : 100,
                                                 'print_show_caller'            : False,
                                                 'print_show_locals'            : False,
                                                 'print_show_method_parent'     : False,
                                                 'print_show_parent_info'       : True,
                                                 'print_show_source_code_path'  : False,
                                                 'print_traces_on_exit'         : False,
                                                 'stack'                        : [{'call_index': 0, 'children': [], 'name': 'Trace Session'}],
                                                 'trace_call_handler'           : self.trace_call.trace_call_handler                          ,
                                                 'view_model'                   : []}

    def test___exit__(self):
        assert self.trace_call.view_model == []
        with patch.object(Trace_Call, 'stop') as mock_stop:
            self.trace_call.__exit__(None, None, None)

        mock_stop.assert_called_with()

        assert self.trace_call.view_model == [{ 'prefix': '└───', 'tree_branch': '─── ', 'emoji': '📦 ',
                                                'method_name': 'Trace Session', 'method_parent': '',
                                                'parent_info': '', 'locals': None, 'source_code': None,
                                                'source_code_caller': None, 'source_code_location': None}]


    @patch('builtins.print')
    def test_decorator__trace_calls(self, builtins_print):

            @trace_calls(include=['test', 'pprint'], print=True)
            def method_a():
                method_b()

            def method_b() :
                pprint('an message')

            method_a()

            assert builtins_print.call_args_list == [call(),
                                                     call('--------- CALL TRACER ----------'),
                                                     call('Here are the 6 traces captured\n'),
                                                     call('\x1b[1m📦  Trace Session\x1b[0m'),
                                                     call('\x1b[1m│   └── 🔗️ method_a\x1b[0m'),
                                                     call('\x1b[1m│       └── 🔗️ method_b\x1b[0m'),
                                                     call('\x1b[1m│           └── 🔗️ pprint\x1b[0m'),
                                                     call('\x1b[1m│               └── 🔗️ pprint\x1b[0m'),
                                                     call('\x1b[1m└────── 🧩️ format\x1b[0m')] != []


    def test_add_trace_ignore(self):
        value = random_value()
        assert self.trace_call.trace_call_handler.trace_ignore_start_with == []
        assert self.trace_call.add_trace_ignore(value) is None
        assert self.trace_call.trace_call_handler.trace_ignore_start_with == [value]

    def test_trace(self):
        title = random_value()
        assert self.trace_call.stack == [{'call_index': 0, 'children': [], 'name': 'Trace Session'}]
        assert self.trace_call.trace(title) is self.trace_call

    def test_formatted_local_data(self):
        with patch('builtins.print') as mock_print:
            self.trace_call.formatted_local_data(local_data=None, formatted_line=None)
            assert mock_print.call_args_list == []

        with patch('builtins.print') as mock_print:
            local_data     = {'a':42, '_b':'_ignored'}
            formatted_line = ''
            expected_calls = [call('       🔖 a = \x1b[92m42\x1b[0m')]
            self.trace_call.formatted_local_data(local_data=local_data, formatted_line=formatted_line)
            assert mock_print.call_args_list == expected_calls

        with patch('builtins.print') as mock_print:
            local_data     = {'an_dict': {'a': 42 }}
            formatted_line = ''
            expected_calls = [call("       🔖 an_dict = \x1b[92m{'a': 42}\x1b[0m")]
            self.trace_call.formatted_local_data(local_data=local_data, formatted_line=formatted_line)
            assert mock_print.call_args_list == expected_calls

        with patch('builtins.print') as mock_print:
            local_data     = {'an_method': mock_print}
            formatted_line = ''
            expected_calls = [call('       🔖 an_method = \x1b[94mMagicMock\x1b[0m')]
            self.trace_call.formatted_local_data(local_data=local_data, formatted_line=formatted_line)
            assert mock_print.call_args_list == expected_calls

        with patch('builtins.print') as mock_print:
            self.trace_call.print_max_string_length = 2
            local_data     = {'large_string': 'xx' * self.trace_call.print_max_string_length}
            formatted_line = ''
            expected_calls = [call('       🔖 large_string = \x1b[92mxx...\x1b[0m')]
            self.trace_call.formatted_local_data(local_data=local_data, formatted_line=formatted_line)
            assert mock_print.call_args_list == expected_calls


    def test_print_traces(self):

        with patch('builtins.print') as mock_print:
            self.trace_call.print_traces()
            expected_calls = [call(),
                              call('--------- CALL TRACER ----------'),
                              call('Here are the 0 traces captured\n')]
            assert mock_print.call_args_list == expected_calls

        #self.trace_call.print_traces_on_exit = True
        self.handler.trace_capture_start_with =['test']
        with self.trace_call:
            another_function()

        with patch('builtins.print') as mock_print:
            self.trace_call.print_traces()

            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'         ),
                                                 call('Here are the 3 traces captured\n'         ),
                                                 call('\x1b[1m📦  Trace Session\x1b[0m'          ),
                                                 call('\x1b[1m│   └── 🔗️ another_function\x1b[0m                                  test_Trace_Call'),
                                                 call('\x1b[1m└────── 🧩️ dummy_function\x1b[0m                                    test_Trace_Call')]

        with patch('builtins.print') as mock_print:
            self.trace_call.print_show_method_parent = True
            self.trace_call.print_traces()
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 3 traces captured\n'),
                                                 call('\x1b[1m📦  \x1b[38;2;118;138;118m\x1b[0m.\x1b[1mTrace Session\x1b[0m\x1b[0m'),
                                                 call('\x1b[1m│   └── 🔗️ \x1b[38;2;118;138;118mtest_Trace_Call\x1b[0m.\x1b[1manother_function\x1b[0m\x1b[0m'),
                                                 call('\x1b[1m└────── 🧩️ \x1b[38;2;118;138;118mtest_Trace_Call\x1b[0m.\x1b[1mdummy_function\x1b[0m\x1b[0m')]
        #with patch('builtins.print') as mock_print:

        self.handler.trace_capture_start_with  = ['test']
        self.handler.trace_capture_source_code = True
        self.trace_call.print_show_caller        = True
        with self.trace_call:
            another_function()
        with patch('builtins.print') as mock_print:
            self.trace_call.print_traces()
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 5 traces captured\n'),
                                                 call('🔼️\x1b[1mNone\x1b[0m'),
                                                 call('➡️📦  \x1b[90m\x1b[38;2;118;138;118m\x1b[0m.\x1b[1mTrace Session\x1b[0m\x1b[0m'),
                                                 call('│   ├── 🔼️\x1b[1m\x1b[0m'),
                                                 call('│   ├── ➡️🔗️ \x1b[90m\x1b[38;2;118;138;118mtest_Trace_Call\x1b[0m.\x1b[1manother_function\x1b[0m\x1b[0m'),
                                                 call('│   │   └── 🔼️\x1b[1m\x1b[0m'),
                                                 call('│   │   └── ➡️🧩️ \x1b[90m\x1b[38;2;118;138;118mtest_Trace_Call\x1b[0m.\x1b[1mdummy_function\x1b[0m\x1b[0m'),
                                                 call('│   └── 🔼️\x1b[1manother_function()\x1b[0m'),
                                                 call('│   └── ➡️🔗️ \x1b[90mdef another_function():\x1b[0m'),
                                                 call('└────── 🔼️\x1b[1mdummy_function()\x1b[0m'),
                                                 call('└────── ➡️🧩️ \x1b[90mdef dummy_function():\x1b[0m')]

        self.trace_call.print_show_caller = False
        with patch('builtins.print') as mock_print:
            self.trace_call.print_traces()
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 5 traces captured\n'),
                                                 call('➡️📦  \x1b[1m\x1b[38;2;118;138;118m\x1b[0m.\x1b[1mTrace Session\x1b[0m\x1b[0m'),
                                                 call('│   ├── ➡️🔗️ \x1b[1m\x1b[38;2;118;138;118mtest_Trace_Call\x1b[0m.\x1b[1manother_function\x1b[0m\x1b[0m'),
                                                 call('│   │   └── ➡️🧩️ \x1b[1m\x1b[38;2;118;138;118mtest_Trace_Call\x1b[0m.\x1b[1mdummy_function\x1b[0m\x1b[0m'),
                                                 call('│   └── ➡️🔗️ \x1b[1mdef another_function():\x1b[0m'),
                                                 call('└────── ➡️🧩️ \x1b[1mdef dummy_function():\x1b[0m')] != []

        self.trace_call.print_show_locals = True
        with patch('builtins.print') as mock_print:
            with self.trace_call:
                another_function()
            self.trace_call.print_traces()
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 7 traces captured\n'),
                                                 call('➡️📦  \x1b[1m\x1b[38;2;118;138;118m\x1b[0m.\x1b[1mTrace Session\x1b[0m\x1b[0m'),
                                                 call('│   ├── ➡️🔗️ \x1b[1m\x1b[38;2;118;138;118mtest_Trace_Call\x1b[0m.\x1b[1manother_function\x1b[0m\x1b[0m'),
                                                 call('│   │   └── ➡️🧩️ \x1b[1m\x1b[38;2;118;138;118mtest_Trace_Call\x1b[0m.\x1b[1mdummy_function\x1b[0m\x1b[0m'),
                                                 call('                   🔖 a = \x1b[92m12\x1b[0m'),
                                                 call('│   ├── ➡️🔗️ \x1b[1mdef another_function():\x1b[0m'),
                                                 call('│   │   └── ➡️🧩️ \x1b[1mdef dummy_function():\x1b[0m'),
                                                 call('                   🔖 a = \x1b[92m12\x1b[0m'),
                                                 call('│   └── ➡️🔗️ \x1b[1mdef another_function():\x1b[0m'),
                                                 call('└────── ➡️🧩️ \x1b[1mdef dummy_function():\x1b[0m'),
                                                 call('               🔖 a = \x1b[92m12\x1b[0m')]




            #assert mock_print.call_args_list == []

    def test_stop(self):
        prev_trace_function = None
        with patch('sys.settrace') as mock_systrace:
            self.trace_call.stop()
            assert self.trace_call.prev_trace_function is prev_trace_function
            mock_systrace.assert_called_with(prev_trace_function)
        prev_trace_function = '___prev_trace_function___'
        with patch('sys.settrace') as mock_systrace:
            self.trace_call.prev_trace_function = prev_trace_function
            self.trace_call.stop()
            assert self.trace_call.prev_trace_function == prev_trace_function
            mock_systrace.assert_called_with(prev_trace_function)


    @patch('builtins.print')
    def test_trace_calls(self, builtins_print):

        # Test the initialization and its attributes
        trace_call = Trace_Call()
        handler    = trace_call.trace_call_handler
        assert trace_call.prev_trace_function  is None      , "prev_trace_function should be None initially"
        assert handler.call_index              == 0         , "call_index should be 0 initially"
        assert trace_call.view_model           == []        , "view_model should be empty initially"
        assert trace_call.print_traces_on_exit is False     , "print_traces_on_exit should be False initially"
        assert trace_call.stack                == [{"name": handler.trace_title, "children": [], "call_index": 0}], "Initial stack state not correct"


        # Test the enter and exit methods
        with Trace_Call() as trace_call:
            trace_call.trace_call_handler.trace_capture_start_with   = ['test_Trace_Call']
            trace_call.print_traces_on_exit = True                          # To hit the 'print_traces' line in __exit__
            dummy_function()
            another_function()

        assert len(trace_call.view_model) == 4, "Four function calls should be traced"
        assert trace_call.view_model[0]['method_name'] == handler.trace_title    , "First function in view_model should be 'traces'"
        assert trace_call.view_model[1]['method_name'] == 'dummy_function'          , "2nd function in view_model should be 'dummy_function'"
        assert trace_call.view_model[2]['method_name'] == 'another_function'        , "3rd function in view_model should be 'another_function'"
        assert trace_call.view_model[3]['method_name'] == 'dummy_function'          , "4th function in view_model should be 'dummy_function'"
        return
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

    def test_trace_calls__direct_invoke(self):
        frame   = sys._getframe()         # get a valid frame object
        event   = 'call'
        arg     = None

        handler = self.trace_call.trace_call_handler
        handler.trace_capture_all = True
        handler.trace_calls(frame, event, arg)

        stack_0 = self.trace_call.stack[0]
        stack_1 = self.trace_call.stack[1]




        assert stack_0 == dict(call_index = 0               ,
                               children   =  [stack_1]      ,
                               name       = 'Trace Session' )


        stack_1_locals = dict(stack_1.get('locals'))
        del stack_1['locals']
        del stack_1_locals['handler']

        assert stack_1_locals ==   { '__trace_depth': 2,
                                    'arg': None,
                                    'event': 'call',
                                    'frame': frame,
                                    'self':stack_1_locals.get('self')}
        assert stack_1 == dict(call_index=1,
                               children=[],
                               name = 'test_Trace_Call.test_Trace_Call.test_trace_calls__direct_invoke',
                               source_code          =  '',
                               source_code_caller   = '' ,
                               source_code_location = '')

        assert len(self.trace_call.stack) == 2

        self.trace_call.process_data()
        with patch('builtins.print') as mock_print:
            self.trace_call.print_show_parent_info = False
            self.trace_call.print_traces()
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 3 traces captured\n'),
                                                 call('\x1b[1m📦  Trace Session\x1b[0m'),
                                                 call('\x1b[1m│   └── 🧩️ test_trace_calls__direct_invoke\x1b[0m'),
                                                 call('\x1b[1m📦  test_trace_calls__direct_invoke\x1b[0m')]



    def test_trace_calls__direct_invoke__variations(self):
        self.handler.trace_capture_start_with = ['test']
        self.handler.trace_capture_source_code = True
        self.handler.trace_calls( sys._getframe(),  'call', None)

        method_in_frame         = test_Trace_Call.test_trace_calls__direct_invoke__variations
        source_code_file        = __file__
        source_code_line_number = method_line_number(method_in_frame) + 3
        source_code_location    = f'{source_code_file}:{source_code_line_number}'



        stack_1 = self.trace_call.stack[1]
        assert stack_1.get('name'                ) == 'test_Trace_Call.test_Trace_Call.test_trace_calls__direct_invoke__variations'
        assert stack_1.get('source_code'         ) == "self.handler.trace_calls( sys._getframe(),  'call', None)"
        assert stack_1.get('source_code_caller'  ) == 'method()'
        assert stack_1.get('source_code_location') == source_code_location
        assert len(self.trace_call.stack) == 2


        with patch('builtins.print') as mock_print:
            self.trace_call.print_show_parent_info = False
            self.trace_call.process_data()
            self.trace_call.print_traces()
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 3 traces captured\n'),
                                                 call('➡️📦  \x1b[1mTrace Session\x1b[0m'),
                                                 call("│   └── ➡️🧩️ \x1b[1mself.handler.trace_calls( sys._getframe(),  'call', None)\x1b[0m"),
                                                 call("➡️📦  \x1b[1mself.handler.trace_calls( sys._getframe(),  'call', None)\x1b[0m")] != []
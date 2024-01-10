import os
from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.Misc import random_number, wait_for, in_github_action

from osbot_utils.utils.trace.Trace_Call import Trace_Call
from osbot_utils.utils.trace.Trace_Call__Handler import DEFAULT_ROOT_NODE_NODE_TITLE
from osbot_utils.utils.trace.Trace_Call__Print_Traces import Trace_Call__Print_Traces
from tests.utils.trace.test_Trace_Call import another_function


class test_Trace_Call__Print_Traces(TestCase):

    def setUp(self):
            self.print_traces = Trace_Call__Print_Traces()

    def test_formatted_local_data(self):
        with patch('builtins.print') as mock_print:
            self.print_traces.formatted_local_data(local_data=None, formatted_line=None)
            assert mock_print.call_args_list == []

        with patch('builtins.print') as mock_print:
            local_data     = {'a':42, '_b':'_ignored'}
            formatted_line = ''
            expected_calls = [call('│       🔖 \x1b[1m\x1b[38;2;120;120;120ma\x1b[0m = \x1b[92m42\x1b[0m')]
            self.print_traces.formatted_local_data(local_data=local_data, formatted_line=formatted_line)
            assert mock_print.call_args_list == expected_calls

        with patch('builtins.print') as mock_print:
            local_data     = {'an_dict': {'a': 42 }}
            formatted_line = ''
            expected_calls = [call("│       🔖 \x1b[1m\x1b[38;2;120;120;120man_dict\x1b[0m = \x1b[92m{'a': 42}\x1b[0m")]
            self.print_traces.formatted_local_data(local_data=local_data, formatted_line=formatted_line)
            assert mock_print.call_args_list == expected_calls

        with patch('builtins.print') as mock_print:
            local_data     = {'an_method': mock_print}
            formatted_line = ''
            expected_calls = [call('│       🔖 \x1b[1m\x1b[38;2;120;120;120man_method\x1b[0m = \x1b[94mMagicMock\x1b[0m')]
            self.print_traces.formatted_local_data(local_data=local_data, formatted_line=formatted_line)
            assert mock_print.call_args_list == expected_calls

        with patch('builtins.print') as mock_print:
            self.print_traces.config.print_max_string_length = 2
            local_data     = {'large_string': 'xx' * self.print_traces.config.print_max_string_length}
            formatted_line = ''
            expected_calls =  [call('│       🔖 \x1b[1m\x1b[38;2;120;120;120mlarge_string\x1b[0m = \x1b[92mxx...\x1b[0m')]
            self.print_traces.formatted_local_data(local_data=local_data, formatted_line=formatted_line)
            assert mock_print.call_args_list == expected_calls

    def test_print_traces(self):

        trace_call = Trace_Call()
        handler    = trace_call.trace_call_handler

        with patch('builtins.print') as mock_print:
            trace_call.trace_call_print_traces.print_traces([], False)
            expected_calls = [call(),
                              call('--------- CALL TRACER ----------'),
                              call('Here are the 0 traces captured\n')]
            assert mock_print.call_args_list == expected_calls

        handler.config.trace_capture_start_with =['test']

        with trace_call:
            another_function()

        view_model                = trace_call.create_view_model()
        trace_capture_source_code = trace_call.trace_call_handler.config.trace_capture_source_code
        trace_call.trace_call_print_traces.config.show_parent_info = True
        with patch('builtins.print') as mock_print:
            trace_call.trace_call_print_traces.print_traces(view_model, trace_capture_source_code)
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 3 traces captured\n'),
                                                 call('\x1b[1m📦  Trace Session\x1b[0m'),
                                                 call('\x1b[1m│   └── 🔗️ another_function\x1b[0m                                  tests.utils.trace.test_Trace_Call'),
                                                 call('\x1b[1m└────────── 🧩️ dummy_function\x1b[0m                                tests.utils.trace.test_Trace_Call')]


        with patch('builtins.print') as mock_print:
            trace_call.trace_call_print_traces.config.show_parent_info  = False
            trace_call.trace_call_print_traces.config.show_method_class = True
            trace_call.trace_call_print_traces.print_traces(view_model, trace_capture_source_code)
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 3 traces captured\n'),
                                                 call('\x1b[1m📦  \x1b[38;2;138;148;138m\x1b[0m.\x1b[1mTrace Session\x1b[0m\x1b[0m'),
                                                 call('\x1b[1m│   └── 🔗️ \x1b[38;2;138;148;138mtest_Trace_Call\x1b[0m.\x1b[1manother_function\x1b[0m\x1b[0m'),
                                                 call('\x1b[1m└────────── 🧩️ \x1b[38;2;138;148;138mtest_Trace_Call\x1b[0m.\x1b[1mdummy_function\x1b[0m\x1b[0m')]

        #handler.stack.add_node(title=DEFAULT_ROOT_NODE_NODE_TITLE)  # add a root node
        handler.trace_capture_start_with  = ['test']
        handler.config.trace_capture_source_code = True
        trace_call.trace_call_print_traces.config.show_caller        = True
        with trace_call:
            another_function()


        view_model                = trace_call.create_view_model()
        trace_capture_source_code = trace_call.trace_call_handler.config.trace_capture_source_code

        with patch('builtins.print') as mock_print:
            trace_call.trace_call_print_traces.print_traces(view_model, trace_capture_source_code)
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 3 traces captured\n'),
                                                 call('🔼️\x1b[1m\x1b[0m'),
                                                 call('➡️📦  \x1b[90m\x1b[38;2;138;148;138m\x1b[0m.\x1b[1mTrace Session\x1b[0m\x1b[0m'),
                                                 call('│   └── 🔼️\x1b[1manother_function()\x1b[0m'),
                                                 call('│   └── ➡️🔗️ \x1b[90mdef another_function():\x1b[0m'),
                                                 call('└────────── 🔼️\x1b[1mdummy_function()\x1b[0m'),
                                                 call('└────────── ➡️🧩️ \x1b[90mdef dummy_function():\x1b[0m')]


        trace_call.trace_call_print_traces.config.show_caller = False
        with patch('builtins.print') as mock_print:
            trace_call.trace_call_print_traces.print_traces(view_model, trace_capture_source_code)
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 3 traces captured\n'),
                                                 call('➡️📦  \x1b[1m\x1b[38;2;138;148;138m\x1b[0m.\x1b[1mTrace Session\x1b[0m\x1b[0m'),
                                                 call('│   └── ➡️🔗️ \x1b[1mdef another_function():\x1b[0m'),
                                                 call('└────────── ➡️🧩️ \x1b[1mdef dummy_function():\x1b[0m')]

        trace_call.trace_call_print_traces.config.capture_locals   = True
        trace_call.trace_call_print_traces.config.print_locals     = True

        with patch('builtins.print') as mock_print:
            with trace_call:
                another_function()
            view_model                = trace_call.create_view_model()
            trace_capture_source_code = trace_call.trace_call_handler.config.trace_capture_source_code
            trace_call.trace_call_print_traces.print_traces(view_model, trace_capture_source_code)
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 3 traces captured\n'),
                                                 call('➡️📦  \x1b[1m\x1b[38;2;138;148;138m\x1b[0m.\x1b[1mTrace Session\x1b[0m\x1b[0m'),
                                                 call('│   └── ➡️🔗️ \x1b[1mdef another_function():\x1b[0m'),
                                                 call('└────────── ➡️🧩️ \x1b[1mdef dummy_function():\x1b[0m'),
                                                 call('│                   🔖 \x1b[1m\x1b[38;2;120;120;120ma\x1b[0m = \x1b[92m12\x1b[0m')]



    def test__print_durations(self):
        trace_call = Trace_Call()
        config = trace_call.config
        config.trace_capture_all = True
        config.capture_duration  = True
        with trace_call:
            def an_fast_function():
                random_number()
                wait_for(0.01)
            def a_bit_slower():
                random_number()
                wait_for(0.03)
            def even_more_slower():
                random_number()
                wait_for(0.06)
            an_fast_function()
            a_bit_slower()
            even_more_slower()

        expected_stats = { 'event_call'     : 21 ,
                           'event_exception': 0  ,
                           'event_line'     : 72 ,
                           'event_return'   : 18 ,
                           'event_unknown'  : 0  }
        if in_github_action():
            expected_stats['event_line'] = 72
        if 'PYCHARM_RUN_COVERAGE' in os.environ:
            expected_stats['event_line'] = 73


        assert trace_call.stats().stats() == expected_stats
        config.print_duration            = False
        config.with_duration_bigger_than = 10 / 1000
        with patch('builtins.print') as mock_print:
            trace_call.print()
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 16 traces captured\n'),
                                                 call('\x1b[1m📦  Trace Session\x1b[0m'),
                                                 call('\x1b[1m│   ├── 🔗️ an_fast_function\x1b[0m                                  test_Trace_Call__Print_Traces'),
                                                 call('\x1b[1m│   │   └── 🧩️ wait\x1b[0m                                          osbot_utils.utils.Misc'),
                                                 call('\x1b[1m│   ├── 🔗️ a_bit_slower\x1b[0m                                      test_Trace_Call__Print_Traces'),
                                                 call('\x1b[1m│   │   └── 🧩️ wait\x1b[0m                                          osbot_utils.utils.Misc'),
                                                 call('\x1b[1m│   └── 🔗️ even_more_slower\x1b[0m                                  test_Trace_Call__Print_Traces'),
                                                 call('\x1b[1m└────────── 🧩️ wait\x1b[0m                                          osbot_utils.utils.Misc')]



        config.with_duration_bigger_than = 20 / 1000
        with patch('builtins.print') as mock_print:
            trace_call.print()
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 16 traces captured\n'),
                                                 call('\x1b[1m📦  Trace Session\x1b[0m'),
                                                 call('\x1b[1m│   ├── 🔗️ a_bit_slower\x1b[0m                                      test_Trace_Call__Print_Traces'),
                                                 call('\x1b[1m│   │   └── 🧩️ wait\x1b[0m                                          osbot_utils.utils.Misc'),
                                                 call('\x1b[1m│   └── 🔗️ even_more_slower\x1b[0m                                  test_Trace_Call__Print_Traces'),
                                                 call('\x1b[1m└────────── 🧩️ wait\x1b[0m                                          osbot_utils.utils.Misc')]

        config.with_duration_bigger_than = 50 / 1000
        with patch('builtins.print') as mock_print:
            trace_call.print()
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 16 traces captured\n'),
                                                 call('\x1b[1m📦  Trace Session\x1b[0m'),
                                                 call('\x1b[1m│   └── 🔗️ even_more_slower\x1b[0m                                  test_Trace_Call__Print_Traces'),
                                                 call('\x1b[1m└────────── 🧩️ wait\x1b[0m                                          osbot_utils.utils.Misc')]

        config.with_duration_bigger_than = 150 / 1000
        with patch('builtins.print') as mock_print:
            trace_call.print()
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 16 traces captured\n')] != []


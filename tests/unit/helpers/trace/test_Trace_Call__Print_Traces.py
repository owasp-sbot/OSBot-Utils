import pytest
from unittest                                           import TestCase
from unittest.mock                                      import patch, call
from osbot_utils.utils.Env                              import in_github_action
from osbot_utils.utils.Misc                             import random_number, wait_for
from osbot_utils.helpers.trace.Trace_Call               import Trace_Call
from osbot_utils.helpers.trace.Trace_Call__Print_Traces import Trace_Call__Print_Traces
from tests.unit.helpers.trace.test_Trace_Call           import another_function


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
            trace_call.trace_call_print_traces.print_traces([])
            expected_calls = [call(),
                              call('--------- CALL TRACER ----------'),
                              call('Here are the 0 traces captured\n')]
            assert mock_print.call_args_list == expected_calls

        handler.config.trace_capture_start_with =['test']

        with trace_call:
            another_function()

        view_model                = trace_call.view_data()
        trace_call.trace_call_print_traces.config.show_parent_info = True
        trace_call.trace_call_print_traces.config.show_method_class = False
        with patch('builtins.print') as mock_print:
            trace_call.trace_call_print_traces.print_traces(view_model)
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 3 traces captured\n'),
                                                 call('\x1b[1m📦  Trace Session\x1b[0m'),
                                                 call('\x1b[1m│   └── 🔗️ another_function\x1b[0m                                           tests.unit.helpers.trace.test_Trace_Call'),
                                                 call('\x1b[1m└────────── 🧩️ dummy_function\x1b[0m                                         tests.unit.helpers.trace.test_Trace_Call')]


        with patch('builtins.print') as mock_print:
            trace_call.trace_call_print_traces.config.show_parent_info  = False
            trace_call.trace_call_print_traces.config.show_method_class = True
            trace_call.trace_call_print_traces.print_traces(view_model)
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


        view_model                = trace_call.view_data()

        # todo fix config.show_caller which is the funcionality that all traces below are using
        # with patch('builtins.print') as mock_print:
        #     trace_call.trace_call_print_traces.print_traces(view_model)
        #     assert mock_print.call_args_list == [call(),
        #                                          call('--------- CALL TRACER ----------'),
        #                                          call('Here are the 3 traces captured\n'),
        #                                          call('🔼️\x1b[1m\x1b[0m'),
        #                                          call('➡️📦  \x1b[90m\x1b[38;2;138;148;138m\x1b[0m.\x1b[1mTrace Session\x1b[0m\x1b[0m'),
        #                                          call('│   └── 🔼️\x1b[1manother_function()\x1b[0m'),
        #                                          call('│   └── ➡️🔗️ \x1b[90mdef another_function():\x1b[0m'),
        #                                          call('└────────── 🔼️\x1b[1mdummy_function()\x1b[0m'),
        #                                          call('└────────── ➡️🧩️ \x1b[90mdef dummy_function():\x1b[0m')]
        #
        #
        # trace_call.trace_call_print_traces.config.show_caller = False
        # with patch('builtins.print') as mock_print:
        #     trace_call.trace_call_print_traces.print_traces(view_model)
        #     assert mock_print.call_args_list == [call(),
        #                                          call('--------- CALL TRACER ----------'),
        #                                          call('Here are the 3 traces captured\n'),
        #                                          call('➡️📦  \x1b[1m\x1b[38;2;138;148;138m\x1b[0m.\x1b[1mTrace Session\x1b[0m\x1b[0m'),
        #                                          call('│   └── ➡️🔗️ \x1b[1mdef another_function():\x1b[0m'),
        #                                          call('└────────── ➡️🧩️ \x1b[1mdef dummy_function():\x1b[0m')]
        #
        # trace_call.trace_call_print_traces.config.capture_locals   = True
        # trace_call.trace_call_print_traces.config.print_locals     = True
        #
        # with patch('builtins.print') as mock_print:
        #     with trace_call:
        #         another_function()
        #     view_model                = trace_call.view_data()
        #     trace_call.trace_call_print_traces.print_traces(view_model)
        #
        #     from osbot_utils.utils.Dev import pprint
        #
        #     assert mock_print.call_args_list == [call(),
        #                                          call('--------- CALL TRACER ----------'),
        #                                          call('Here are the 3 traces captured\n'),
        #                                          call('➡️📦  \x1b[1m\x1b[38;2;138;148;138m\x1b[0m.\x1b[1mTrace Session\x1b[0m\x1b[0m'),
        #                                          call('│   └── ➡️🔗️ \x1b[1mdef another_function():\x1b[0m'),
        #                                          call('└────────── ➡️🧩️ \x1b[1mdef dummy_function():\x1b[0m')]



    @pytest.mark.skip('improve resilience of this test') # namely around the timings of the waits
    def test__print_durations(self):
        if in_github_action():
            pytest.skip("test is failing in GH actions")       # todo: figure out why this is failing in GH actions (it is not the funcionality, the probs is in the timings of of the waits)

        trace_call = Trace_Call()
        config = trace_call.config
        config.trace_capture_all = True
        config.capture_duration  = True
        with trace_call:
            def an_fast_function():
                random_number()
                wait_for(0.0001)
            def a_bit_slower():
                random_number()
                wait_for(0.0005)
            def even_more_slower():
                random_number()
                wait_for(0.0010)
            an_fast_function()
            a_bit_slower()
            even_more_slower()

        config.print_duration            = False
        config.with_duration_bigger_than = 0.1 / 1000
        config.show_parent_info          = True
        config.show_method_class         = False
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



        config.with_duration_bigger_than = 0.4 / 1000
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

        config.with_duration_bigger_than = 1 / 1000
        with patch('builtins.print') as mock_print:
            trace_call.print()
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 16 traces captured\n'),
                                                 call('\x1b[1m📦  Trace Session\x1b[0m'),
                                                 call('\x1b[1m│   └── 🔗️ even_more_slower\x1b[0m                                  test_Trace_Call__Print_Traces'),
                                                 call('\x1b[1m└────────── 🧩️ wait\x1b[0m                                          osbot_utils.utils.Misc')]

        config.with_duration_bigger_than = 10 / 1000
        with patch('builtins.print') as mock_print:
            trace_call.print()
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 16 traces captured\n')] != []


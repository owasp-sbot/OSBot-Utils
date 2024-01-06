from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.utils.trace.Trace_Call import Trace_Call
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
            expected_calls = [call('       🔖 a = \x1b[92m42\x1b[0m')]
            self.print_traces.formatted_local_data(local_data=local_data, formatted_line=formatted_line)
            assert mock_print.call_args_list == expected_calls

        with patch('builtins.print') as mock_print:
            local_data     = {'an_dict': {'a': 42 }}
            formatted_line = ''
            expected_calls = [call("       🔖 an_dict = \x1b[92m{'a': 42}\x1b[0m")]
            self.print_traces.formatted_local_data(local_data=local_data, formatted_line=formatted_line)
            assert mock_print.call_args_list == expected_calls

        with patch('builtins.print') as mock_print:
            local_data     = {'an_method': mock_print}
            formatted_line = ''
            expected_calls = [call('       🔖 an_method = \x1b[94mMagicMock\x1b[0m')]
            self.print_traces.formatted_local_data(local_data=local_data, formatted_line=formatted_line)
            assert mock_print.call_args_list == expected_calls

        with patch('builtins.print') as mock_print:
            self.print_traces.print_max_string_length = 2
            local_data     = {'large_string': 'xx' * self.print_traces.print_max_string_length}
            formatted_line = ''
            expected_calls = [call('       🔖 large_string = \x1b[92mxx...\x1b[0m')]
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

        handler.trace_capture_start_with =['test']
        with trace_call:
            another_function()

        view_model                = trace_call.trace_call_view_model.view_model
        trace_capture_source_code = trace_call.trace_call_handler.trace_capture_source_code

        with patch('builtins.print') as mock_print:
            trace_call.trace_call_print_traces.print_traces(view_model, trace_capture_source_code)
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'         ),
                                                 call('Here are the 3 traces captured\n'         ),
                                                 call('\x1b[1m📦  Trace Session\x1b[0m'          ),
                                                 call('\x1b[1m│   └── 🔗️ another_function\x1b[0m'),
                                                 call('\x1b[1m└────── 🧩️ dummy_function\x1b[0m')]

        with patch('builtins.print') as mock_print:
            trace_call.trace_call_print_traces.print_show_method_parent = True
            trace_call.trace_call_print_traces.print_traces(view_model, trace_capture_source_code)
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 3 traces captured\n'),
                                                 call('\x1b[1m📦  \x1b[38;2;118;138;118m\x1b[0m.\x1b[1mTrace Session\x1b[0m\x1b[0m'),
                                                 call('\x1b[1m│   └── 🔗️ \x1b[38;2;118;138;118mtest_Trace_Call\x1b[0m.\x1b[1manother_function\x1b[0m\x1b[0m'),
                                                 call('\x1b[1m└────── 🧩️ \x1b[38;2;118;138;118mtest_Trace_Call\x1b[0m.\x1b[1mdummy_function\x1b[0m\x1b[0m')]


        handler.trace_capture_start_with  = ['test']
        handler.trace_capture_source_code = True
        trace_call.trace_call_print_traces.print_show_caller        = True
        with trace_call:
            another_function()

        view_model                = trace_call.trace_call_view_model.view_model
        trace_capture_source_code = trace_call.trace_call_handler.trace_capture_source_code

        with patch('builtins.print') as mock_print:
            trace_call.trace_call_print_traces.print_traces(view_model, trace_capture_source_code)
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

        trace_call.trace_call_print_traces.print_show_caller = False
        with patch('builtins.print') as mock_print:
            trace_call.trace_call_print_traces.print_traces(view_model, trace_capture_source_code)
            assert mock_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 5 traces captured\n'),
                                                 call('➡️📦  \x1b[1m\x1b[38;2;118;138;118m\x1b[0m.\x1b[1mTrace Session\x1b[0m\x1b[0m'),
                                                 call('│   ├── ➡️🔗️ \x1b[1m\x1b[38;2;118;138;118mtest_Trace_Call\x1b[0m.\x1b[1manother_function\x1b[0m\x1b[0m'),
                                                 call('│   │   └── ➡️🧩️ \x1b[1m\x1b[38;2;118;138;118mtest_Trace_Call\x1b[0m.\x1b[1mdummy_function\x1b[0m\x1b[0m'),
                                                 call('│   └── ➡️🔗️ \x1b[1mdef another_function():\x1b[0m'),
                                                 call('└────── ➡️🧩️ \x1b[1mdef dummy_function():\x1b[0m')] != []

        trace_call.trace_call_print_traces.print_show_locals = True
        with patch('builtins.print') as mock_print:
            with trace_call:
                another_function()
            view_model                = trace_call.trace_call_view_model.view_model
            trace_capture_source_code = trace_call.trace_call_handler.trace_capture_source_code
            trace_call.trace_call_print_traces.print_traces(view_model, trace_capture_source_code)
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



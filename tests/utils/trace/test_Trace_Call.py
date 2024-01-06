from pprint                                         import pprint
from unittest                                       import TestCase
from unittest.mock                                  import patch, call
from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.utils.Objects import base_classes, obj_info
from osbot_utils.utils.trace.Trace_Call             import Trace_Call, trace_calls
from osbot_utils.utils.trace.Trace_Call__Handler    import Trace_Call__Handler
from osbot_utils.utils.trace.Trace_Call__View_Model import Trace_Call__View_Model


def dummy_function():
    a=12
    pass

def another_function():
    dummy_function()

class test_Trace_Call(TestCase):


    def setUp(self):
        self.trace_call       = Trace_Call()
        self.handler          = self.trace_call.trace_call_handler
        self.trace_view_model = self.trace_call.trace_call_view_model

    def test___default_kwargs(self):
        assert Trace_Call.__default_kwargs__() == dict(print_on_exit           = False ,
                                                       print_locals            = False ,
                                                       capture_source_code     = False ,
                                                       ignore_start_with       = []    ,
                                                       capture_start_with      = []    ,
                                                       print_max_string_length = 100   ,
                                                       title                   = ''    ,
                                                       show_parent_info        = True  ,
                                                       show_caller             = False ,
                                                       show_method_parent      = False ,
                                                       show_source_code_path   = False )

    def test___init__(self):
        assert Kwargs_To_Self in base_classes(Trace_Call)
        assert self.trace_call.__locals__() == {**self.trace_call.__default_kwargs__(),
                                                'prev_trace_function'          : None,
                                                'stack'                        : [{'call_index': 0, 'children': [], 'name': 'Trace Session'}],
                                                'trace_call_handler'           : self.trace_call.trace_call_handler                          ,
                                                'trace_call_view_model'        : self.trace_call.trace_call_view_model                       ,
                                                'trace_call_print_traces'      : self.trace_call.trace_call_print_traces                     }
        assert type(self.trace_call.trace_call_handler   ) is Trace_Call__Handler
        assert type(self.trace_call.trace_call_view_model) is Trace_Call__View_Model


    def test___exit__(self):
        assert self.trace_view_model.view_model == []
        with patch.object(Trace_Call, 'stop') as mock_stop:
            self.trace_call.__exit__(None, None, None)

        mock_stop.assert_called_with()

        assert self.trace_view_model.view_model == [{ 'prefix': '└───', 'tree_branch': '─── ', 'emoji': '📦 ',
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
    def test___enter__exist__(self, builtins_print):
        # Test the initialization and its attributes
        trace_call       = Trace_Call()
        handler          = trace_call.trace_call_handler
        trace_view_model = trace_call.trace_call_view_model
        print_traces     = trace_call.trace_call_print_traces
        print_traces.show_parent_info = True

        assert trace_call.prev_trace_function     is None      , "prev_trace_function should be None initially"
        assert handler.call_index                 == 0         , "call_index should be 0 initially"
        assert trace_view_model.view_model        == []        , "view_model should be empty initially"
        assert print_traces.print_traces_on_exit is False     , "print_traces_on_exit should be False initially"
        assert trace_call.stack                   == [{"name": handler.trace_title, "children": [], "call_index": 0}], "Initial stack state not correct"


        # Test the enter and exit methods
        with Trace_Call() as trace_call:
            trace_call.trace_call_handler.trace_capture_start_with  = ['test_Trace_Call']
            trace_call.trace_call_print_traces.print_show_parent_info = True
            trace_call.trace_call_print_traces.print_traces_on_exit = True                          # To hit the 'print_traces' line in __exit__
            dummy_function()
            another_function()

        view_model = trace_call.trace_call_view_model.view_model
        assert len(view_model) == 4, "Four function calls should be traced"
        assert view_model[0]['method_name'] == handler.trace_title    , "First function in view_model should be 'traces'"
        assert view_model[1]['method_name'] == 'dummy_function'          , "2nd function in view_model should be 'dummy_function'"
        assert view_model[2]['method_name'] == 'another_function'        , "3rd function in view_model should be 'another_function'"
        assert view_model[3]['method_name'] == 'dummy_function'          , "4th function in view_model should be 'dummy_function'"

        assert builtins_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 4 traces captured\n'),
                                                 call('\x1b[1m📦  Trace Session\x1b[0m'),
                                                 call('\x1b[1m│   ├── 🧩️ dummy_function\x1b[0m                                    test_Trace_Call'),
                                                 call('\x1b[1m│   └── 🔗️ another_function\x1b[0m                                  test_Trace_Call'),
                                                 call('\x1b[1m└────── 🧩️ dummy_function\x1b[0m                                    test_Trace_Call')] != []
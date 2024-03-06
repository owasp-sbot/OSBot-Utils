from pprint                                         import pprint
from unittest                                       import TestCase
from unittest.mock                                  import patch, call

from osbot_utils.testing.Patch_Print                    import Patch_Print
from osbot_utils.utils.Lists import tuple_to_list
from osbot_utils.utils.Python_Logger                    import Python_Logger
from osbot_utils.utils.Misc                             import list_set
from osbot_utils.testing.Temp_File                      import Temp_File
from osbot_utils.base_classes.Kwargs_To_Self            import Kwargs_To_Self
from osbot_utils.utils.Objects                          import base_classes
from osbot_utils.helpers.trace.Trace_Call               import Trace_Call, trace_calls
from osbot_utils.helpers.trace.Trace_Call__Config       import Trace_Call__Config
from osbot_utils.helpers.trace.Trace_Call__Handler      import Trace_Call__Handler
from osbot_utils.helpers.trace.Trace_Call__View_Model   import Trace_Call__View_Model


def dummy_function():
    a=12
    pass

def another_function():
    dummy_function()

class test_Trace_Call(TestCase):


    def setUp(self):
        self.trace_call       = Trace_Call()
        self.config           = self.trace_call.config
        self.handler          = self.trace_call.trace_call_handler
        self.trace_view_model = self.trace_call.trace_call_view_model

    def test___default_kwargs(self):
        default_kwargs = Trace_Call().__default_kwargs__()
        assert list_set(default_kwargs) == ['config', 'prev_trace_function', 'started']
        assert type(default_kwargs.get('config')) is Trace_Call__Config

    def test___init__(self):
        assert Kwargs_To_Self in base_classes(Trace_Call)

        assert self.trace_call.__locals__() == { 'config'                 : self.trace_call.config                 ,
                                                 'prev_trace_function'    : None                                   ,
                                                 'stack'                  : []                                     ,
                                                 'started'                : False                                  ,
                                                 'trace_call_handler'     : self.trace_call.trace_call_handler     ,
                                                 'trace_call_view_model'  : self.trace_call.trace_call_view_model  ,
                                                 'trace_call_print_traces': self.trace_call.trace_call_print_traces}
        assert type(self.trace_call.trace_call_handler   ) is Trace_Call__Handler
        assert type(self.trace_call.trace_call_view_model) is Trace_Call__View_Model


    def test___exit__(self):
        assert self.trace_view_model.view_model == []
        with patch.object(Trace_Call, 'stop') as mock_stop:
            self.trace_call.__exit__(None, None, None)

        mock_stop.assert_called_with()
        self.trace_call.view_data()         # this is populated by the self.trace_view_model.view_model object
        assert self.trace_view_model.view_model == [{ 'duration': 0.0, 'extra_data': {}, 'lines': [],'prefix': '', 'tree_branch': '─── ', 'emoji': '📦 ',
                                                      'method_name': '', 'method_parent': '',
                                                      'parent_info': '', 'locals': {}, 'source_code': '',
                                                      'source_code_caller': '', 'source_code_location': ''}]


    def test_capture_all(self):
        assert self.config.trace_capture_all is False
        self.trace_call.capture_all()
        assert self.config.trace_capture_all is True

    @patch('builtins.print')
    def test_decorator__trace_calls(self, builtins_print):

            @trace_calls(include=['test', 'pprint'], print_traces=True)
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
                                                     call('\x1b[1m└────────────────────── 🧩️ format\x1b[0m')] != []


    def test_print_lines(self):
        with Patch_Print() as _:
            self.trace_call.print_lines()

        assert _.call_args_list() == [call(),
                                      call('--------- CALL TRACER (Lines)----------'),
                                      call('Here are the 0 lines captured\n'),
                                      call('┌─────┬──────┬────────┬────┬──┬───────┐   '),
                                      call('│ #   │ Line │ Source code  │ Method Class and Name │ Self object │ Depth │   '),
                                      call('├─────┼──────┼────────┼────┼──┼───────┤   '),
                                      call('└─────┴──────┴────────┴────┴──┴───────┘')] != [call()]
    def test_stats(self):
        assert self.trace_call.stats() == {'calls': 0, 'calls_skipped': 0, 'exceptions': 0, 'lines': 0, 'returns': 0, 'unknowns': 0}

    def test_stats_data(self):
        assert self.trace_call.stats_data() == []

    def test_stop(self):
        prev_trace_function = None
        self.trace_call.started = True
        with patch('sys.settrace') as mock_systrace:
            self.trace_call.stop()
            assert self.trace_call.prev_trace_function is prev_trace_function
            mock_systrace.assert_called_with(prev_trace_function)
        prev_trace_function = '___prev_trace_function___'
        self.trace_call.started = True
        with patch('sys.settrace') as mock_systrace:
            self.trace_call.prev_trace_function = prev_trace_function
            self.trace_call.stop()
            assert self.trace_call.prev_trace_function == prev_trace_function
            mock_systrace.assert_called_with(prev_trace_function)


    @patch('builtins.print')
    def test___enter__exit__(self, builtins_print):
        trace_call       = Trace_Call()
        handler          = trace_call.trace_call_handler
        trace_view_model = trace_call.trace_call_view_model
        print_traces     = trace_call.trace_call_print_traces

        print_traces.config.show_parent_info = True

        assert trace_call.prev_trace_function     is None      , "prev_trace_function should be None initially"
        assert handler.stack.call_index           == 0         , "call_index should be 0 initially"
        assert trace_view_model.view_model        == []        , "view_model should be empty initially"
        assert print_traces.config.print_traces_on_exit is False     , "print_traces_on_exit should be False initially"

        assert trace_call.stack == []

        # Test the enter and exit methods
        with Trace_Call() as trace_call:
            trace_call.trace_call_handler.config.trace_capture_start_with  = ['test_Trace_Call']
            trace_call.trace_call_print_traces.config.show_parent_info = True
            trace_call.trace_call_print_traces.config.show_method_class = False
            trace_call.trace_call_print_traces.config.print_traces_on_exit = True                          # To hit the 'print_traces' line in __exit__
            dummy_function()
            another_function()

        view_model = trace_call.trace_call_view_model.view_model
        assert len(view_model) == 4, "Four function calls should be traced"

        assert view_model[0]['method_name'] == handler.config.title      , "First function in view_model should be 'traces'"
        assert view_model[1]['method_name'] == 'dummy_function'          , "2nd function in view_model should be 'dummy_function'"
        assert view_model[2]['method_name'] == 'another_function'        , "3rd function in view_model should be 'another_function'"
        assert view_model[3]['method_name'] == 'dummy_function'          , "4th function in view_model should be 'dummy_function'"


        assert builtins_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 4 traces captured\n'),
                                                 call('\x1b[1m📦  Trace Session\x1b[0m'),
                                                 call('\x1b[1m│   ├── 🧩️ dummy_function\x1b[0m                                    test_Trace_Call'),
                                                 call('\x1b[1m│   └── 🔗️ another_function\x1b[0m                                  test_Trace_Call'),
                                                 call('\x1b[1m└────────── 🧩️ dummy_function\x1b[0m                                test_Trace_Call')] != []


    def test__check_that_stats_catches_exception_stats(self):
        try:
            with Trace_Call() as trace_call:
                def throw_an_exception():
                    raise Exception('test_1')
                try:
                    throw_an_exception()
                except Exception as error:
                    assert error.args[0] == 'test_1'
                raise Exception('test_2')
        except Exception as error:
            assert error.args[0] == 'test_2'

    def test__config__capture_frame_stats(self):
        self.config.capture_frame_stats    = True
        self.config.show_parent_info       = False
        self.config.show_method_class      = False
        self.config.trace_capture_contains = ['random_filename', 'file_extension_fix']
        with self.trace_call:
            with Temp_File() as temp_file:
                with Temp_File() as temp_file:
                    def an_temp_file():
                        return temp_file.tmp_file

                    an_temp_file()

        with patch('builtins.print') as builtins_print:
            view_model = self.trace_view_model.create(self.trace_call.stack)
            self.trace_call.trace_call_print_traces.print_traces(view_model)

        assert builtins_print.call_args_list == [call(),
                                                 call('--------- CALL TRACER ----------'),
                                                 call('Here are the 5 traces captured\n'),
                                                 call('\x1b[1m📦  Trace Session\x1b[0m'),
                                                 call('\x1b[1m│   ├── 🔗️ random_filename\x1b[0m'),
                                                 call('\x1b[1m│   │   └── 🧩️ file_extension_fix\x1b[0m'),
                                                 call('\x1b[1m│   └── 🔗️ random_filename\x1b[0m'),
                                                 call('\x1b[1m└────────── 🧩️ file_extension_fix\x1b[0m')] != []

        assert list_set(self.handler.stats.frames_stats()) == ['codecs', 'genericpath', 'os',
                                                               'osbot_utils', 'posixpath', 'random', 'shutil',
                                                               'tempfile', 'test_Trace_Call', 'typing']

        assert self.handler.stats.frames_stats().get('osbot_utils') == { 'base_classes': {'Kwargs_To_Self': {'__setattr__': 1}},
                                                                         'helpers': {'trace': {'Trace_Call': {'__exit__': 1, 'on_exit': 1, 'stop': 1}}},
                                                                         'testing': {'Temp_File': {'__enter__': 2, '__exit__': 2, '__init__': 2}},
                                                                         'utils': {'Files': {'delete': 2,
                                                                                             'exists': 4,
                                                                                             'file_extension_fix': 2,
                                                                                             'folder_delete_all': 2,
                                                                                             'folder_exists': 4,
                                                                                             'is_file': 4,
                                                                                             'is_folder': 4,
                                                                                             'path_combine': 2,
                                                                                             'temp_folder': 2,
                                                                                             'write': 2},
                                                                                   'Misc': {'random_filename': 2},
                                                                                   'Objects': { 'are_types_compatible_for_assigment'              : 1,
                                                                                                'obj_attribute_annotation'                        : 1,
                                                                                                'value_type_matches_obj_annotation_for_attr'      : 1,
                                                                                                'value_type_matches_obj_annotation_for_union_attr':1 }}}

    def test__config_print_traces_on_exit(self):
        self.config.print_traces_on_exit = True
        with Patch_Print() as _:
            self.trace_call.on_exit()
        assert _.call_args_list() == [call(),
                                      call('--------- CALL TRACER ----------'),
                                      call('Here are the 1 traces captured\n'),
                                      call('\x1b[1m─── 📦  \x1b[38;2;138;148;138m\x1b[0m.\x1b[1m\x1b[0m\x1b[0m')]
        self.config.print_traces_on_exit = False
        self.config.print_lines_on_exit   = True
        with Patch_Print() as _:
            self.trace_call.on_exit()
        assert _.call_args_list() == [call(),
                                      call('--------- CALL TRACER (Lines)----------'),
                                      call('Here are the 0 lines captured\n'),
                                      call('┌─────┬──────┬────────┬────┬──┬───────┐   '),
                                      call('│ #   │ Line │ Source code  │ Method Class and Name │ Self object │ Depth │   '),
                                      call('├─────┼──────┼────────┼────┼──┼───────┤   '),
                                      call('└─────┴──────┴────────┴────┴──┴───────┘')]

    def test__trace_up_to_a_level(self):
        with self.config as _:
            _.all()
            _.up_to_depth(2)
            _.trace_show_internals = True
            _.show_method_class = False

        expected_calls = [ ''                                                ,
                           '--------- CALL TRACER ----------'                ,
                           'Here are the 8 traces captured\n'                ,
                           '\x1b[1m📦  Trace Session\x1b[0m'                 ,
                           '\x1b[1m│   ├── 🧩️ __setattr__\x1b[0m'            ,
                           '\x1b[1m│   ├── 🔗️ Python_Logger.__init__\x1b[0m' ,
                           '\x1b[1m│   │   ├── 🧩️ set_logger_name\x1b[0m'    ,
                           '\x1b[1m│   │   ├── 🧩️ set_config\x1b[0m'         ,
                           '\x1b[1m│   │   └── 🧩️ setup\x1b[0m'              ,
                           '\x1b[1m│   └── 🔗️ add_memory_logger\x1b[0m'      ,
                           '\x1b[1m└────────── 🧩️ add_handler_memory\x1b[0m' ]
        #expected_calls = expected_calls
        with Patch_Print(print_calls=False, enabled=True) as _:
            with self.trace_call:
                logger = Python_Logger()
                logger.add_memory_logger()
        assert _.calls() == expected_calls

    def test_regression__previous_set_variables_can_be_set_to_none(self):
        with Trace_Call__Config() as _:                             # create a new clean object
            assert _.trace_capture_start_with == []                 # confirm variable is set
            with self.assertRaises(Exception) as context:           # FIXED: after the fix
                _.trace_capture_start_with = None                   # FIXED: this now raises an exception
            assert str(context.exception) == ("Can't set None, to a variable that is already set. Invalid type for "
                                              "attribute 'trace_capture_start_with'. "
                                              "Expected '<class 'list'>' but got '<class 'NoneType'>'")
            # _.trace_capture_start_with        = None               # BUG: this should not be allowed
            # assert _.trace_capture_start_with is None              # BUG: this var should not have changed

        class An_Class(Kwargs_To_Self):                              # create a test class to confirm behaviour
            none_allowed = None                                      # we can have a None here (since the type is not defined)
            an_list      : list                                      # when a list is defined, the default value will be assigned to it (in this case [] )

        an_class = An_Class()                                        # create an instance of the test class
        assert an_class.none_allowed is None                         # conform that the none_allowed var exists and it is None
        assert an_class.an_list      == []                           # confirm that the an_list var exists and it is an empty list
        with self.assertRaises(Exception) as context:                # FIXED: after the fix
            an_class.an_list = None                                  # FIXED: this raises an exception
        assert str(context.exception) == ("Can't set None, to a variable that is already set. Invalid type for "
                                           "attribute 'an_list'. Expected '<class 'list'>' but got '<class 'NoneType'>'")
        #an_class.an_list = None                                     # BUG: this should not be allowed (since we know that an_list should be a list)
        #assert an_class.an_list      is None                        # BUG: this var should not have changed

    def test_bug__it_is_possible_to_change_types_of_objects_already_set(self):
        class An_Class(): pass

        an_class = An_Class()                                       # create an instance of the test class
        an_class.new_var = None                                     # we can create new vars (since we have not 'locked' the class)
        assert an_class.new_var is None                             # confirm it exists and it is None
        an_class.new_var = "abc"                                    # confirm that we can assign the variable to a string
        assert type(an_class.new_var) is str                        # confirm that it is a string
        an_class.new_var = 42                                       # BUG: confirm that we can change the type (which we really shouldn't)
        assert type(an_class.new_var) is int                        # BUG: confirm that the type changed (which it shouldn't)


    def test__regression__trace_capture_start_with__can_be_set_to__none(self):
        config = Trace_Call__Config()                       # create a clean copy of Trace_Call__Config
        with config as _:                                   # use the context support to make the code cleanner below
            assert _.trace_capture_start_with == []         # this is what we expect by default
            #_.enable_type_safety()
            #_.trace_capture_start_with        = None        # FIXED this now doesn't do anything   BUG: this should not be possible
            assert _.trace_capture_start_with == []         # FIXED: value was not overwritten     BUG: if we allow this to happen, other parts of the code will break

        config = Trace_Call__Config()                       # create a new clean object
        with config as _:
            assert _.trace_capture_start_with == []         # confirm value
            kwargs = {'trace_capture_start_with': ['a']}    # create an object that can be used on update_from_kwargs
            _.update_from_kwargs(**kwargs)                  # this is the other location of the bug (in fact it is where the bug was discovered)
            assert _.trace_capture_start_with == ['a']      # so far so good, since the list was correctly populated

            kwargs = {'trace_capture_start_with': None}     # this is where the bug will be created
            _.update_from_kwargs(**kwargs)                  # FIXED: works now  BUG: this should not have worked
            assert _.trace_capture_start_with == ['a']      # FIXED: was None   BUG: this should not have been set to None (since it is not a list)


    def test__regression__trace_calls__decorator_fails_when_trace_capture_start_with_is_set_to_none(self):
        #with self.assertRaises(Exception) as context:                          # FIXED: this is the exception that we expect to be raised
            @trace_calls()                                                      # FIXED: BUG this is where the exception will occur
            def method_a():                                                     # FIXED: i.e. on the setup of the call tracer for method_a()
                pass                                                            # we will never get here (we got here and all good)

            method_a()                                                          # trigger the execution of the trace_calls decorator

        #assert str(context.exception) == "Invalid type for attribute 'with_duration_bigger_than'. Expected '<class 'float'>' but got '<class 'int'>'"    # confirm correct exception was raised



# class test_ Pickle(TestCase):
#
#     def test_process_data(self):
#         trace_call              = Trace_Call()
#         trace_call__view_model  = Trace_Call__View_Model()
#         trace_call_print_traces = Trace_Call__Print_Traces()
#         call_handler            = trace_call.trace_call_handler
#
#         call_handler                 .config.capture_locals            = False
#         trace_call.trace_call_handler.config.trace_capture_start_with  = ['*']
#         #trace_call.trace_call_handler.config.trace_capture_contains     = ['print']
#         trace_call_print_traces      .config.show_parent_info          = True
#         #trace_call_print_traces      .config.print_locals              = False
#         import requests
#         trace_call.config.capture_frame_stats = True
#         with trace_call:
#             with Temp_File() as temp_file:
#                 def an_temp_file():
#                     return temp_file.tmp_file
#                 an_temp_file()
#
#
#
#         stack       = trace_call.stack
#         #pprint(stack)
#         view_model  = trace_call__view_model.create(stack)
#         #trace_call_print_traces.print_traces(view_model)
#
#         #pprint(call_handler.stats.raw_call_stats)
#         #pprint(call_handler.stats.frames_stats())
from unittest import TestCase

from osbot_utils.utils.Objects import default_value
from osbot_utils.utils.trace.Trace_Call__Config import Trace_Call__Config


class test_Trace_Call__Config(TestCase):

    def setUp(self):
        self.trace_call_config = Trace_Call__Config()

    def test__init__(self):
        assert type(default_value(Trace_Call__Config)) is Trace_Call__Config

    def test__kwargs__(self):
        expected_data = { 'capture_duration'         : False ,
                          'capture_extra_data'       : False ,
                          'capture_frame'            : True  ,
                          'capture_frame_stats'      : False ,
                          'capture_locals'           : True  ,
                          'capture_start_with'       : []    ,
                          'ignore_start_with'        : []    ,
                          'print_locals'             : False ,
                          'print_max_string_length'  : 100   ,
                          'print_lines_on_exit'      : False ,
                          'print_traces_on_exit'     : False ,
                          'print_duration'           : False,
                          'show_caller'              : False ,
                          'show_method_class'        : False ,
                          'show_parent_info'         : True  ,
                          'show_source_code_path'    : False ,
                          'title'                    : ''    ,
                          'trace_capture_all'        : False ,
                          'trace_capture_lines'      : False ,
                          'trace_capture_source_code': False ,
                          'trace_capture_start_with' : []    ,
                          'trace_capture_contains'   : []    ,
                          'trace_ignore_start_with'  : []    ,
                          'trace_show_internals'     : False ,
                          'with_duration_bigger_than': False }
        assert Trace_Call__Config.__cls_kwargs__    () == expected_data
        assert Trace_Call__Config.__default_kwargs__() == expected_data

        with self.trace_call_config as _:
            assert _.__cls_kwargs__     () == expected_data
            assert _.__default_kwargs__ () == expected_data
            assert _.__kwargs__         () == expected_data
            assert _.__locals__         () == expected_data
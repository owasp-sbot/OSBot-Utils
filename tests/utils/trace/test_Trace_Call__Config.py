from unittest import TestCase

from osbot_utils.utils.Objects import default_value
from osbot_utils.utils.trace.Trace_Call__Config import Trace_Call__Config


class test_Trace_Call__Config(TestCase):

    def setUp(self):
        self.trace_call_config = Trace_Call__Config()

    def test__init__(self):
        assert type(default_value(Trace_Call__Config)) is Trace_Call__Config

    def test__kwargs__(self):
        expected_data = { 'capture_frame'            : True  ,
                          'capture_locals'           : True  ,
                          'capture_source_code'      : False ,
                          'capture_start_with'       : []    ,
                          'ignore_start_with'        : []    ,
                          'print_locals'             : False ,
                          'print_max_string_length'  : 100   ,
                          'print_on_exit'            : False ,
                          'process_data'             : True  ,
                          'show_caller'              : False ,
                          'show_method_parent'       : False ,
                          'show_parent_info'         : True  ,
                          'show_source_code_path'    : False ,
                          'title'                    : ''    ,
                          'trace_capture_all'        : False ,
                          'trace_capture_source_code': False ,
                          'trace_capture_start_with' : []    ,
                          'trace_ignore_internals'   : True  ,
                          'trace_ignore_start_with'  : []    }
        assert Trace_Call__Config.__cls_kwargs__    () == expected_data
        assert Trace_Call__Config.__default_kwargs__() == expected_data

        with self.trace_call_config as _:
            assert _.__cls_kwargs__     () == expected_data
            assert _.__default_kwargs__ () == expected_data
            assert _.__kwargs__         () == expected_data
            assert _.__locals__         () == expected_data
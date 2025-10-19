from unittest                                     import TestCase
from unittest.mock                                import patch, call
from osbot_utils.utils.Objects                    import default_value
from osbot_utils.helpers.trace.Trace_Call__Config import Trace_Call__Config, PRINT_PADDING__DURATION


class test_Trace_Call__Config(TestCase):

    def setUp(self):
        self.trace_call_config = Trace_Call__Config()

    def test__init__(self):
        assert type(default_value(Trace_Call__Config)) is Trace_Call__Config

    def test__kwargs__(self):
        expected_data = { 'capture_duration'           : False ,
                          'capture_extra_data'         : False ,
                          'capture_frame'              : True  ,
                          'capture_frame_stats'        : False ,
                          'capture_locals'             : False ,
                          'deep_copy_locals'           : False ,
                          'ignore_start_with'          : []    ,
                          'print_locals'               : False ,
                          'print_max_string_length'    : 100   ,
                          'print_padding_duration'     : 100   ,
                          'print_padding_parent_info'  : 60    ,
                          'print_lines_on_exit'        : False ,
                          'print_traces_on_exit'       : False ,
                          'print_duration'             : False ,
                          'show_caller'                : False ,
                          'show_method_class'          : True  ,      # recently changed
                          'show_parent_info'           : False ,      # recently changed
                          'show_source_code_path'      : False ,
                          'title'                      : ''    ,
                          'trace_capture_all'          : False ,
                          'trace_capture_lines'        : False ,
                          'trace_capture_source_code'  : False ,
                          'trace_capture_start_with'   : []    ,
                          'trace_capture_contains'     : []    ,
                          'trace_enabled'              : True  ,
                          'trace_ignore_contains'      : []    ,
                          'trace_ignore_start_with'    : []    ,
                          'trace_show_internals'       : False ,
                          'trace_up_to_depth'          : 0     ,
                          'with_duration_bigger_than'  : 0.0   }
        assert Trace_Call__Config.__cls_kwargs__      () == expected_data
        assert Trace_Call__Config().__default_kwargs__() == expected_data

        with self.trace_call_config as _:
            assert _.__cls_kwargs__     () == expected_data
            assert _.__default_kwargs__ () == expected_data
            assert _.__kwargs__         () == expected_data
            assert _.__locals__         () == expected_data

    def test_all(self):
        with self.trace_call_config as _:
            _.all(up_to_depth=5, print_traces=True)
            assert _.trace_capture_all      is True
            assert _.print_traces_on_exit   is True
            assert _.trace_up_to_depth      == 5

    def test_capture(self):
        with self.trace_call_config as _:
            assert _.trace_capture_start_with == []
            assert _.trace_capture_contains   == []
            assert _.ignore_start_with        == []
            assert _.print_traces_on_exit     is False

            _.print_traces_on_exit = False
            _.capture(starts_with=['a,b,c'], contains=['d,e,f'], ignore=['g,h,i'])

            assert _.trace_capture_start_with == ['a,b,c']
            assert _.trace_capture_contains   == ['d,e,f']
            assert _.ignore_start_with        == ['g,h,i']
            assert _.print_traces_on_exit     is True

            _.capture(starts_with='A', contains='B', ignore="C")

            assert _.trace_capture_start_with == ['A']
            assert _.trace_capture_contains   == ['B']
            assert _.ignore_start_with        == ['C']
            assert _.print_traces_on_exit     is True

    def test_duration(self):
        with self.subTest("Initial state"):
            config = self.trace_call_config
            assert config.capture_duration is False
            assert config.print_duration is False
            assert config.print_padding_duration == PRINT_PADDING__DURATION
            assert config.with_duration_bigger_than == 0

        with self.subTest("After setting duration"):
            config.duration(bigger_than=10, padding=20)
            assert config.capture_duration is True
            assert config.print_duration is True
            assert config.print_padding_duration == 20
            assert config.with_duration_bigger_than == 10

    def test_locals(self):
        config = self.trace_call_config
        assert config.capture_locals is False
        assert config.print_locals is False

        config.locals()
        assert config.capture_locals is True
        assert config.print_locals is True

    def test_lines(self):
        config = self.trace_call_config
        assert config.trace_capture_lines is False
        assert config.print_traces_on_exit is False
        assert config.print_lines_on_exit is False

        config.lines(print_traces=True, print_lines=True)
        assert config.trace_capture_lines is True
        assert config.print_traces_on_exit is True
        assert config.print_lines_on_exit is True

    def test_print_config(self):
        with patch('osbot_utils.helpers.trace.Trace_Call__Config.pprint') as mock_pprint:
            self.trace_call_config.print_config()
        mock_pprint.assert_called_once()
        assert mock_pprint.call_args_list == [call(self.trace_call_config.__locals__())]

    def test_up_to_depth(self):
        config = self.trace_call_config
        assert config.trace_up_to_depth == 0

        config.up_to_depth(5)
        assert config.trace_up_to_depth == 5

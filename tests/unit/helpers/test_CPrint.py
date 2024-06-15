from unittest import TestCase
from unittest.mock import patch, call
from osbot_utils.utils.Misc import list_set

from osbot_utils.helpers.CPrint import CPrint, CFormat_Colors
from osbot_utils.testing.Patch_Print import Patch_Print


class test_CPrint(TestCase):

    def setUp(self):
        self.cprint = CPrint()
        self.result = None


    def test__init__(self):

        expected_colors = sorted(['black', 'blink', 'blue', 'bold', 'bright_black', 'bright_blue', 'bright_cyan',
                                  'bright_green', 'bright_magenta', 'bright_red', 'bright_white', 'bright_yellow',
                                  'cyan', 'dark_red', 'dark_grey', 'double_underline', 'encircled', 'faint', 'framed', 'green',
                                  'grey', 'inverse', 'italic', 'magenta', 'none', 'overlined', 'red', 'strikethrough',
                                  'underline', 'white', 'yellow'])
        colors_in_colors = sorted([name for name in CFormat_Colors.__dict__ if not name.startswith('__')])
        assert colors_in_colors == expected_colors
        assert list_set(self.cprint.__locals__()) == sorted(['apply_colors'    ,
                                                             'auto_bold'       ,
                                                             'auto_new_line'   ,
                                                             'auto_print'      ,
                                                             'clear_on_print'  ,
                                                             'current_line'    ,
                                                             'lines'           ,
                                                             *expected_colors  ])
        assert self.cprint.auto_new_line  is True
        assert self.cprint.auto_print     is True
        assert self.cprint.clear_on_print is True
        assert self.cprint.current_line   == ''
        assert self.cprint.lines          == []

    def test_print(self):
        with Patch_Print(enabled=True) as patched_print:
            with self.cprint as _:
                _.red('this is in red')
                _.green('now green')
                _.new_line()
                _.blue('asd')
                _.print()

        assert patched_print.call_args_list() == [call('\x1b[31mthis is in red\x1b[0m'),
                                                  call('\x1b[32mnow green\x1b[0m'),
                                                  call(''),
                                                  call('\x1b[34masd\x1b[0m')]
        assert _.lines == []

    def test__kwargs__auto_new_line(self):
        with Patch_Print(enabled=True) as patched_print:
            with self.cprint as _:
                _.auto_new_line = False
                _.auto_print    = False
                _.red('this is in red')
                _.green('now green')
                _.new_line()
                _.blue('asd')
                assert _.lines == ['\x1b[31mthis is in red\x1b[0m\x1b[32mnow green\x1b[0m', '']
                _.print()
                assert _.lines == []

        assert patched_print.call_args_list() == [call('\x1b[31mthis is in red\x1b[0m\x1b[32mnow green\x1b[0m'),
                                                  call(''),
                                                  call('\x1b[34masd\x1b[0m')]

    def test__kwargs__auto_print(self):
        with Patch_Print(enabled=True) as patched_print:
            with self.cprint as _:
                _.auto_print = True
                assert patched_print.call_args_list() == []
                assert _.lines == []
                _.red('this is in red')
                assert patched_print.call_args_list() == [call('\x1b[31mthis is in red\x1b[0m')]
                assert _.lines == []
                _.green('now green')
                assert patched_print.call_args_list() == [call('\x1b[31mthis is in red\x1b[0m'), call('\x1b[32mnow green\x1b[0m')]
                assert _.lines == []
                _.new_line()
                assert patched_print.call_args_list() == [call('\x1b[31mthis is in red\x1b[0m'), call('\x1b[32mnow green\x1b[0m'), call('')]
                assert _.lines == []
                _.blue('asd')
                assert patched_print.call_args_list() == [call('\x1b[31mthis is in red\x1b[0m'), call('\x1b[32mnow green\x1b[0m'), call(''), call('\x1b[34masd\x1b[0m')]
                assert _.lines == []

    def test__kwargs__clear_on_print(self):
        with Patch_Print(enabled=True) as patched_print:
            with self.cprint as _:
                _.auto_print     = False
                _.clear_on_print = False
                _.red  ('this is in red')
                _.green('this is in green')
                _.print()

        assert patched_print.call_args_list() == [call(f'\x1b[{CFormat_Colors.red  }mthis is in red\x1b[0m'),
                                                  call(f'\x1b[{CFormat_Colors.green}mthis is in green\x1b[0m')]

        assert _.lines == ['\x1b[31mthis is in red\x1b[0m',
                           '\x1b[32mthis is in green\x1b[0m']

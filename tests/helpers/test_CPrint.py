from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.helpers.CPrint import CPrint
from osbot_utils.testing.Patch_Print import Patch_Print


class test_CPrint(TestCase):

    def setUp(self):
        self.cprint = CPrint()
        self.result = None

    def test_print(self):
        print()



        with Patch_Print() as patched_print:
            with self.cprint as _:
                _.red('this is in red')
                _.green('now green')
                _.line()
                _.blue('asd')
        assert patched_print.call_args_list() == [call('\x1b[31mthis is in red\x1b[0m', end=''),
                                                  call('\x1b[32mnow green\x1b[0m', end=''),
                                                  call()                                    ,
                                                  call('\x1b[34masd\x1b[0m', end='')]



    @patch('builtins.print')
    def test_print_red(self, mock_print):
        CPrint.print(Color.RED, "Test in red")
        mock_print.assert_called_with('\x1b[31m', 'Test in red', '\x1b[0m')

    @patch('builtins.print')
    def test_print_green(self, mock_print):
        CPrint.print(Color.GREEN, "Test in green")
        mock_print.assert_called_with('\x1b[32m', 'Test in green', '\x1b[0m')

    @patch('builtins.print')
    def test_print_blue_with_multiple_args(self, mock_print):
        CPrint.print(Color.BLUE, "Test", "in", "blue")
        mock_print.assert_called_with('\x1b[34m', 'Test', 'in', 'blue', '\x1b[0m')


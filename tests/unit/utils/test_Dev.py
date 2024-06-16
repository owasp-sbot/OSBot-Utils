from unittest               import TestCase
from unittest.mock          import patch, call

import pytest

from osbot_utils.testing.Stdout import Stdout
from osbot_utils.utils.Dev  import Dev

class Test_Dev(TestCase):

    def test_jformat(self):
        assert Dev.jformat({'answer': 42}) == '{\n    "answer": 42\n}'

    @patch('builtins.print')
    def test_jprint(self, builtins_print):
        assert Dev.jprint({'answer': 42}) == {'answer': 42 }
        assert builtins_print.call_count == 2
        builtins_print.assert_has_calls([call(), call('{\n    "answer": 42\n}')])

    def test_pformat(self):
        assert Dev.pformat({'answer': 42}) == "{'answer': 42}"

    @patch('builtins.print')
    def test_pprint__confirm_call_to_builtins_print(self, builtins_print):
        with Stdout() as stdout:
            Dev.pprint('aaa')                                       # first call
            Dev.pprint('aaa',123)                                   # 2nd call
            assert builtins_print.call_count == 2                   # confirm two calls where made
            builtins_print.assert_called_with()                     # confirm last call was made with no params
            builtins_print.assert_has_calls([call(),call()])        # confirm values of two calls
        assert stdout.value() == "'aaa'\n'aaa'\n123\n"

    @patch('pprint.pprint')
    def test__a_pprint__confirm_call_to_pprint_pprint(self, pprint_pprint):
        with Stdout() as stdout:
            assert Dev.pprint('1st'    )    == '1st'
            assert Dev.pprint('2nd',123)    == ('2nd',123)
            assert pprint_pprint.call_count == 3
            pprint_pprint.assert_has_calls([call('1st', indent=2), call('2nd', indent=2),call(123, indent=2)])
        assert stdout.value() == '\n\n'


    @patch('builtins.print')
    def test_nprint(self, builtins_print):
        assert Dev.nprint({'answer': 42}) == {'answer': 42 }
        assert builtins_print.call_count == 2
        builtins_print.assert_has_calls([call(), call({'answer': 42})])



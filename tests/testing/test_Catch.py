from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.testing.Catch import Catch


class test_Catch(TestCase):

    @patch('builtins.print')
    def test_Catch(self, builtins_print):

        expected_error = "Catch: <class 'Exception'> : new exception"
        with Catch(log_exception=True, expected_error=expected_error) as catch:
            raise Exception('new exception')
        assert builtins_print.call_count == 5

        assert str(catch) == expected_error
        catch.assert_error_is(expected_error)

        calls = builtins_print.mock_calls
        assert calls[0] == call('')
        assert calls[1] == call('********* Catch ***********')
        assert calls[2] == call(Exception)
        assert calls[3] == call('')
        assert str(calls[4]) == str(call(Exception('new exception')))


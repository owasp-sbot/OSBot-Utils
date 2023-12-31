from pprint import pprint
from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.utils.Misc import wait, time_delta_to_str

from osbot_utils.testing.Catch import Catch
from osbot_utils.testing.Duration import Duration


class test_Duration(TestCase):

    @patch('builtins.print')
    def test_Duration(self, builtins_print):
        with Duration() as duration:
            wait(0.2)
        duration_srt     = time_delta_to_str(duration.duration)
        expected_output = f'\nDuration: {duration_srt}'
        assert builtins_print.mock_calls == [call(expected_output)]

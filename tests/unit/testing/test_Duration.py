from unittest                               import TestCase
from unittest.mock                          import patch, call
from osbot_utils.helpers.duration.Duration  import Duration
from osbot_utils.utils.Misc                 import wait, time_delta_to_str



class test_Duration(TestCase):

    @patch('builtins.print')
    def test_Duration(self, builtins_print):
        with Duration() as duration:
            wait(0.002)
        duration_srt     = time_delta_to_str(duration.duration)
        expected_output = f'\nDuration: {duration_srt}'
        assert builtins_print.mock_calls == [call(expected_output)]

from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.trace.Trace_Call__Stats import Trace_Call__Stats
from tests.utils.trace.test_Trace_Call__Stack import Frames_Test_Data


class test_Trace_Call_Stats(TestCase):

    def setUp(self):
        self.trace_call_stats = Trace_Call__Stats()

    def test___kwargs__(self):
        expected_locals = dict(event_call      = 0 ,
                               event_exception = 0 ,
                               event_line      = 0 ,
                               event_return    = 0 ,
                               event_unknown  =  0 ,
                               raw_call_stats = [] )

        assert Trace_Call__Stats.__cls_kwargs__    () == expected_locals
        assert Trace_Call__Stats.__default_kwargs__() == expected_locals
        assert Trace_Call__Stats().__kwargs__      () == expected_locals
        assert Trace_Call__Stats().__locals__      () == expected_locals

    def test_log_frame(self):
        print()
        test_frames = Frames_Test_Data()
        stats           = self.trace_call_stats

        stats.log_frame(test_frames.frame_1)
        stats.log_frame(test_frames.frame_2)

        pprint(stats.frames_stats())


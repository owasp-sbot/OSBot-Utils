from unittest import TestCase

from osbot_utils.utils.trace.Trace_Call__Stats import Trace_Call__Stats


class test_Trace_Call_Stats(TestCase):

    def setUp(self):
        self.trace_call_stats = Trace_Call__Stats()

    def test___kwargs__(self):
        expected_locals = dict(event_call      = 0 ,
                               event_exception = 0 ,
                               event_line      = 0 ,
                               event_return    = 0 ,
                               event_unknown  =  0 )

        assert Trace_Call__Stats.__cls_kwargs__    () == expected_locals
        assert Trace_Call__Stats.__default_kwargs__() == expected_locals
        assert Trace_Call__Stats().__kwargs__      () == expected_locals
        assert Trace_Call__Stats().__locals__      () == expected_locals

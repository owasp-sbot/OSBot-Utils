from unittest                                                                     import TestCase
from osbot_utils.helpers.timestamp_capture.schemas.Schema__Method_Timing          import Schema__Method_Timing
from osbot_utils.helpers.timestamp_capture.schemas.Schema__Timestamp_Entry        import Schema__Timestamp_Entry
from osbot_utils.helpers.timestamp_capture.static_methods.timestamp_utils         import (timestamp_entry__to_ms    ,
                                                                                          method_timing__total_ms   ,
                                                                                          method_timing__avg_ms     ,
                                                                                          method_timing__self_ms    ,
                                                                                          method_timing__min_ms     ,
                                                                                          method_timing__max_ms     )


class test_timestamp_utils(TestCase):

    def test_timestamp_entry__to_ms(self):                                        # Test converting entry timestamp to ms
        entry = Schema__Timestamp_Entry(timestamp_ns=50_000_000)                  # 50ms
        assert timestamp_entry__to_ms(entry) == 50.0

        entry = Schema__Timestamp_Entry(timestamp_ns=1_500_000)                   # 1.5ms
        assert timestamp_entry__to_ms(entry) == 1.5

        entry = Schema__Timestamp_Entry(timestamp_ns=0)
        assert timestamp_entry__to_ms(entry) == 0.0

    def test_method_timing__total_ms(self):                                       # Test total time in ms
        timing = Schema__Method_Timing(total_ns=100_000_000)                      # 100ms
        assert method_timing__total_ms(timing) == 100.0

        timing = Schema__Method_Timing(total_ns=0)
        assert method_timing__total_ms(timing) == 0.0

    def test_method_timing__avg_ms(self):                                         # Test average time per call
        timing = Schema__Method_Timing(total_ns=100_000_000, call_count=10)       # 100ms / 10 = 10ms avg
        assert method_timing__avg_ms(timing) == 10.0

        timing = Schema__Method_Timing(total_ns=50_000_000, call_count=5)         # 50ms / 5 = 10ms avg
        assert method_timing__avg_ms(timing) == 10.0

    def test_method_timing__avg_ms__zero_calls(self):                             # Test avg with zero calls (edge case)
        timing = Schema__Method_Timing(total_ns=100_000_000, call_count=0)
        assert method_timing__avg_ms(timing) == 0.0

    def test_method_timing__self_ms(self):                                        # Test self time in ms
        timing = Schema__Method_Timing(self_ns=30_000_000)                        # 30ms
        assert method_timing__self_ms(timing) == 30.0

    def test_method_timing__min_ms(self):                                         # Test min time in ms
        timing = Schema__Method_Timing(min_ns=5_000_000)                          # 5ms
        assert method_timing__min_ms(timing) == 5.0

    def test_method_timing__max_ms(self):                                         # Test max time in ms
        timing = Schema__Method_Timing(max_ns=25_000_000)                         # 25ms
        assert method_timing__max_ms(timing) == 25.0
from unittest                                                                    import TestCase
from osbot_utils.helpers.timestamp_capture.schemas.Schema__Method_Timing         import Schema__Method_Timing
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.utils.Objects                                                   import base_classes


class test_Schema__Method_Timing(TestCase):

    def test__init__(self):                                                      # Test auto-initialization of schema
        with Schema__Method_Timing() as _:
            assert type(_)          is Schema__Method_Timing
            assert base_classes(_)  == [Type_Safe, object]
            assert _.name           == ''
            assert _.call_count     == 0
            assert _.total_ns       == 0
            assert _.min_ns         == 0
            assert _.max_ns         == 0
            assert _.self_ns        == 0

    def test__init____with_values(self):                                         # Test initialization with values
        with Schema__Method_Timing(name       = 'process_data'     ,
                                   call_count = 10                 ,
                                   total_ns   = 50_000_000         ,             # 50ms
                                   min_ns     = 3_000_000          ,             # 3ms
                                   max_ns     = 8_000_000          ,             # 8ms
                                   self_ns    = 30_000_000         ) as _:       # 30ms
            assert _.name           == 'process_data'
            assert _.call_count     == 10
            assert _.total_ns       == 50_000_000
            assert _.min_ns         == 3_000_000
            assert _.max_ns         == 8_000_000
            assert _.self_ns        == 30_000_000

    def test__json_round_trip(self):                                             # Test serialization round-trip
        with Schema__Method_Timing(name       = 'convert'          ,
                                   call_count = 5                  ,
                                   total_ns   = 100_000_000        ,
                                   min_ns     = 15_000_000         ,
                                   max_ns     = 25_000_000         ,
                                   self_ns    = 60_000_000         ) as _:
            json_data = _.json()
            recreated = Schema__Method_Timing.from_json(json_data)

            assert recreated.name       == _.name
            assert recreated.call_count == _.call_count
            assert recreated.total_ns   == _.total_ns
            assert recreated.min_ns     == _.min_ns
            assert recreated.max_ns     == _.max_ns
            assert recreated.self_ns    == _.self_ns
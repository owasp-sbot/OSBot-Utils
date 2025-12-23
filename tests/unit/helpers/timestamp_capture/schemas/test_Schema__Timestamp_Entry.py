from unittest                                                                      import TestCase
from osbot_utils.helpers.timestamp_capture.schemas.Schema__Timestamp_Entry         import Schema__Timestamp_Entry
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe
from osbot_utils.utils.Objects                                                     import base_classes


class test_Schema__Timestamp_Entry(TestCase):

    def test__init__(self):                                                        # Test auto-initialization of schema
        with Schema__Timestamp_Entry() as _:
            assert type(_)              is Schema__Timestamp_Entry
            assert base_classes(_)      == [Type_Safe, object]
            assert _.name               == ''
            assert _.event              == ''
            assert _.timestamp_ns       == 0
            assert _.clock_ns           == 0
            assert _.thread_id          == 0
            assert _.depth              == 0
            assert _.extra              is None

    def test__init____with_values(self):                                           # Test initialization with values
        with Schema__Timestamp_Entry(name         = 'test_method'  ,
                                     event        = 'enter'        ,
                                     timestamp_ns = 123456789      ,
                                     clock_ns     = 987654321      ,
                                     thread_id    = 12345          ,
                                     depth        = 3              ,
                                     extra        = {'key': 'val'} ) as _:
            assert _.name               == 'test_method'
            assert _.event              == 'enter'
            assert _.timestamp_ns       == 123456789
            assert _.clock_ns           == 987654321
            assert _.thread_id          == 12345
            assert _.depth              == 3
            assert _.extra              == {'key': 'val'}

    def test__json_round_trip(self):                                               # Test serialization round-trip
        with Schema__Timestamp_Entry(name         = 'method_a'     ,
                                     event        = 'exit'         ,
                                     timestamp_ns = 111111111      ,
                                     clock_ns     = 222222222      ,
                                     thread_id    = 999            ,
                                     depth        = 2              ) as _:
            json_data  = _.json()
            recreated  = Schema__Timestamp_Entry.from_json(json_data)

            assert recreated.name         == _.name
            assert recreated.event        == _.event
            assert recreated.timestamp_ns == _.timestamp_ns
            assert recreated.clock_ns     == _.clock_ns
            assert recreated.thread_id    == _.thread_id
            assert recreated.depth        == _.depth
from unittest                                                                      import TestCase
from osbot_utils.helpers.timestamp_capture.schemas.Schema__Timestamp_Entry         import Schema__Timestamp_Entry
from osbot_utils.utils.Objects                                                     import base_classes


class test_Schema__Timestamp_Entry(TestCase):

    def test__init__(self):                                                        # Test auto-initialization of schema
        with Schema__Timestamp_Entry() as _:
            assert type(_)              is Schema__Timestamp_Entry
            assert base_classes(_)      == [object]
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
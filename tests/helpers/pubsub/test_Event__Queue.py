import sys
from threading                                          import Event
from unittest                                           import TestCase
from osbot_utils.base_classes.Kwargs_To_Self            import Kwargs_To_Self
from osbot_utils.helpers.pubsub.Event__Queue            import Event__Queue, QUEUE_WAIT_TIMEOUT
from osbot_utils.helpers.pubsub.schemas.Schema__Event   import Schema__Event
from osbot_utils.utils.Objects                          import base_types

class test_Event_Queue(TestCase):

    def setUp(cls):
        cls.event_queue = Event__Queue()

    def test__init__(self):
        with self.event_queue as _:
            assert _.__dict__ == {'event_class'  : Schema__Event      ,
                                  'events'       : []                 ,
                                  'log_events'   : False              ,
                                  'queue'        : _.queue            ,
                                  'queue_name'   : _.queue_name       ,
                                  'queue_timeout': QUEUE_WAIT_TIMEOUT ,
                                  'running'      : True               ,
                                  'thread'       : _.thread           }
            assert _.queue_name.startswith('event_queue')


    def test_start_stop(self):
        _ = self.event_queue                        # can't use with context since it will start and end the queue

        _.queue_timeout   = 0.00001
        assert _.running               == False

        assert _.start()               == _
        assert _.running               is True
        assert _.thread                is not None
        assert _.thread.daemon         is True
        assert _.thread.name           == "Thread-4 (run_thread)"
        assert _.thread.is_alive()     is True
        #assert _.thread._is_stopped    is False
        assert _.thread._target        == _.run_thread
        assert _.thread._args          == ()
        assert _.thread._kwargs        == {}
        assert _.thread._stderr        == sys.stderr
        assert type(_.thread._started) is Event

        assert _.stop()                 == _
        assert _.running               is False
        assert _.thread.is_alive()     is True
        #assert _.thread._is_stopped    is False

        assert _.wait_for_thread_ends() is _
        assert _.thread.is_alive()     is False
        #assert _.thread._is_stopped    is True              # doesn't exist in python 3.13

    def test_handle_event(self):

        class Some_Event(Event__Queue):
            events : list

            def handle_event(self, event):
                self.events.append(event)

        with Some_Event() as _:
            event_1 = _.new_event_obj(event_data={'some': 'event'})
            assert base_types(_)    == [Event__Queue, Kwargs_To_Self, object]
            assert _.running        is True
            assert _.queue.qsize()  == 0
            _.queue.put(event_1, block=True)
            assert _.queue.qsize()  == 1
            _.wait_micro_seconds()
            assert _.events         == [event_1]
            assert _.queue.qsize()  == 0

        assert _.running is False

    def test_send_message(self):
        message_1 = 'Hello World!'
        message_2 = 'from here'
        data_1    = {'some': 'data', 'goes': 'here'}
        data_2    = 'message will become data value'
        with self.event_queue as _:
            _.log_events = True
            event_1 = _.send_message(message_1)
            event_2 = _.send_message(message_2, event_target='some target')
            event_3 = _.new_event_obj()
            event_4 = _.new_event_obj(timestamp=123, event_id='an-event_id', connection_id='an-topic-id')
            assert _.send_event(event_3) is True
            assert _.send_event(event_4) is True
            assert _.send_event('aaaaa') is False
            event_5 = _.send_data(data_1)
            event_6 = _.send_data(data_2)
            _.wait_micro_seconds()
            assert _.events == [event_1, event_2, event_3, event_4, event_5, event_6]
            assert event_1.json() == {'event_data'  : {}                ,
                                      'event_id'     : event_1.event_id ,
                                      'event_message': 'Hello World!'   ,
                                      'event_target' : ''               ,
                                      'event_type'   : ''               ,
                                      'timestamp'    : event_1.timestamp,
                                      'connection_id': '' }
            assert event_2.json() == {'event_data'  : {}                ,
                                      'event_id'     : event_2.event_id ,
                                      'event_message': message_2        ,
                                      'event_target' : 'some target'    ,
                                      'event_type'   : ''               ,
                                      'timestamp'    : event_2.timestamp,
                                      'connection_id': ''               }
            assert event_3.json() == {'event_data'  : {}                ,
                                      'event_id'     : event_3.event_id ,
                                      'event_message': ''               ,
                                      'event_target' : ''               ,
                                      'event_type'   : ''               ,
                                      'timestamp'    : event_3.timestamp,
                                      'connection_id': ''               }
            assert event_4.json() == {'event_data'  : {}                ,
                                      'event_id'     : 'an-event_id'    ,
                                      'event_message': ''               ,
                                      'event_target' : ''               ,
                                      'event_type'   : ''               ,
                                      'timestamp'    : 123              ,
                                      'connection_id': 'an-topic-id'    }
            assert event_5.json() == {'event_data'   : data_1            ,
                                      'event_id'     : event_5.event_id ,
                                      'event_message': ''               ,
                                      'event_target' : ''               ,
                                      'event_type'   : ''               ,
                                      'timestamp'    : event_5.timestamp,
                                      'connection_id': ''    }
            assert event_6.json() == {'event_data'  : {'data': data_2}  ,
                                      'event_id'     :  event_6.event_id,
                                      'event_message': ''               ,
                                      'event_target' : ''               ,
                                      'event_type'   : ''               ,
                                      'timestamp'    : event_6.timestamp,
                                      'connection_id': ''               }

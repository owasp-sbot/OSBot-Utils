import sys
from threading import Event
from unittest import TestCase

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.pubsub.Event__Queue import Event__Queue, QUEUE_WAIT_TIMEOUT
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import obj_info, base_types


class test_Event_Queue(TestCase):

    def setUp(cls):
        cls.event_queue = Event__Queue()

    def test__init__(self):
        with self.event_queue as _:
            assert _.__dict__ == {'queue'        : _.queue            ,
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
        assert _.thread.name           == "Thread-3 (run_thread)"
        assert _.thread.is_alive()     is True
        assert _.thread._is_stopped    is False
        assert _.thread._target        == _.run_thread
        assert _.thread._args          == ()
        assert _.thread._kwargs        == {}
        assert _.thread._stderr        == sys.stderr
        assert type(_.thread._started) is Event

        assert _.stop()                 == _
        assert _.running               is False
        assert _.thread.is_alive()     is True
        assert _.thread._is_stopped    is False

        assert _.wait_for_thread_ends() is _
        assert _.thread.is_alive()     is False
        assert _.thread._is_stopped    is True

    def test_handle_event(self):

        class Some_Event(Event__Queue):
            events : list

            def handle_event(self, event):
                self.events.append(event)

        event_1 = {'some': 'event'}
        with Some_Event() as _:
            assert base_types(_)    == [Event__Queue, Kwargs_To_Self, object]
            assert _.running        is True
            assert _.queue.qsize()  == 0
            _.queue.put(event_1, block=True)
            assert _.queue.qsize()  == 1
            _.wait_for(0.00001)
            assert _.events         == [event_1]
            assert _.queue.qsize()  == 0

        assert _.running is False

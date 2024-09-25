from unittest import TestCase

from osbot_utils.helpers.pubsub.Event__Queue import Event__Queue
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Execute_Method import Schema__Event__Execute_Method
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import is_guid, wait_for


class test_Schema__Event__Execute_Method(TestCase):

    def setUp(self):
        self.target_method = self.an_method
        self.target_args   = ["arg value 1"]
        self.target_kwargs = dict(arg_2='value2')
        event_kwargs = dict(method_target=self.target_method, method_args=self.target_args, method_kwargs=self.target_kwargs)
        self.event_execute_method = Schema__Event__Execute_Method(**event_kwargs)

    def an_method(self, arg_1, arg_2=None):
        return f"{arg_1} : {arg_2} : 42 "

    def test__init__(self):
        with self.event_execute_method as _:
            assert _.__locals__() == {'connection_id'   : ''                 ,
                                      'event_data'      : {}                 ,
                                      'event_id'        : ''                 ,
                                      'event_message'   : ''                 ,
                                      'event_target'    : ''                 ,
                                      'event_type'      : 'execute-method'   ,
                                      'execution_result': None               ,
                                      'method_args'     : ['arg value 1']    ,
                                      'method_kwargs'   : {'arg_2': 'value2'},
                                      'method_target'   : self.target_method ,
                                      'timestamp'       : 0                  }



    def test__event_queue__send_event(self):

        with Event__Queue(log_events=True) as _:
            assert _.running                                    is True
            assert self.event_execute_method.event_id           == ''
            assert _.send_event(self.event_execute_method)      is True
            assert is_guid(self.event_execute_method.event_id)  is True
            assert _.queue_size()                               == 1
            assert _.wait_for_queue_empty()                     is True
            assert _.queue_size()                               == 0
            assert len(_.events)                                == 1
            assert is_guid(_.events[0].event_id)                is True
        assert _.running                                    is False

    def test__event_queue__handle_event(self):

        class Execute_Events(Event__Queue):

            def handle_event(self, event):
                result = event.execute()
                pprint(result)

        print()
        with Execute_Events(log_events=True) as _:
            assert _.send_event(self.event_execute_method) is True
            assert _.wait_for_queue_completed()


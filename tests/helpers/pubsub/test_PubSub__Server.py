from unittest import TestCase

from osbot_utils.helpers.pubsub.PubSub__Client import PubSub__Client
from osbot_utils.helpers.pubsub.PubSub__Server import PubSub__Server
from osbot_utils.helpers.pubsub.PubSub__Sqlite import PubSub__Sqlite
from osbot_utils.helpers.pubsub.schemas.Schema__Event import Schema__Event
from osbot_utils.testing.Logging import DEFAULT_LOG_FORMAT
from osbot_utils.testing.Stdout import Stdout
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import wait_for


class test_PubSub__Server(TestCase):
    server     : PubSub__Server

    @classmethod
    def setUpClass(cls):
        cls.server = PubSub__Server()
        cls.server.logging.log_format = ''
        cls.server.logging.set_format_on_all_handlers()

    @classmethod
    def tearDownClass(cls):
        cls.server.logging.log_format = DEFAULT_LOG_FORMAT

    def test_client_send_event(self):
        print()
        print()

        message_1 = 'hello from the client!!!!!'
        data_1    = {'we':'can also send dict'}
        event_3   = Schema__Event(event_message='an message')

        with self.server as _:
            _.queue_timeout = 0.001
            client = _.new_client()
            assert isinstance(client, PubSub__Client)
            event_1  = client.send_message(message_1)
            event_2  = client.send_data   (data_1   )
            result_3 = client.send_event  (event_3  )

            _.wait_micro_seconds()

            assert _.events == [event_1, event_2, event_3]
            assert result_3 is True



# def test_new_client(self):
    #     with self.server as _:
    #         client = _.new_client()
    #         assert type(client) is PubSub__Client

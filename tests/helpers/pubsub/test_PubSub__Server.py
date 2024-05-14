from unittest import TestCase

from osbot_utils.helpers.pubsub.PubSub__Client import PubSub__Client
from osbot_utils.helpers.pubsub.PubSub__Server import PubSub__Server
from osbot_utils.helpers.pubsub.PubSub__Sqlite import PubSub__Sqlite
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

    def test_start__stop(self):
        print()
        print()

        client_event_1 = 'hello from the client!!!!!'
        client_event_2 = {'we':'can also send dict'}
        with Stdout() as stdout:
            with self.server as _:
                _.queue_timeout = 0.001
                client = _.new_client()
                self.server.start()
                client.send_event(client_event_1)
                client.send_event(client_event_2)
                #_.events.put({'aaaa'})

                _.wait_for(0.0004)
                _.stop()
                _.wait_for_thread_ends()
                assert _.events == [client_event_1, client_event_2]

        assert stdout.value() == ''

# def test_new_client(self):
    #     with self.server as _:
    #         client = _.new_client()
    #         assert type(client) is PubSub__Client

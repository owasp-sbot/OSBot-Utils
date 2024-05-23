from unittest import TestCase

from osbot_utils.helpers.pubsub.PubSub__Client import PubSub__Client
from osbot_utils.helpers.pubsub.PubSub__Server import PubSub__Server
from osbot_utils.helpers.pubsub.PubSub__Sqlite import PubSub__Sqlite
from osbot_utils.helpers.pubsub.schemas.Schema__Event import Schema__Event
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Join_Room import Schema__Event__Join_Room
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Leave_Room import Schema__Event__Leave_Room
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Message import Schema__Event__Message
from osbot_utils.testing.Logging import DEFAULT_LOG_FORMAT
from osbot_utils.testing.Stdout import Stdout
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import wait_for, random_text


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

    def test__init__(self):
        with self.server as _:
            assert self.server.__locals__() == {  'clients'          : {}           ,
                                                  'clients_connected': set()        ,
                                                  'event_class'      : Schema__Event,
                                                  'events'           : []           ,
                                                  'log_events'       : False        ,
                                                  'logging'          : _.logging    ,
                                                  'queue'            : _.queue      ,
                                                  'queue_name'       : _.queue_name ,
                                                  'queue_timeout'    : 1.0          ,
                                                  'rooms'            : {}           ,
                                                  'running'          : True         ,
                                                  'thread'           : _.thread     }

    def test_client_send_event(self):
        print()
        print()

        message_1 = 'hello from the client!!!!!'
        data_1    = {'we':'can also send dict'}
        event_3   = Schema__Event__Message(event_message='an message')

        with self.server as _:
            _.log_events = True
            _.queue_timeout = 0.001
            client = _.new_client()
            assert isinstance(client, PubSub__Client)
            event_1  = client.send_message(message_1)
            event_2  = client.send_data   (data_1   )
            result_3 = client.send_event  (event_3  )

            _.wait_micro_seconds(1000)

            assert _.events == [event_1, event_2, event_3]
            assert result_3 is True

    def test_new_client(self):
        with self.server as _:
            client    = _.new_client()
            client_id = client.client_id
            assert isinstance(client, PubSub__Client)
            assert _.get_client(client_id) == client
            assert _.clients[client_id] == client

    def test_client_connect_and_disconnect__via_events(self):
        with (self.server as _):

            client = _.new_client()

            client.connect()
            _.wait_micro_seconds(10)

            assert client in _.clients_connected

            client.disconnect()
            _.wait_micro_seconds()
            assert client not in _.clients_connected        # BUG

    def test_client_join_room__client_leave_room(self):
        with (self.server as _):
            room_name        = random_text('room_name')
            client_1         = _.new_client()
            client_2         = _.new_client()
            join_room_event  = Schema__Event__Join_Room(room_name=room_name)
            leave_room_event = Schema__Event__Leave_Room(room_name=room_name)

            assert _.rooms == {}
            _.client_join_room(client_1, join_room_event)
            assert _.rooms[room_name].clients == {client_1}
            _.client_join_room(client_1, join_room_event)
            assert _.rooms[room_name].clients == {client_1}
            _.client_join_room(client_2, join_room_event)
            assert _.rooms[room_name].clients == {client_1, client_2}

            _.client_leave_room(client_1, leave_room_event)
            assert _.rooms[room_name].clients == {client_2}
            _.client_leave_room(client_1, leave_room_event)
            assert _.rooms[room_name].clients == {client_2}
            _.client_leave_room(client_2, leave_room_event)
            assert _.rooms[room_name].clients == set()

    def test_client_join_room__client_leave_room__via_events(self):
        print()
        with self.server as _:
            room_name = random_text('room_name')
            client_1 = _.new_client()
            client_2 = _.new_client()

            client_1.join_room(room_name)
            client_2.join_room(room_name)
            _.wait_micro_seconds()                            # this needs to be higher if we do anything inside those client_* methods :)
            assert _.room(room_name).clients == {client_1, client_2}

            client_1.leave_room(room_name)
            client_2.leave_room(room_name)
            _.wait_micro_seconds()
            assert _.room(room_name).clients == set()

    def test_client_receive_messages__via_room(self):
        with self.server as _:
            message_1 = 'hello both clients'
            message_2 = 'now only to client 2'
            room_name = random_text('room_name')
            room      = _.room(room_name)
            client_1  = _.new_client()
            client_2  = _.new_client()

            client_1.join_room(room_name)
            client_2.join_room(room_name)
            _.wait_micro_seconds(10)

            room.send_to_clients__message(message_1)             #  todo: fix this to be Events/Messages received via event_queue
            _.wait_micro_seconds(10)

            client_1.leave_room(room_name)
            _.wait_micro_seconds(10)

            room.send_to_clients__message(message_2)

            assert client_1.received_messages == [message_1]
            assert client_2.received_messages == [message_1, message_2]







# def test_new_client(self):
    #     with self.server as _:
    #         client = _.new_client()
    #         assert type(client) is PubSub__Client

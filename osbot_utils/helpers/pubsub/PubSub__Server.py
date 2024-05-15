import queue
from threading import Thread
from queue import Queue

from osbot_utils.helpers.pubsub.Event__Queue                        import Event__Queue
from osbot_utils.helpers.pubsub.PubSub__Client                      import PubSub__Client
from osbot_utils.helpers.pubsub.schemas.Schema__Event               import Schema__Event
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Connect      import Schema__Event__Connect
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Leave_Room   import Schema__Event__Leave_Room
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Disconnect   import Schema__Event__Disconnect
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Join_Room    import Schema__Event__Join_Room
from osbot_utils.testing.Logging                                    import Logging
from osbot_utils.utils.Dev                                          import pprint


class PubSub__Server(Event__Queue):
    #pubsub_db: PubSub__Sqlite
    clients          : dict
    clients_connected: set
    rooms            : dict[str, set[PubSub__Client]]
    logging          : Logging

    def __init__ (self):
        super().__init__()

    # def db_table_clients(self):
    #     return self.pubsub_db.table_clients()     # todo refactor to class that uses this as a base and uses sqlite to capture connections

    def add_client(self, client: PubSub__Client):
        client_id = client.client_id
        if client_id:
            self.clients[client_id] = client
        return self

    def client_connect(self, client):
        self.clients_connected.add(client)

    def client_disconnect(self, client):
        self.clients_connected.discard(client)

    def client_join_room(self, client, room_name):
        self.room(room_name).add(client)

    def client_leave_room(self, client, room_name):
        self.room(room_name).discard(client)

    def get_client(self, client_id):
        return self.clients.get(client_id)

    def handle_event(self, event: Schema__Event):
        event_type = type(event)
        client     = self.clients.get(event.connection_id)
        if client:
            if   event_type is Schema__Event__Connect    : self.client_connect   (client)
            elif event_type is Schema__Event__Disconnect : self.client_disconnect(client)
            elif event_type is Schema__Event__Join_Room  : self.client_join_room (client, event.room_name)
            elif event_type is Schema__Event__Leave_Room : self.client_leave_room(client, event.room_name)
            else:
                pprint(f'NOT FOUND : {event_type}')

        if self.log_events:
            self.events.append(event)
        return True

    def log(self, message):
        self.logging.debug(message)
        return self

    def new_client(self):
        client = PubSub__Client(event_queue = self)
        self.add_client(client)
        return client

    def room(self, room_name):
        if room_name not in self.rooms:
            self.rooms[room_name] = set()
        return self.rooms.get(room_name)






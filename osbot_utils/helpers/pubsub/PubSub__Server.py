import queue
from threading import Thread
from queue import Queue

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.pubsub.Event__Queue import Event__Queue
from osbot_utils.helpers.pubsub.PubSub__Client import PubSub__Client
from osbot_utils.helpers.pubsub.PubSub__Sqlite  import PubSub__Sqlite
from osbot_utils.helpers.pubsub.schemas.Schema__Event import Schema__Event
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Connect import Schema__Event__Connect
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Disconnect import Schema__Event__Disconnect
from osbot_utils.testing.Logging                import Logging


class PubSub__Server(Event__Queue):
    #pubsub_db: PubSub__Sqlite
    clients          : dict
    clients_connected: set
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

    def get_client(self, client_id):
        return self.clients.get(client_id)

    def handle_event(self, event: Schema__Event):
        event_type = type(event)
        client     = self.clients.get(event.connection_id)
        if client:
            if event_type is Schema__Event__Connect:
                self.clients_connected.add(client)
            elif event_type is Schema__Event__Disconnect:
                self.clients_connected.discard(client)

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




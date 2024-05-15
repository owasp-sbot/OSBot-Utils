from queue import Queue

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.pubsub.Event__Queue import Event__Queue
from osbot_utils.helpers.pubsub.schemas.Schema__Event import Schema__Event
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Connect import Schema__Event__Connect
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Disconnect import Schema__Event__Disconnect
from osbot_utils.utils.Misc import random_guid


class PubSub__Client(Kwargs_To_Self):
    event_queue : Event__Queue
    client_id   : str

    def __init__(self, **kwargs):
        self.client_id = kwargs.get('client_id') or random_guid()
        super().__init__(**kwargs)

    def connect(self):
        event_connect = Schema__Event__Connect(connection_id=self.client_id)
        self.send_event(event_connect)
        return self

    def disconnect(self):
        event_connect = Schema__Event__Disconnect(connection_id=self.client_id)
        self.send_event(event_connect)
        return self

    def send_data(self, event_data, **kwargs):
        return self.event_queue.send_data(event_data, **kwargs)

    def send_event(self, event : Schema__Event):
        return self.event_queue.send_event(event)

    def send_message(self, message, **kwargs):
        return self.event_queue.send_message(message, **kwargs)

from queue import Queue
from typing import List

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.pubsub.Event__Queue import Event__Queue
from osbot_utils.helpers.pubsub.schemas.Schema__Event import Schema__Event
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Connect import Schema__Event__Connect
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Disconnect import Schema__Event__Disconnect
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Join_Room import Schema__Event__Join_Room
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Leave_Room import Schema__Event__Leave_Room
from osbot_utils.utils.Misc import random_guid


class PubSub__Client(Kwargs_To_Self):
    event_queue       : Event__Queue
    client_id         : str
    received_messages : List[str]           # todo: fix this to be Events/Messages received via event_queue

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

    def join_room(self, room_name):
        event  = Schema__Event__Join_Room(connection_id=self.client_id, room_name=room_name)
        self.send_event(event)
        return self

    def leave_room(self, room_name):
        event  = Schema__Event__Leave_Room(connection_id=self.client_id, room_name=room_name)
        self.send_event(event)
        return self

    def send_data(self, event_data, **kwargs):
        return self.event_queue.send_data(event_data, connection_id=self.client_id, **kwargs)

    def send_event(self, event : Schema__Event):
        event.connection_id = self.client_id
        return self.event_queue.send_event(event)

    def send_message(self, message, **kwargs):
        return self.event_queue.send_message(message, connection_id=self.client_id, **kwargs)

    def receive_message(self, message):
        self.received_messages.append(message)      # todo: fix this to be Events/Messages received via event_queue

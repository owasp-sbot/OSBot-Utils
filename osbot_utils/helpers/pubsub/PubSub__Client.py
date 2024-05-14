from queue import Queue

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.pubsub.Event__Queue import Event__Queue
from osbot_utils.helpers.pubsub.schemas.Schema__Event import Schema__Event


class PubSub__Client(Kwargs_To_Self):
    event_queue : Event__Queue

    def send_data(self, event_data, **kwargs):
        return self.event_queue.send_data(event_data, **kwargs)

    def send_event(self, event : Schema__Event):
        return self.event_queue.send_event(event)

    def send_message(self, message, **kwargs):
        return self.event_queue.send_message(message, **kwargs)

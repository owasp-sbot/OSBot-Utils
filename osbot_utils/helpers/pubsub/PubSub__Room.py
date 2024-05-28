from typing import Set

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.pubsub.Event__Queue import Event__Queue
from osbot_utils.helpers.pubsub.PubSub__Client import PubSub__Client


class PubSub__Room(Kwargs_To_Self):
    event_queue: Event__Queue
    room_name  : str
    clients    : Set[PubSub__Client]

    def send_to_clients__message(self, message):
        for client in self.clients:
            client.receive_message(message)

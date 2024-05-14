from queue import Queue

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class PubSub__Client(Kwargs_To_Self):
    queue__events : Queue

    def send_event(self, message):
        self.queue__events.put(message)
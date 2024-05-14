import queue
from threading import Thread
from queue import Queue

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.pubsub.Event__Queue import Event__Queue
from osbot_utils.helpers.pubsub.PubSub__Client import PubSub__Client
from osbot_utils.helpers.pubsub.PubSub__Sqlite  import PubSub__Sqlite
from osbot_utils.testing.Logging                import Logging


class PubSub__Server(Event__Queue):
    #pubsub_db: PubSub__Sqlite

    logging       : Logging
    events        : list

    def __init__ (self):
        super().__init__()

    # def db_table_clients(self):
    #     return self.pubsub_db.table_clients()

    def handle_event(self, event):
        self.events.append(event)
        self.log(f'.... got an event...: {event} ')
        return True

    def log(self, message):
        self.logging.debug(message)
        return self

    def new_client(self):
        return PubSub__Client(queue__events = self.queue)

    def stop(self):
        self.running = False

    def run_thread(self):
        self.log('STARTING SERVER')
        super().run_thread()
        self.log("STOPPING server")

    def wait_for_thread_ends(self):
        self.thread.join()

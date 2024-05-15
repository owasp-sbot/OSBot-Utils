import time
from enum import Enum
from queue                                      import Queue, Empty
from threading                                  import Thread
from typing import Any

from osbot_utils.helpers.pubsub.schemas.Schema__Event import Schema__Event
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Message import Schema__Event__Message
from osbot_utils.utils                                import Misc
from osbot_utils.base_classes.Kwargs_To_Self          import Kwargs_To_Self
from osbot_utils.utils.Misc import random_text, wait_for, timestamp_utc_now, random_guid

QUEUE_WAIT_TIMEOUT  = 1.0                           # todo: see if this value is a good one to use here

class Event__Queue(Kwargs_To_Self):
    events       : list
    event_class  : type
    log_events   : bool   = False
    queue        : Queue
    queue_name   : str    = random_text('event_queue')
    queue_timeout: float  = QUEUE_WAIT_TIMEOUT
    running      : bool
    thread       : Thread = None


    def __init__(self, **kwargs):
        self.event_class = Schema__Event
        super().__init__(**kwargs)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False

    def new_event_obj(self, **kwargs):
        return self.event_class(**kwargs)

    def handle_event(self, event):
        if self.log_events:
            self.events.append(event)
        return True

    def send_event(self, event: Schema__Event):
        if isinstance(event, Schema__Event):
            if not event.timestamp:
                event.timestamp = timestamp_utc_now()
            if not event.event_id:
                event.event_id = random_guid()
            self.queue.put(event)
            return True
        return False

    def send_data(self, event_data, **kwargs):
        if type(event_data) is not dict:
            event_data = {'data': event_data}
        new_event = Schema__Event__Message(event_data=event_data, **kwargs)
        if self.send_event(new_event):
            return new_event

    def send_message(self, message, **kwargs):
        new_event = Schema__Event__Message(event_message=str(message), **kwargs)
        if self.send_event(new_event):
            return new_event

    def start(self):
        self.running = True
        self.thread =  Thread(target=self.run_thread, daemon=True)
        self.thread.start()
        return self

    def stop(self):
        self.running = False
        return self

    def run_thread(self):
        while self.running:
            try:
                event = self.queue.get(timeout=self.queue_timeout)
                if isinstance(event, self.event_class):
                    self.handle_event(event)
            except Empty:
                continue
            except Exception as e:                          # todo: add way to handle this (which are errors in the handle_event), may call an on_event_handler_exceptions method
                continue

    def wait_micro_seconds(self, value=10):
        time.sleep(0.000001 * value)


    def wait_for_thread_ends(self):
        self.thread.join()
        return self
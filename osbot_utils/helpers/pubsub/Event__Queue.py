import time
from queue                                                      import Queue, Empty
from threading                                                  import Thread
from osbot_utils.type_safe.Type_Safe                         import Type_Safe
from osbot_utils.helpers.pubsub.schemas.Schema__Event           import Schema__Event
from osbot_utils.helpers.pubsub.schemas.Schema__Event__Message  import Schema__Event__Message
from osbot_utils.utils.Misc                                     import random_text, timestamp_utc_now, random_guid

TIMEOUT__THREAD_JOIN              = 1.0                             # todo: see if this value is a good one to use here
TIMEOUT__QUEUE_GET                = 1.0
TIMEOUT__WAIT_FOR_QUEUE_COMPLETED = 0.05                            # todo: see if this value is too aggressive (or if will be better to use a value like 0.1 or 0.5)


class Event__Queue(Type_Safe):
    events              : list
    event_class         : type
    events_added        : int
    events_completed    : int
    events_failed       : int
    log_events          : bool   = False
    queue               : Queue
    queue_name          : str    = random_text('event_queue')
    queue_get_timeout   : float  = TIMEOUT__QUEUE_GET
    running             : bool
    thread              : Thread = None


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
            self.events_added += 1
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
        self.running = False                                         # will make the event loop stop at the next self.queue_get_timeout
        return self

    def queue_size(self):
        return self.queue.qsize()

    def run_thread(self):
        while self.running:
            try:
                event = self.queue.get(timeout=self.queue_get_timeout)
                if isinstance(event, self.event_class):
                    self.handle_event(event)
                    self.events_completed += 1
            except Empty:
                continue
            except Exception as e:                          # todo: add way to handle this (which are errors in the handle_event), may call an on_event_handler_exceptions method
                self.events_failed += 1
                continue

    def wait_micro_seconds(self, value=10):
        time.sleep(0.000001 * value)


    def wait_for_thread_ends(self):
        self.thread.join()
        return self

    # todo see if there are valid use cases for wait_for_queue_empty , or the wait_for_queue_completed is the one that is always used
    def wait_for_queue_empty(self, thread_join_timeout=TIMEOUT__THREAD_JOIN):             # this will start a new thread to wait for the main queue to be empty
        def wait_until_queue_empty():
            while self.running:
                if self.queue.empty():
                    break
                time.sleep(0.01)

        wait_thread = Thread(target=wait_until_queue_empty)
        wait_thread.start()
        wait_thread.join(timeout=thread_join_timeout)
        return self.queue.empty()

    def wait_for_queue_completed(self, thread_join_timeout=TIMEOUT__THREAD_JOIN):             # this will start a new thread to wait for the main queue to be empty
        def wait_until_queue_completed():
            while self.running:
                if self.queue.empty() and self.events_added == self.events_completed :
                    break
                time.sleep(TIMEOUT__WAIT_FOR_QUEUE_COMPLETED)
        wait_thread = Thread(target=wait_until_queue_completed)
        wait_thread.start()
        wait_thread.join(timeout=thread_join_timeout)
        return self.queue.empty()
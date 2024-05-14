from queue                                      import Queue, Empty
from threading                                  import Thread
from osbot_utils.utils                          import Misc
from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.utils.Misc                     import random_text, wait_for

QUEUE_WAIT_TIMEOUT  = 1.0                           # todo: see if this value is a good one to use here

class Event__Queue(Kwargs_To_Self):
    queue        : Queue
    queue_name   : str    = random_text('event_queue')
    running      : bool
    thread       : Thread = None
    queue_timeout: float = QUEUE_WAIT_TIMEOUT

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False

    def handle_event(self, event):
        return True

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
                event= self.queue.get(timeout=self.queue_timeout)
                self.handle_event(event)
            except Empty:
                continue
            except Exception as e:                          # todo: add way to handle this (which are errors in the handle_event), may call an on_event_handler_exceptions method
                continue

    def wait_for(self, seconds):
        Misc.wait_for(seconds)
        return self

    def wait_for_thread_ends(self):
        self.thread.join()
        return self
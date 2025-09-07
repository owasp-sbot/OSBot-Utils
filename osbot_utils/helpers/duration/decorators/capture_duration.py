import time
from osbot_utils.type_safe.Type_Safe import Type_Safe


class capture_duration(Type_Safe):
    action_name : str
    duration    : float
    start_time  : float
    end_time    : float
    seconds     : float
    precision   : int = 3                                       # Default rounding to 3 decimal places


    def __enter__(self):
        self.start_time = time.perf_counter()                   # Start the performance counter
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()                     # End the performance counter
        self.duration = self.end_time - self.start_time
        self.seconds = round(self.duration, self.precision)     # Use configurable precision
        return False                                            # Ensures that exceptions are rethrown

    def data(self):
        return {
            "start": self.start_time,
            "end": self.end_time,
            "seconds": self.seconds,
        }

    def print(self):
        print()
        if self.action_name:
            print(f'action "{self.action_name}" took: {self.seconds} seconds')
        else:
            print(f'action took: {self.seconds} seconds')
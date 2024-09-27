from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Misc import timestamp_utc_now


class capture_duration(Type_Safe):
    action_name     : str
    duration        : float
    start_timestamp : int
    end_timestamp   : int
    seconds         : float

    def __enter__(self):
        self.start_timestamp = timestamp_utc_now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_timestamp  = timestamp_utc_now()
        self.duration       = self.end_timestamp - self.start_timestamp
        self.seconds        = round(self.duration / 1000, 3)                # Duration in seconds (rounded to the 3 digits)
        return False                                                        # ensures that any exceptions that happened are rethrown

    def data(self):
        return dict(start = self.start_timestamp, end = self.end_timestamp, seconds = self.seconds)

    def print(self):
        print()
        if self.action_name:
            print(f'action "{self.action_name}" took: {self.seconds} seconds')
        else:
            print(f'action took: {self.seconds} seconds')
from osbot_utils.utils.Misc import timestamp_utc_now


class capture_duration():
    def __init__(self):
        self.duration        = None
        self.start_timestamp = None
        self.end_timestamp   = None
        self.seconds         = None

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
        print(f'action took: {self.seconds} seconds')

class print_duration(capture_duration):

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = super().__exit__(exc_type, exc_val, exc_tb)
        self.print()
        return result

from osbot_utils.utils.Misc import timestamp_now

class Timestamp_Now(int):
    def __new__(cls, value=None):
        if value is None:
            value = timestamp_now()
        return int.__new__(cls, value)

    def __init__(self, value=None):
        self.value = value if value is not None else timestamp_now()

    def __str__(self):
        return str(self.value)
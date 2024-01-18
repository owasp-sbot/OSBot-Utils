import random

from osbot_utils.utils.Misc import random_int

DEFAULT_VALUE__RANDOM_SEED = 42

class Random_Seed:
    def __init__(self, seed=DEFAULT_VALUE__RANDOM_SEED, enabled=True):
        self.enabled = enabled
        self.seed = seed

    def __enter__(self):
        if self.enabled:
            random.seed(self.seed)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.enabled:
            random.seed(None)

    def next_int(self, **kwargs):
        return random_int(**kwargs)

    def next_ints(self, count):
        ints = (self.next_int() for i in range(count))
        return ints


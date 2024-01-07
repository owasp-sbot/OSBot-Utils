from osbot_utils.utils.Dev import pprint

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Trace_Call__Stats(Kwargs_To_Self):

    event_call      : int
    event_exception : int
    event_line      : int
    event_return    : int
    event_unknown   : int            # to use for extra events that are not being captured

    def __repr__(self):
        return str(self.stats())

    def __eq__(self, target):
        if self is target:
            return True
        return self.stats() == target

    def stats(self):
        return self.__locals__()

    def print(self):
        pprint(self.stats())

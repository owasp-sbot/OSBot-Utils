from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Trace_Call__Stats(Kwargs_To_Self):

    event_call  : int
    event_return: int

    def __repr__(self):
        return str(self.__locals__())

    def __eq__(self, target):
        if self is target:
            return True
        return self.__locals__() == target

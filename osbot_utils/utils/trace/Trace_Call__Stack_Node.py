from osbot_utils.utils.Dev import pprint

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Trace_Call__Stack_Node(Kwargs_To_Self):
    call_index          : int
    children            : list
    locals              : dict
    name                : str
    source_code         : str
    source_code_caller  : str
    source_code_location: str

    def __eq__(self, other):
        if not isinstance(other, Trace_Call__Stack_Node):
            return False
        if self is other:
            return True
        return self.data() == other.data()

    def __repr__(self):
        return '[Trace_Call__Stack_Node]'


    def data(self):
        return self.__locals__()

    def print(self):
        pprint(self.data())

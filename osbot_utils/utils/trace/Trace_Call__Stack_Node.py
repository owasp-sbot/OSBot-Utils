from osbot_utils.utils.Dev import pprint

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Trace_Call__Stack_Node(Kwargs_To_Self):
    call_index          : int
    children            : list
    locals              : dict
    func_name           : str
    module              : str
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
        return f'Trace_Call__Stack_Node (call_index={self.call_index})'

    def info(self):
        return f'Stack_Node: call_index:{self.call_index} | name: {self.name} | children: {len(self.children)} | source_code: {self.source_code is not None}'

    def data(self):
        return self.__locals__()

    def print(self):
        pprint(self.data())

    def print_info(self):
        pprint(self.info())

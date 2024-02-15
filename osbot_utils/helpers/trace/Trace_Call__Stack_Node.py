from osbot_utils.utils.Misc import random_id

from osbot_utils.utils.Dev import pprint

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

EXTRA_DATA__RETURN_VALUE = '(return_value)'

class Trace_Call__Stack_Node(Kwargs_To_Self):
    call_duration       : float
    call_end            : float
    call_index          : int
    call_start          : float
    children            : list
    extra_data          : dict
    locals              : dict
    frame               : None
    func_name           : str
    lines               : list
    key                 : str
    module              : str
    name                : str
    source_code         : str
    source_code_caller  : str
    source_code_location: str

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     #self.key = random_id()

    def __eq__(self, other):
        if not isinstance(other, Trace_Call__Stack_Node):
            return False
        if self is other:
            return True
        return self.data() == other.data()

    def __repr__(self):
        return f'Trace_Call__Stack_Node (call_index={self.call_index})'

    def all_children(self):
        all_children = self.children.copy()                     # Initialize the list with the current node's children
        for child in self.children:                             # Recursively add the children of each child node
            all_children.extend(child.all_children())
        return all_children

    def info(self):
        return f'Stack_Node: call_index:{self.call_index} | name: {self.name} | children: {len(self.children)} | source_code: {self.source_code is not None}'

    def data(self):
        return self.__locals__()

    def print(self):
        pprint(self.data())

    def print_info(self):
        pprint(self.info())



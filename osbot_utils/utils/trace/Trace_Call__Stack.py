from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.trace.Trace_Call__Stack_Node import Trace_Call__Stack_Node


class Trace_Call__Stack(Kwargs_To_Self):

    stack_data : list

    def __eq__(self, target):
        if self is target:
            return True
        return self.stack_data == target

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __iter__(self):
        return iter(self.stack_data)

    def __getitem__(self, index):
        if -len(self.stack_data) <= index < len(self.stack_data):
            return self.stack_data[index]

    def __len__(self):
        return self.size()

    def add_node(self, title: str, call_index: int):
        stack_node = self.new_stack_node(title, call_index)
        return self.add_stack_node(stack_node)

    def add_stack_node(self, stack_node : Trace_Call__Stack_Node, frame=None):
        if type(stack_node) is Trace_Call__Stack_Node:
            if self.stack_data:                                             # if there are items in the stack
                self.top().children.append(stack_node)                      # add an xref to the new node to the children of the top node
            self.stack_data.append(stack_node)                              # append the new node to the stack
            if frame:
                frame.f_locals['__trace_depth'] = len(self)                 # todo: find a betten way than using adding __trace_depth to locals "to Store the depth in frame locals" (which will used to decide when to pop from the stack)
            return True
        return False

    def bottom(self):
        if self.stack_data:
            return self.stack_data[0]

    def new_stack_node(self, name, call_index):
        return Trace_Call__Stack_Node(call_index=call_index, name=name)

    def nodes(self):
        return self.stack_data

    def pop(self, frame):
        if frame:
            if '__trace_depth' in frame.f_locals:
                if frame.f_locals['__trace_depth'] == len(self):        # todo change this logic of using __trace_depth to detect when to pop from the stack
                    self.stack_data.pop()
                    return True
                    #self.stack.pop()  # Pop the stack on return if corresponding call was captured

        return False


    def top(self):
        if self.stack_data:
            return self.stack_data[-1]

    def size(self):
        return self.stack_data.__len__()
import linecache
import time
from copy                                               import deepcopy
from osbot_utils.base_classes.Kwargs_To_Self            import Kwargs_To_Self
from osbot_utils.helpers.trace.Trace_Call__Config       import Trace_Call__Config
from osbot_utils.helpers.trace.Trace_Call__Stack_Node   import Trace_Call__Stack_Node


class Trace_Call__Stack(Kwargs_To_Self):
    call_index : int
    stack_data : list
    config     : Trace_Call__Config
    root_node  : Trace_Call__Stack_Node
    line_index : int

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

    def add_frame(self, frame):
        if frame and frame.__class__.__name__=='frame':
            self.call_index += 1  # Increment the call index
            code        = frame.f_code                                                      # Get code object from frame
            func_name   = code.co_name                                                      # Get function name
            module      = frame.f_globals.get("__name__", "")                               # Get module name

            source_code = self.map_source_code(frame)
            full_name   = self.map_full_name(frame, module, func_name)
            new_node    = self.create_stack_node(frame, full_name, source_code, self.call_index)
            if self.add_stack_node(new_node, frame):
                return new_node


    def add_node(self, title: str):
        new_node = self.new_stack_node(title)
        if self.config.capture_duration:
            new_node.call_start = time.perf_counter()
        if self.add_stack_node(new_node):
            return new_node

    def add_stack_node(self, stack_node : Trace_Call__Stack_Node, frame=None):
        if type(stack_node) is Trace_Call__Stack_Node:
            if self.stack_data:                                             # if there are items in the stack
                self.top().children.append(stack_node)                      # add an xref to the new node to the children of the top node
            else:
                self.root_node = stack_node                                 # if not this is the first node and capture it as a root node
            self.stack_data.append(stack_node)                              # append the new node to the stack
            return True
        return False

    def bottom(self):
        if self.stack_data:
            return self.stack_data[0]

    def create_stack_node(self, frame, full_name, source_code, call_index):
        new_node = Trace_Call__Stack_Node(call_index=call_index, name=full_name)
        if frame:
            code      = frame.f_code
            new_node.func_name = code.co_name                           # Get function name
            new_node.module    = frame.f_globals.get("__name__", "")    # Get module name
            if source_code:
                 new_node.source_code           = source_code.get('source_code'          )
                 new_node.source_code_caller    = source_code.get('source_code_caller'   )
                 new_node.source_code_location  = source_code.get('source_code_location' )

            if self.config.capture_frame:
                new_node.frame = frame
            if self.config.capture_locals:
                if self.config.deep_copy_locals:
                    try:
                        new_node.locals = deepcopy(frame.f_locals)
                    except Exception as error:
                        new_node.locals = {'error': f'error in deepcopy: {error}'}
                else:
                    new_node.locals = frame.f_locals

            if self.config.capture_duration:
                new_node.call_start = time.perf_counter()
        return new_node

    def empty_stack(self):              # use to make sure the stack is empty (usally called at the end of a trace sessions)
        for node in reversed(list(self.stack_data)):
            self.pop(node)
        return self

    def map_source_code(self, frame):
        if self.config.trace_capture_source_code:
            filename             = frame.f_code.co_filename
            lineno               = frame.f_lineno
            source_code          = linecache.getline(filename, lineno).strip()

            caller_filename      = frame.f_back.f_code.co_filename
            caller_lineno        = frame.f_back.f_lineno
            source_code_caller   = linecache.getline(caller_filename, caller_lineno).strip()
            source_code_location = f'{filename}:{lineno}'
        else:
            source_code          = ''
            source_code_caller   = ''
            source_code_location = ''

        return dict(source_code          = source_code          ,
                    source_code_caller   = source_code_caller   ,
                    source_code_location = source_code_location )

    def map_full_name(self, frame, module, func_name):
        if frame and module and func_name:
            instance = frame.f_locals.get("self", None)                                                           # Get instance if available
            try:
                class_name = instance.__class__.__name__ if instance else ""
            except Exception:                                                               # note: this will trigger this exception: ansi_text_visible_length("some text")
                class_name = "<unavailable>"
            if class_name:
                full_name = f"{module}.{class_name}.{func_name}"
            else:
                full_name = f"{module}.{func_name}"
            return full_name

    def new_stack_node(self, name):
        return Trace_Call__Stack_Node(call_index=self.call_index, name=name)

    def nodes(self):
        return self.stack_data

    def remove_from_top(self, top_node, extra_data: dict):
        if self.config.capture_duration:
            top_node.call_end     = time.perf_counter()
            top_node.call_duration = top_node.call_end - top_node.call_start
        if type(extra_data) is dict:
            top_node.extra_data.update(extra_data)
        self.stack_data.pop()
        return True

    def pop(self, target, extra_data: dict = None):
        top_node = self.top()
        if target and top_node :
            if type(target) is Trace_Call__Stack_Node:                  # handle the case when target is Trace_Call__Stack_Node
                if target == top_node:                                  # if they match, pop the stack (since we are only capturing a subset of the stack)
                    return self.remove_from_top(top_node, extra_data)
            elif target is top_node.frame:                              # if not assume target is a frame
                return self.remove_from_top(top_node, extra_data)       # if they match, pop the stack (since we are only capturing a subset of the stack)
        return False

    def push(self, frame):
        return self.add_frame(frame)


    def top(self):
        if self.stack_data:
            return self.stack_data[-1]

    def size(self):
        return self.stack_data.__len__()
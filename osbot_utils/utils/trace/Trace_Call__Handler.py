import linecache
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.trace.Trace_Call__Config import Trace_Call__Config
from osbot_utils.utils.trace.Trace_Call__Stack import Trace_Call__Stack
from osbot_utils.utils.trace.Trace_Call__Stack_Node import Trace_Call__Stack_Node

DEFAULT_ROOT_NODE_NODE_TITLE = 'Trace Session'

class Trace_Call__Handler(Kwargs_To_Self):
    stack      : Trace_Call__Stack
    config     : Trace_Call__Config


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trace_title   = self.config.title or DEFAULT_ROOT_NODE_NODE_TITLE                           # Title for the trace root node
        self.stack.config  = self.config
        self.stack.add_node(self.trace_title)

    def add_frame(self, frame):
        return self.handle_event__call(frame)

    def add_trace_ignore(self, value):
        self.config.trace_ignore_start_with.append(value)
        return

    def handle_event__call(self, frame):
        if frame:
            code        = frame.f_code                                                      # Get code object from frame
            func_name   = code.co_name                                                      # Get function name
            module      = frame.f_globals.get("__name__", "")                               # Get module name
            capture     = self.should_capture(module, func_name)
            if capture:
                return self.stack.add_frame(frame)


    def handle_event__return(self, frame):
        return self.stack.pop(frame)

    def should_capture(self, module, func_name):
        capture = False
        if module and func_name:
            if self.config.trace_capture_all:
                capture = True
            else:
                for item in self.config.trace_capture_start_with:                                  # Check if the module should be captured
                    if module.startswith(item):
                        capture = True
                        break
            if self.config.trace_ignore_internals and func_name.startswith('_'):                   # Skip private functions
                capture = False

            for item in self.config.trace_ignore_start_with:                                       # Check if the module should be ignored
                if module.startswith(item):
                    capture = False
                    break
        return capture

    # todo: replace or remove this temp method to help with refactoring
    def stack_json(self):
        data = []
        for stack_node in self.stack:
            item = self.stack_json__parse_node(stack_node)
            data.append(item)
        return data

    def stack_json__parse_node(self, stack_node: Trace_Call__Stack_Node):
        node         = stack_node.data()
        new_children = []
        for child in node.get('children'):
            new_children.append(self.stack_json__parse_node(child))
        node['children'] = new_children
        return node

    def stack_top(self):
        if self.stack:
            return self.stack[-1]

    def trace_calls(self, frame, event, arg):
        if event == 'call':
            self.handle_event__call(frame)
        elif event == 'return':
            self.handle_event__return(frame)
        return self.trace_calls

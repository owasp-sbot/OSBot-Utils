import linecache
from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.utils.trace.Trace_Call__Config     import Trace_Call__Config
from osbot_utils.utils.trace.Trace_Call__Stack      import Trace_Call__Stack
from osbot_utils.utils.trace.Trace_Call__Stack_Node import Trace_Call__Stack_Node, EXTRA_DATA__RETURN_VALUE
from osbot_utils.utils.trace.Trace_Call__Stats      import Trace_Call__Stats

DEFAULT_ROOT_NODE_NODE_TITLE = 'Trace Session'

class Trace_Call__Handler(Kwargs_To_Self):
    config : Trace_Call__Config
    stack  : Trace_Call__Stack
    stats  : Trace_Call__Stats


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trace_title   = self.config.title or DEFAULT_ROOT_NODE_NODE_TITLE                           # Title for the trace root node
        self.stack.config  = self.config

    def add_frame(self, frame):
        return self.handle_event__call(frame)

    def add_trace_ignore(self, value):
        self.config.trace_ignore_start_with.append(value)
        return

    def handle_event__call(self, frame):
        if frame:
            if self.config.capture_frame_stats:
                self.stats.log_frame(frame)
            if self.should_capture(frame):
                return self.stack.add_frame(frame)


    def handle_event__return(self, frame, return_value=None):
        if return_value and self.config.capture_extra_data:
            extra_data = { EXTRA_DATA__RETURN_VALUE : return_value}
        else:
            extra_data = {}
        return self.stack.pop(target=frame, extra_data = extra_data)

    def should_capture(self, frame):                                                    # todo: see if we can optimise these 3 lines (starting with frame.f_code) which are repeated in a number of places here
        capture = False
        if frame:
            code        = frame.f_code                                                      # Get code object from frame
            func_name   = code.co_name                                                      # Get function name
            module      = frame.f_globals.get("__name__", "")                               # Get module name

            if module and func_name:
                if self.config.trace_capture_all:
                    capture = True
                else:
                    for item in self.config.trace_capture_start_with:                                  # capture if the module starts with
                        if item:                                                                       # prevent empty queries  (which will always be true)
                            if module.startswith(item) or item =='*':
                                capture = True
                                break
                    for item in self.config.trace_capture_contains:                                    # capture if module of func_name contains
                        if item:                                                                       # prevent empty queries  (which will always be true)
                            if item in module or item in func_name:
                                capture = True
                                break
                if self.config.trace_ignore_internals and func_name.startswith('_'):                   # Skip private functions
                    capture = False

                for item in self.config.trace_ignore_start_with:                                       # Check if the module should be ignored
                    if module.startswith(item):
                        capture = False
                        break
        return capture

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
            self.stats.event_call +=1
            self.handle_event__call(frame)                  # todo: handle bug with locals which need to be serialised, since it's value will change
        elif event == 'return':
            self.stats.event_return += 1
            self.handle_event__return(frame, arg)
        elif event == 'exception':
            self.stats.event_exception +=1                  # for now don't handle exception events
        elif event == 'line':
            self.stats.event_line +=1                       # for now don't handle line events
        else:
            self.stats.event_unknown += 1

        return self.trace_calls

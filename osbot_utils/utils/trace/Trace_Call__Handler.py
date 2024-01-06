import linecache

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.trace.Trace_Call__Config import Trace_Call__Config

DEFAULT_ROOT_NODE_NODE_TITLE = 'Trace Session'

class Trace_Call__Handler(Kwargs_To_Self):
    call_index : int
    stack      : list
    config     : Trace_Call__Config


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trace_title  = self.config.title or DEFAULT_ROOT_NODE_NODE_TITLE                           # Title for the trace
        self.stack        = [self.new_stack_node(self.trace_title, self.call_index)]


    def new_stack_node(self, title, call_index):
        return { "name"       : title      ,
                 "children"   : []         ,
                 "call_index" : call_index }

    def add_trace_ignore(self, value):
        self.config.trace_ignore_start_with.append(value)
        return

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
        instance = frame.f_locals.get("self", None)                                                           # Get instance if available
        try:
            class_name = instance.__class__.__name__ if instance else ""
        except Exception:
            class_name = "<unavailable>"
        if class_name:
            full_name = f"{module}.{class_name}.{func_name}"
        else:
            full_name = f"{module}.{func_name}"
        return full_name

    def create_stack_node(self, frame, full_name, source_code, call_index):

        new_node = { "name"                : full_name            ,
                     "children"            : []                   ,
                     'call_index'          :  call_index          ,
                     'source_code'         : source_code.get('source_code'          ),
                     'source_code_caller'  : source_code.get('source_code_caller'   ),
                     'source_code_location': source_code.get('source_code_location' ) }     # Create a new node for this call
        if self.config.capture_locals:
            new_node['locals'] = frame.f_locals
        return new_node

    def add_node(self, frame, new_node):
        self.stack[-1]["children"].append(new_node)         # Insert the new node into the stack
        self.stack.append(new_node)                         # Push the new node to the stack
        frame.f_locals['__trace_depth'] = len(self.stack)   # Store the depth in frame locals

    def handle_event__call(self, frame):
        code        = frame.f_code                                                      # Get code object from frame
        func_name   = code.co_name                                                      # Get function name
        module      = frame.f_globals.get("__name__", "")                               # Get module name

        capture     = self.should_capture(module, func_name)

        if capture:
            self.call_index += 1  # Increment the call index
            source_code      = self.map_source_code(frame)
            full_name        = self.map_full_name(frame, module, func_name)
            new_node         =  self.create_stack_node(frame, full_name, source_code, self.call_index)

            self.add_node(frame, new_node)


    def handle_event__return(self, frame):
        if '__trace_depth' in frame.f_locals and frame.f_locals['__trace_depth'] == len(self.stack):
            self.stack.pop()  # Pop the stack on return if corresponding call was captured

    def trace_calls(self, frame, event, arg):
        if event == 'call':
            self.handle_event__call(frame)
        elif event == 'return':
            self.handle_event__return(frame)
        return self.trace_calls
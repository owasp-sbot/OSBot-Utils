import linecache

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Trace_Call__Handler(Kwargs_To_Self):
    call_index                : int = 0
    title                     : str
    stack                     : list
    capture_locals            : bool = True
    trace_capture_all         : bool
    trace_capture_source_code : bool
    trace_capture_start_with  : list
    trace_ignore_internals    : bool = True
    trace_ignore_start_with   : list



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trace_title                 = self.title or 'Trace Session'                            # Title for the trace
        self.stack = [{"name": self.trace_title, "children": [],
                       "call_index": self.call_index}]  # Call stack information
        #self.trace_capture_start_with = self.trace_capture_start_with or []
        #self.trace_ignore_start_with  = self.trace_ignore_start_with  or []

    def add_trace_ignore(self, value):
        self.trace_ignore_start_with.append(value)
        return

    def trace_calls(self, frame, event, arg):
        if event == 'call':
            code        = frame.f_code                                                      # Get code object from frame
            func_name   = code.co_name                                                      # Get function name
            module      = frame.f_globals.get("__name__", "")                               # Get module name
            capture     = False

            if self.trace_capture_all:
                capture = True
            else:
                for item in self.trace_capture_start_with:                                  # Check if the module should be captured
                    if module.startswith(item):
                        capture = True
                        break
            if self.trace_ignore_internals and func_name.startswith('_'):                   # Skip private functions
                capture = False

            for item in self.trace_ignore_start_with:                                       # Check if the module should be ignored
                if module.startswith(item):
                    capture = False
                    break

            if capture:
                if self.trace_capture_source_code:
                    filename    = frame.f_code.co_filename
                    lineno      = frame.f_lineno
                    source_code = linecache.getline(filename, lineno).strip()

                    caller_filename      = frame.f_back.f_code.co_filename
                    caller_lineno        = frame.f_back.f_lineno
                    source_code_caller   = linecache.getline(caller_filename, caller_lineno).strip()
                    source_code_location = f'{filename}:{lineno}'
                else:
                    source_code          = ''
                    source_code_caller   = ''
                    source_code_location = ''


                instance = frame.f_locals.get("self", None)                                                           # Get instance if available
                try:
                    class_name = instance.__class__.__name__ if instance else ""
                except Exception:
                    class_name = "<unavailable>"
                full_name = f"{module}.{class_name}.{func_name}" if class_name else f"{module}.{func_name}"
                if "utils.for_testing.Trace_Call.Trace_Call" in full_name:                                          # Skip internal calls to this class
                    return self.trace_calls
                self.call_index += 1                                                                                # Increment the call index
                new_node = { "name"                : full_name            ,
                             "children"            : []                   ,
                             'call_index'          : self.call_index      ,
                             #'locals'              : locals               ,
                             'source_code'         : source_code          ,
                             'source_code_caller'  : source_code_caller   ,
                             'source_code_location': source_code_location }     # Create a new node for this call
                if self.capture_locals:
                    new_node['locals'] = frame.f_locals
                self.stack[-1]["children"].append(new_node)                                                         # Insert the new node into the stack
                self.stack.append(new_node)                                                                         # Push the new node to the stack
                frame.f_locals['__trace_depth'] = len(self.stack)                                                   # Store the depth in frame locals
        elif event == 'return':
            if '__trace_depth' in frame.f_locals and frame.f_locals['__trace_depth'] == len(self.stack):
                self.stack.pop()                                                                                    # Pop the stack on return if corresponding call was captured

        return self.trace_calls
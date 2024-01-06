import linecache
import sys
from functools import wraps

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.trace.Trace_Call__Handler import Trace_Call__Handler
from osbot_utils.utils.trace.Trace_Call__Print_Traces import Trace_Call__Print_Traces
from osbot_utils.utils.trace.Trace_Call__View_Model import Trace_Call__View_Model


def trace_calls(title=None, print=True, locals=False, source_code=False, ignore=None, include=None,
                max_string=None, show_types=False, show_caller=False, show_parent=False, show_path=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with Trace_Call(title=title, print_on_exit=print, print_locals=locals,
                            capture_source_code=source_code, ignore_start_with=ignore,
                            capture_start_with=include, print_max_string_length=max_string,
                            show_parent_info=show_types, show_method_parent=show_parent,
                            show_caller=show_caller, show_source_code_path=show_path):
                return func(*args, **kwargs)
        return wrapper
    return decorator

class Trace_Call(Kwargs_To_Self):
    title                   = None
    capture_source_code     = False
    ignore_start_with       = None
    capture_start_with      = None
    print_on_exit           = False
    print_locals            = False
    print_max_string_length = 100
    show_parent_info        = True
    show_caller             = False
    show_method_parent      = False
    show_source_code_path   = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        handler_kwargs = dict(title=self.title)
        self.trace_call_handler                             = Trace_Call__Handler(**handler_kwargs)
        self.trace_call_view_model                          = Trace_Call__View_Model()
        self.trace_call_print_traces                        = Trace_Call__Print_Traces()
        self.trace_call_print_traces.print_traces_on_exit   = self.print_on_exit
        self.trace_call_handler.trace_capture_start_with    = self.capture_start_with or []
        self.trace_call_handler.trace_ignore_start_with     = self.ignore_start_with  or []
        self.stack              = self.trace_call_handler.stack
        self.prev_trace_function         = None                                                # Stores the previous trace function


    def __enter__(self):
        self.start()                                                                        # Start the tracing
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()                                                                         # Stop the tracing
        self.process_data()        # Process the data captured
        if self.trace_call_print_traces.print_traces_on_exit:
            view_model                = self.trace_call_view_model.view_model
            trace_capture_source_code = self.trace_call_handler.trace_capture_source_code
            self.trace_call_print_traces.print_traces(view_model, trace_capture_source_code)                                                             # Print the traces if the flag is set


    # todo: see if this used or needed
    # def trace(self, title):
    #     self.trace_call_handler.trace_title = title
    #     self.stack.append({"name": title, "children": [],"call_index": self.trace_call_handler.call_index})
    #     return self







    def process_data(self):
        self.trace_call_view_model.create(self.stack)                                # Process data to create the view model
        self.trace_call_view_model.fix_view_mode()                                   # Fix the view mode for the last node

    def start(self):
        self.prev_trace_function = sys.gettrace()
        sys.settrace(self.trace_call_handler.trace_calls)                                                      # Set the new trace function

    def stop(self):
        sys.settrace(self.prev_trace_function)                                              # Restore the previous trace function


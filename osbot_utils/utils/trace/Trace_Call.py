import linecache
import sys
from functools import wraps

from osbot_utils.base_classes.Kwargs_To_Self            import Kwargs_To_Self
from osbot_utils.utils.trace.Trace_Call__Config         import Trace_Call__Config
from osbot_utils.utils.trace.Trace_Call__Handler        import Trace_Call__Handler
from osbot_utils.utils.trace.Trace_Call__Print_Traces   import Trace_Call__Print_Traces
from osbot_utils.utils.trace.Trace_Call__View_Model     import Trace_Call__View_Model


def trace_calls(title=None, print=True, locals=False, source_code=False, ignore=None, include=None,
                max_string=None, show_types=False, show_caller=False, show_parent=False, show_path=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            config_kwargs = dict(title=title, print_on_exit=print, print_locals=locals,
                                 capture_source_code=source_code, ignore_start_with=ignore,
                                 capture_start_with=include, print_max_string_length=max_string,
                                 show_parent_info=show_types, show_method_parent=show_parent,
                                 show_caller=show_caller, show_source_code_path=show_path)

            config = Trace_Call__Config(**config_kwargs)
            with Trace_Call(config=config):
                result = func(*args, **kwargs)
                return result
        return wrapper
    return decorator

class Trace_Call(Kwargs_To_Self):

    config : Trace_Call__Config

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.trace_call_handler                             = Trace_Call__Handler     (config=self.config)
        self.trace_call_view_model                          = Trace_Call__View_Model  ()
        self.trace_call_print_traces                        = Trace_Call__Print_Traces(config=self.config)
        self.trace_call_print_traces.print_traces_on_exit   = self.config.print_on_exit
        self.trace_call_handler.config.trace_capture_start_with    = self.config.capture_start_with or []
        self.trace_call_handler.config.trace_ignore_start_with     = self.config.ignore_start_with  or []
        self.stack                                          = self.trace_call_handler.stack
        self.prev_trace_function                            = None                                                # Stores the previous trace function


    def __enter__(self):
        self.start()                                                                        # Start the tracing
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()                                                                         # Stop the tracing
        if self.config.process_data:

            self.create_view_model()        # Process the data captured
            if self.trace_call_print_traces.config.print_on_exit:
                view_model                = self.trace_call_view_model.view_model
                self.trace_call_print_traces.print_traces(view_model)


    def create_view_model(self):
        self.trace_call_view_model.create(self.stack)                                       # Process data to create the view model

    def start(self):
        self.prev_trace_function = sys.gettrace()
        sys.settrace(self.trace_call_handler.trace_calls)                                   # Set the new trace function

    def stop(self):
        sys.settrace(self.prev_trace_function)                                              # Restore the previous trace function


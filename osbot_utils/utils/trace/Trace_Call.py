import linecache
import sys
from functools import wraps

from osbot_utils.base_classes.Kwargs_To_Self            import Kwargs_To_Self
from osbot_utils.utils.trace.Trace_Call__Config import Trace_Call__Config, PRINT_MAX_STRING_LENGTH
from osbot_utils.utils.trace.Trace_Call__Handler        import Trace_Call__Handler
from osbot_utils.utils.trace.Trace_Call__Print_Traces   import Trace_Call__Print_Traces
from osbot_utils.utils.trace.Trace_Call__View_Model     import Trace_Call__View_Model


def trace_calls(title=None, print=True, show_locals=False, source_code=False, ignore=None, include=None,
                max_string=None, show_types=False, show_caller=False, show_class=False, show_path=False,
                show_duration=False, duration_bigger_than=0, contains=None, ignore_internals=True,
                extra_data=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            config_kwargs = dict(title=title, print_on_exit=print, print_locals=show_locals,
                                 capture_source_code=source_code, ignore_start_with=ignore,
                                 capture_start_with=include, print_max_string_length=max_string,
                                 show_parent_info=show_types, show_method_class=show_class,
                                 show_caller=show_caller, show_source_code_path=show_path,
                                 capture_duration=show_duration, print_duration= show_duration,
                                 with_duration_bigger_than=duration_bigger_than,
                                 trace_capture_contains=contains, trace_ignore_internals=ignore_internals,
                                 capture_extra_data=extra_data)

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

        self.trace_call_handler                                 = Trace_Call__Handler     (config=self.config)
        self.trace_call_view_model                              = Trace_Call__View_Model  ()
        self.trace_call_print_traces                            = Trace_Call__Print_Traces(config=self.config)
        self.config.print_on_exit                               = self.config.print_on_exit
        self.config.trace_capture_start_with                    = self.config.capture_start_with       or []          # todo add a better way to set these to [] when then value is null
        self.config.trace_ignore_start_with                     = self.config.ignore_start_with        or []          #      probablty better done inside Kwargs_To_Self since it doesn't make sense for lists or dicts to have None value
        self.config.trace_capture_contains                      = self.config.trace_capture_contains   or []          #      and None will be quite common since we can use [] on method's params
        self.config.print_max_string_length                     = self.config.print_max_string_length  or PRINT_MAX_STRING_LENGTH
        self.stack                                              = self.trace_call_handler.stack
        self.prev_trace_function                                = None                                                # Stores the previous trace function


    def __enter__(self):
        self.start()                                                                        # Start the tracing
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()                                                                         # Stop the tracing
        # Process the data captured
        if self.trace_call_print_traces.config.print_on_exit:
            self.print()

    def capture_all(self):
        self.config.trace_capture_all = True
        return self

    def create_view_model(self):
        return self.trace_call_view_model.create(self.stack)

    def print(self):
        view_model = self.create_view_model()
        self.trace_call_print_traces.print_traces(view_model)
        return view_model

    def start(self):
        self.trace_call_handler.stack.add_node(title=self.trace_call_handler.trace_title)
        self.prev_trace_function = sys.gettrace()
        sys.settrace(self.trace_call_handler.trace_calls)                                   # Set the new trace function

    def stop(self):
        sys.settrace(self.prev_trace_function)                                              # Restore the previous trace function
        self.stack.empty_stack()

    def stats(self):
        return self.trace_call_handler.stats

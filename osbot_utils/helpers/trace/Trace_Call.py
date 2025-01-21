import linecache
import sys
import threading
from functools                                              import wraps
from osbot_utils.base_classes.Kwargs_To_Self                import Kwargs_To_Self
from osbot_utils.helpers.trace.Trace_Call__Config           import Trace_Call__Config, PRINT_MAX_STRING_LENGTH
from osbot_utils.helpers.trace.Trace_Call__Handler          import Trace_Call__Handler
from osbot_utils.helpers.trace.Trace_Call__Print_Lines      import Trace_Call__Print_Lines
from osbot_utils.helpers.trace.Trace_Call__Print_Traces     import Trace_Call__Print_Traces
from osbot_utils.helpers.trace.Trace_Call__View_Model       import Trace_Call__View_Model
from osbot_utils.testing.Stdout                             import Stdout
from osbot_utils.utils.Str                                  import ansi_to_text


def trace_calls(title         = None , print_traces = True , show_locals    = False, source_code          = False ,
                ignore        = None , include      = None , show_path      = False, duration_bigger_than = 0     ,
                trace_depth   = 0    , max_string   = None , show_types     = False, show_duration        = False , # show_caller    = False     ,         # todo: add back when show_caller is working again
                show_class    = False, contains     = None , show_internals = False, enabled              = True  ,
                extra_data    = False, show_lines   = False, print_lines    = False, show_types_padding   = None  , duration_padding=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            config_kwargs = dict(title=title, print_traces_on_exit=print_traces, print_locals=show_locals,
                                 capture_locals = show_locals,
                                 trace_capture_source_code=source_code, ignore_start_with=ignore,
                                 trace_capture_start_with=include, print_max_string_length=max_string,
                                 show_parent_info=show_types, show_method_class=show_class,
                                 show_source_code_path=show_path,
                                 capture_duration=show_duration, print_duration= show_duration,
                                 with_duration_bigger_than=duration_bigger_than,
                                 trace_capture_contains=contains, trace_show_internals=show_internals,
                                 capture_extra_data=extra_data,
                                 print_padding_parent_info= show_types_padding, print_padding_duration=duration_padding,
                                 print_lines_on_exit=print_lines, trace_enabled=enabled,
                                 trace_capture_lines=show_lines or print_lines,
                                 trace_up_to_depth=trace_depth)

            config = (Trace_Call__Config().update_from_kwargs (**config_kwargs))

            with Trace_Call(config=config):
                result = func(*args, **kwargs)
                return result
        return wrapper
    return decorator

class Trace_Call(Kwargs_To_Self):

    config             : Trace_Call__Config
    started            : bool
    prev_trace_function: None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.trace_call_handler                                 = Trace_Call__Handler     (config=self.config)
        self.trace_call_print_traces                            = Trace_Call__Print_Traces(config=self.config)
        self.trace_call_view_model                              = Trace_Call__View_Model  ()
        self.config.print_traces_on_exit                        = self.config.print_traces_on_exit
        #self.config.trace_capture_start_with                    = self.config.capture_start_with       or []          # todo add a better way to set these to [] when then value is null
        self.config.trace_ignore_start_with                     = self.config.ignore_start_with        or []          #      probablty better done inside Kwargs_To_Self since it doesn't make sense for lists or dicts to have None value
        self.config.trace_capture_contains                      = self.config.trace_capture_contains   or []          #      and None will be quite common since we can use [] on method's params
        self.config.print_max_string_length                     = self.config.print_max_string_length  or PRINT_MAX_STRING_LENGTH
        self.stack                                              = self.trace_call_handler.stack
        self.trace_on_thread__data                              = {}
        #self.prev_trace_function                                = None                                                # Stores the previous trace function


    def __enter__(self):
        return self.on_enter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.on_exit()

    def on_enter(self):
        if self.config.trace_enabled:
            self.start()  # Start the tracing
        return self

    def on_exit(self):
        if self.config.trace_enabled:
            self.stop()  # Stop the tracing
            if self.config.print_traces_on_exit:
                self.print()
            if self.config.print_lines_on_exit:
                self.print_lines()

    def capture_all(self):
        self.config.trace_capture_all = True
        return self

    def view_data(self):
        return self.trace_call_view_model.create(self.stack)

    def print(self):
        view_model = self.view_data()
        self.trace_call_print_traces.print_traces(view_model)
        #self.print_lines()
        return view_model

    def print_to_str(self):
        with Stdout() as stdout:
            self.print()
        trace_data = ansi_to_text(stdout.value())
        return trace_data


    def print_lines(self):
        print()
        view_model = self.view_data()
        print_lines = Trace_Call__Print_Lines(config=self.config, view_model=view_model)
        print_lines.print_lines()

    def start(self):
        self.trace_call_handler.stack.add_node(title=self.trace_call_handler.config.title)
        self.prev_trace_function = sys.gettrace()
        self.started             = True                                                         # set this here so that it does show in the trace
        sys.settrace(self.trace_call_handler.trace_calls)                                       # Set the new trace function

    def start__on_thread(self, root_node=None):
        if sys.gettrace() is None:
            current_thread    = threading.current_thread()
            thread_sys_trace = sys.gettrace()
            thread_name       = current_thread.name
            thread_id         = current_thread.native_id
            thread_nodes      = []
            thread_data       = dict(thread_name      = thread_name     ,
                                     thread_id        = thread_id       ,
                                     thread_nodes     = thread_nodes    ,
                                     thread_sys_trace = thread_sys_trace)
            title = f"Thread: {thread_name} ({thread_id})"
            thread_node__for_title = self.trace_call_handler.stack.add_node(title=title)         # Add node with name of Thread

            if root_node:                                                                   # Add node with name of node
                thread_node__for_root = self.trace_call_handler.stack.add_node(root_node)
                thread_nodes.append(thread_node__for_root)
            thread_nodes.append(thread_node__for_title)
            sys.settrace(self.trace_call_handler.trace_calls)
            self.trace_on_thread__data[thread_id] = thread_data


    def stop(self):
        if self.started:
            sys.settrace(self.prev_trace_function)                                              # Restore the previous trace function
            self.stack.empty_stack()
            self.started = False

    def stop__on_thread(self):
        current_thread = threading.current_thread()
        thread_id      = current_thread.native_id
        thread_data    = self.trace_on_thread__data.get(thread_id)
        if thread_data:                                             # if there trace_call set up in the current thread
            thread_sys_trace = thread_data.get('thread_sys_trace')
            thread_nodes     = thread_data.get('thread_nodes')
            for thread_node in thread_nodes:                        # remove extra nodes added during start__on_thread
                self.trace_call_handler.stack.pop(thread_node)
            sys.settrace(thread_sys_trace)                          # restore previous sys.trace value
            del self.trace_on_thread__data[thread_id]

    def stats(self):
        return self.trace_call_handler.stats

    def stats_data(self):
        return self.trace_call_handler.stats.raw_call_stats


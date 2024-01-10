from osbot_utils.utils.Dev import pprint

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

PRINT_MAX_STRING_LENGTH = 100

class Trace_Call__Config(Kwargs_To_Self):
    title                      : str
    capture_locals             : bool = True
    capture_duration           : bool
    capture_extra_data         : bool
    capture_frame              : bool = True
    capture_frame_stats        : bool
    deep_copy_locals           : bool
    trace_capture_lines        : bool
    ignore_start_with          : list
    print_duration             : bool
    print_max_string_length    : int  = PRINT_MAX_STRING_LENGTH
    print_locals               : bool
    print_traces_on_exit       : bool
    print_lines_on_exit        : bool
    show_parent_info           : bool = True
    show_caller                : bool
    show_method_class          : bool
    show_source_code_path      : bool
    trace_capture_all          : bool
    trace_capture_source_code  : bool
    trace_capture_start_with   : list
    trace_capture_contains     : list
    trace_enabled              : bool = True
    trace_show_internals       : bool
    trace_ignore_start_with    : list
    with_duration_bigger_than  : bool

    def all(self, print_traces=True):
        self.trace_capture_all    = True
        self.print_traces_on_exit = print_traces

    def capture(self, starts_with=None, contains=None, ignore=None):
        if starts_with:
            if type(starts_with) is str:
                starts_with = [starts_with]
            self.trace_capture_start_with = starts_with
        if contains:
            if type(contains) is str:
                contains = [contains]
            self.trace_capture_contains = contains
        if ignore:
            if type(ignore) is str:
                ignore = [ignore]
            self.ignore_start_with = ignore
        self.print_traces_on_exit = True

    def locals(self):
        self.capture_locals = True
        self.print_locals   = True

    def lines(self, print_traces=True, print_lines=True):
        self.trace_capture_lines  = True
        self.print_traces_on_exit = print_traces
        self.print_lines_on_exit  = print_lines

    def print_config(self):
        pprint(self.__locals__())
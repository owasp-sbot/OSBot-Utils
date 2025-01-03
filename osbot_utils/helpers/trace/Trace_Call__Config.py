
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Dev              import pprint                   # todo: fix test requirement of mock to use this method


PRINT_MAX_STRING_LENGTH    = 100
PRINT_PADDING__DURATION    = 100
PRINT_PADDING_PARENT_INFO  = 60

class Trace_Call__Config(Type_Safe):
    capture_locals             : bool = False
    capture_duration           : bool
    capture_extra_data         : bool
    capture_frame              : bool = True
    capture_frame_stats        : bool
    deep_copy_locals           : bool
    ignore_start_with          : list
    print_padding_duration     : int = PRINT_PADDING__DURATION
    print_padding_parent_info  : int = PRINT_PADDING_PARENT_INFO
    print_duration             : bool
    print_max_string_length    : int  = PRINT_MAX_STRING_LENGTH
    print_locals               : bool
    print_traces_on_exit       : bool
    print_lines_on_exit        : bool
    show_parent_info           : bool = False
    show_caller                : bool
    show_method_class          : bool = True
    show_source_code_path      : bool
    title                      : str
    trace_capture_all          : bool
    trace_capture_source_code  : bool
    trace_capture_start_with   : list
    trace_capture_contains     : list
    trace_enabled              : bool = True
    trace_ignore_start_with    : list
    trace_ignore_contains      : list
    trace_capture_lines        : bool
    trace_show_internals       : bool
    trace_up_to_depth          : int
    with_duration_bigger_than  : float

    def __init__(self, **wargs):
        super().__init__(**wargs)
        #self.locked()

    def all(self, up_to_depth=0, print_traces=True):
        self.trace_capture_all    = True
        self.print_traces_on_exit = print_traces
        self.trace_up_to_depth    = up_to_depth
        return self

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
        return self

    def duration(self, bigger_than=0, padding=PRINT_PADDING__DURATION):
        self.capture_duration          = True
        self.print_duration            = True
        self.print_padding_duration          = padding
        self.with_duration_bigger_than = bigger_than
        return self

    def locals(self):
        self.capture_locals = True
        self.print_locals   = True
        return self

    def lines(self, print_traces=True, print_lines=True):
        self.trace_capture_lines  = True
        self.print_traces_on_exit = print_traces
        self.print_lines_on_exit  = print_lines
        return self

    def print_config(self):
        pprint(self.__locals__())
        return self

    def print_on_exit(self, value=True):
        self.print_traces_on_exit = value
        return self

    def up_to_depth(self, depth):
        self.trace_up_to_depth = depth
        return self
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

PRINT_MAX_STRING_LENGTH = 100

class Trace_Call__Config(Kwargs_To_Self):
    title                      : str
    capture_locals             : bool = True
    capture_duration           : bool
    capture_extra_data         : bool
    capture_frame              : bool = True
    capture_frame_stats        : bool
    trace_capture_lines        : bool
    capture_start_with         : list
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
    trace_show_internals       : bool
    trace_ignore_start_with    : list
    with_duration_bigger_than  : bool
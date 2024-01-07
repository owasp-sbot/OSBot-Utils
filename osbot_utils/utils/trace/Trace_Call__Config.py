from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

PRINT_MAX_STRING_LENGTH = 100

class Trace_Call__Config(Kwargs_To_Self):
    title                     : str
    capture_locals            : bool = True
    capture_frame             : bool = True
    capture_source_code       : bool
    ignore_start_with         : list
    capture_start_with        : list
    print_on_exit             : bool
    print_locals              : bool
    print_max_string_length   : int  = PRINT_MAX_STRING_LENGTH
    process_data              : bool = True
    show_parent_info          : bool = True
    show_caller               : bool
    show_method_parent        : bool
    show_source_code_path     : bool
    trace_capture_all         : bool
    trace_capture_source_code : bool
    trace_capture_start_with  : list
    trace_ignore_internals    : bool = True
    trace_ignore_start_with   : list
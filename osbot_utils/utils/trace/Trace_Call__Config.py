from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Trace_Call__Config(Kwargs_To_Self):
    title                   : str
    capture_locals          : bool  = True
    capture_source_code     : bool
    ignore_start_with       : list
    capture_start_with      : list
    print_on_exit           : bool
    print_locals            : bool
    print_max_string_length : int   = 100
    process_data            : bool  = True
    show_parent_info        : bool  = True
    show_caller             : bool
    show_method_parent      : bool
    show_source_code_path   : bool
    trace_capture_all         : bool
    trace_capture_source_code : bool
    trace_capture_start_with  : list
    trace_ignore_internals    : bool = True
    trace_ignore_start_with   : list
    title                     : str
    capture_source_code       : bool
    ignore_start_with         : list
    capture_start_with        : list
    print_on_exit             : bool
    print_locals              : bool
    #print_max_string_length = 100
    ##show_parent_info        = False
    #show_caller             = False
    show_method_parent        : bool
    show_source_code_path     : bool
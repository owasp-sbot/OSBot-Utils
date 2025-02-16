from osbot_utils.type_safe.Type_Safe import Type_Safe

# todo: this needs a good clean up and refactoring
class Flow_Run__Config(Type_Safe):
    add_task_to_self          : bool = True
    log_to_console            : bool = False
    log_to_memory             : bool = True
    logging_enabled           : bool = True
    print_logs                : bool = False
    print_none_return_value   : bool = False
    print_finished_message    : bool = False
    print_error_stack_trace   : bool = False
    raise_flow_error          : bool = True
    flow_data__capture_events : bool = False


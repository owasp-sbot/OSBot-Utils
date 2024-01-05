import linecache
import sys
from functools import wraps

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.Dev import pformat, pprint
from osbot_utils.utils.trace.Trace_Call__Handler import Trace_Call__Handler
from osbot_utils.utils.trace.Trace_Call__View_Model import Trace_Call__View_Model

# ANSI escape codes     #todo: refactor this color support to OSBot_Utils
dark_mode = False

if dark_mode:
    BOLD    = "\033[1m\033[48;2;30;31;34m\033[38;2;255;255;255m"        # dark mode
    BLUE    = "\033[48;2;30;31;34m\033[94m"
    GREEN   = "\033[48;2;30;31;34m\033[92m"
    OLIVE   = "\033[48;2;30;31;34m\033[38;2;118;138;118m"
    GREY    = "\033[48;2;30;31;34m\033[90m"
else:
    BOLD  = "\033[1m"
    BLUE  = "\033[94m"
    GREEN = "\033[92m"
    OLIVE = "\033[38;2;118;138;118m"
    GREY  = "\033[90m"

RED     = "\033[91m"

RESET   = "\033[0m"

text_blue       = lambda text: f"{BLUE}{text}{RESET}"
text_bold       = lambda text: f"{BOLD}{text}{RESET}"
text_bold_red   = lambda text: f"{BOLD}{RED}{text}{RESET}"
text_bold_green = lambda text: f"{BOLD}{GREEN}{text}{RESET}"
text_bold_blue  = lambda text: f"{BOLD}{BLUE}{text}{RESET}"
text_green      = lambda text: f"{GREEN}{text}{RESET}"
text_grey       = lambda text: f"{GREY}{text}{RESET}"
text_olive      = lambda text: f"{OLIVE}{text}{RESET}"
text_red        = lambda text: f"{RED}{text}{RESET}"
text_none       = lambda text: f"{text}"
text_color      = lambda text, color: f"{color}{text}{RESET}"

MAX_STRING_LENGTH = 100

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
    print_on_exit           = False
    print_locals            = False
    capture_source_code     = False
    ignore_start_with       = None
    capture_start_with      = None
    print_max_string_length = None
    show_parent_info        = True
    show_caller             = False
    show_method_parent      = False
    show_source_code_path   = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        handler_kwargs = dict(title=self.title)
        self.trace_call_handler     = Trace_Call__Handler(**handler_kwargs)
        self.trace_call_view_model  = Trace_Call__View_Model()


        self.trace_call_handler.trace_capture_start_with    = self.capture_start_with or []
        self.trace_call_handler.trace_ignore_start_with     = self.ignore_start_with  or []
        self.stack              = self.trace_call_handler.stack
        self.prev_trace_function         = None                                                # Stores the previous trace function
        self.print_show_method_parent    = self.show_method_parent                             # todo: refactor these print_* variables (now that we have the nice setup created by Kwargs_To_Self)
        self.print_show_caller           = self.show_caller
        self.print_traces_on_exit        = self.print_on_exit                                               # Flag for printing traces when exiting
        self.print_show_parent_info      = self.show_parent_info                                            # Flag for showing parent info when printing
        self.print_show_locals           = self.print_locals
        self.print_show_source_code_path = self.show_source_code_path
        self.print_max_string_length     = self.print_max_string_length or MAX_STRING_LENGTH

    def __enter__(self):
        self.start()                                                                        # Start the tracing
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()                                                                         # Stop the tracing
        self.process_data()                                                                 # Process the data captured
        if self.print_traces_on_exit:
            self.print_traces()                                                             # Print the traces if the flag is set


    # todo: see if this used or needed
    # def trace(self, title):
    #     self.trace_call_handler.trace_title = title
    #     self.stack.append({"name": title, "children": [],"call_index": self.trace_call_handler.call_index})
    #     return self



    def formatted_local_data(self, local_data, formatted_line):
        if local_data:
            formatted_data = {}
            max_key_length = 0  # Variable to store the length of the longest key

            # First pass to format data and find the length of the longest key
            for key, value in local_data.items():
                if key.startswith('_'):                                                 # don't show internal methods
                    continue
                # Convert objects to their type name
                if isinstance(value, dict):
                    value = pformat(value)                                                  # convert dicts to string (so that they are impacted by self.self.print_max_string_length)
                if not isinstance(value, (int, float, bool, str, dict)):
                    formatted_data[key] = (type(value).__name__, BLUE)
                elif isinstance(value, str) and len(value) > self.print_max_string_length:
                    formatted_data[key] = (value[:self.print_max_string_length] + "...", GREEN)    # Trim large strings
                else:
                    formatted_data[key] = (value, GREEN)

                # Update the maximum key length
                if len(key) > max_key_length:
                    max_key_length = len(key)

            def format_multiline(value, left_padding):
                lines = str(value).split('\n')
                indented_lines = [lines[0]] + [" " * (left_padding +1) + line for line in lines[1:]]
                return '\n'.join(indented_lines)

            # Second pass to print the keys and values aligned
            padding = " " * len(formatted_line)
            for key, (value, color) in formatted_data.items():
                # Calculate the number of spaces needed for alignment
                spaces = " " * (max_key_length - len(key))
                var_name = f"{padding}       🔖 {key}{spaces} = "
                value = format_multiline(value, len(var_name))
                print(f'{var_name}{color}{value}{RESET}')

    def print_traces(self):
        view_model = self.trace_call_view_model.view_model
        print()
        print("--------- CALL TRACER ----------")
        print(f"Here are the {len(view_model)} traces captured\n")
        for idx, item in enumerate(view_model):
            prefix               = item['prefix']
            tree_branch          = item['tree_branch']
            emoji                = item['emoji']
            method_name          = item['method_name']
            method_parent        = item['method_parent']
            parent_info          = item['parent_info']
            locals               = item.get('locals'            , {} )
            source_code          = item.get('source_code'       , '' )
            source_code_caller   = item.get('source_code_caller', '' )
            source_code_location = item.get('source_code_location') or ''

            if self.print_show_method_parent:
                method_name = f'{text_olive(method_parent)}.{text_bold(method_name)}'
                self.print_show_parent_info = False         # these are not compatible

            node_text          = source_code or method_name
            formatted_line     = f"{prefix}{tree_branch}{emoji} {node_text}"
            padding            = " " * (60 - len(formatted_line))

            if self.trace_call_handler.trace_capture_source_code:
                if self.print_show_caller:
                    print(f"{prefix}{tree_branch}🔼️{text_bold(source_code_caller)}")
                    print(f"{prefix}{tree_branch}➡️{emoji} {text_grey(node_text)}")
                else:
                    print(f"{prefix}{tree_branch}➡️{emoji} {text_bold(node_text)}")

                # if self.print_show_source_code_path:
                #
                #     raise Exception("to implement path_source_code_root")
                    # path_source_code_root = ...
                    #
                    # print(f" " * len(prefix), end="         ")
                    # fixed_source_code_location = source_code_location.replace(path_source_code_root, '')
                    # print(fixed_source_code_location)
            else:
                if idx == 0 or self.print_show_parent_info is False:                            # Handle the first line and conditional parent info differently
                    print(f"{text_bold(formatted_line)}")                                                  # Don't add "|" to the first line
                else:
                    print(f"{text_bold(formatted_line)}{padding} {parent_info}")

            if self.print_show_locals:
            #     formatted_line = formatted_line.replace('│', ' ')
            #     print(f"{text_bold(formatted_line)}")
                 self.formatted_local_data(locals, f'{prefix}{tree_branch}')
            # else:



    def process_data(self):
        self.trace_call_view_model.create(self.stack)                                # Process data to create the view model
        self.trace_call_view_model.fix_view_mode()                                   # Fix the view mode for the last node

    def start(self):
        self.prev_trace_function = sys.gettrace()
        sys.settrace(self.trace_call_handler.trace_calls)                                                      # Set the new trace function

    def stop(self):
        sys.settrace(self.prev_trace_function)                                              # Restore the previous trace function


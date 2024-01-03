import linecache
import sys
from functools import wraps

from osbot_utils.utils.Dev import pformat

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

class Trace_Call:
    def __init__(self, title=None, print_on_exit=False, print_locals=False, capture_source_code=False, ignore_start_with=None,
                       capture_start_with=None, print_max_string_length=None, show_parent_info=True, show_caller=False,
                       show_method_parent=False, show_source_code_path=False):
        self.prev_trace_function         = None                                                # Stores the previous trace function
        self.call_index                  = 0                                                   # Counter for the index of each function call
        self.trace_title                 = title or 'Trace Session'                            # Title for the trace
        self.stack                       = [{"name"      : self.trace_title , "children": [],
                                             "call_index": self.call_index }]                  # Call stack information
        self.view_model                  = []                                                  # Stores the view model data
        self.print_show_method_parent    = show_method_parent
        self.print_show_caller           = show_caller
        self.print_traces_on_exit        = print_on_exit                                               # Flag for printing traces when exiting
        self.print_show_parent_info      = show_parent_info                                            # Flag for showing parent info when printing
        self.print_show_locals           = print_locals
        self.print_show_source_code_path = show_source_code_path
        self.print_max_string_length     = print_max_string_length or MAX_STRING_LENGTH
        self.trace_capture_all           = False
        self.trace_capture_source_code   = capture_source_code
        self.trace_ignore_internals      = True
        self.trace_capture_start_with    = capture_start_with or ['cbr_website_beta']                                # List of starting substrings for modules to trace
        self.trace_ignore_start_with     = ignore_start_with  or []
        #self.view_parents_to_prune      = capture_start_with or ["cbr_website_beta"]                                # List of parent names to prune in the view

    def __enter__(self):
        self.start()                                                                        # Start the tracing
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()                                                                         # Stop the tracing
        self.process_data()                                                                 # Process the data captured
        self.fix_view_mode()                                                                # Fix the view mode for the last node
        if self.print_traces_on_exit:
            self.print_traces()                                                             # Print the traces if the flag is set

    def add_trace_ignore(self, value):
        self.trace_ignore_start_with.append(value)
        return

    def trace(self, title):
        self.trace_title = title
        self.stack.append({"name": title, "children": [],"call_index": self.call_index})
        return self

    def create_view_model(self, json_list, level=0, prefix="", view_model=None):
        if view_model is None:
            view_model = []                                                                 # Initialize view model if None

        for idx, node in enumerate(json_list):                                              # Iterate over each node in the JSON list to populate the view model
            components           = node["name"].split('.')
            locals               = node.get('locals')
            source_code          = node.get('source_code'         )
            source_code_caller   = node.get('source_code_caller'  )
            source_code_location = node.get('source_code_location')
            method_name          = components[-1]
            if len(components) > 1:
                method_parent  = f"{components[-2]}"
            else:
                method_parent  = ""
            if method_name == "__init__":                                                   # Adjust the method_name based on special method names like __init__ and __call__
                method_name = f"{method_parent}.{method_name}"
            elif method_name == "__call__":
                method_name = f"{method_parent}.{method_name}"
            elif method_name == "<module>":
                method_name = f"{method_parent}.{method_name}"

            pruned_parents = [comp for comp in components] #if comp not in self.view_parents_to_prune]    # Remove the parents that are in the prune list
            parent_info = '.'.join(pruned_parents[:-1])

            if level == 0:                                                                  # Handle tree representation at level 0
                emoji = "📦 "
                tree_branch = ""
            else:
                is_last_sibling = (idx == len(json_list) - 1)                               # Check if the node is the last sibling
                tree_branch = "└── " if is_last_sibling else "├── "
                emoji = "🧩️" if not node["children"] else "🔗️"

            view_model.append({ 'prefix'              : prefix               ,
                                'tree_branch'         : tree_branch          ,
                                'emoji'               : emoji                ,
                                'method_name'         : method_name          ,
                                'method_parent'       : method_parent        ,
                                'parent_info'         : parent_info          ,
                                'locals'              : locals               ,
                                'source_code'         : source_code          ,
                                'source_code_caller'  : source_code_caller   ,
                                'source_code_location': source_code_location })
            next_prefix = prefix + ("    " if tree_branch == "└── " else "│   ")            # Calculate the prefix for the next level
            self.create_view_model(node["children"], level + 1, prefix=next_prefix, view_model=view_model)

        return view_model

    # todo: find a way to sync these default values with the ones in the __init__ method
    def default_kwargs(self):
        return dict(title                   = None  ,
                    print_on_exit           = False ,
                    print_locals            = False ,
                    capture_source_code     = False ,
                    ignore_start_with       = None  ,
                    capture_start_with      = None  ,
                    print_max_string_length = None  ,
                    show_parent_info        = True  ,
                    show_caller             = False ,
                    show_method_parent      = False ,
                    show_source_code_path   = False )

    def fix_view_mode(self):
        if len(self.view_model) > 0:
            last_node = self.view_model[-1]                                                 # Get the last node in the view model
            last_node['prefix']      = '└───'                                               # Update the prefix for the last node
            last_node['tree_branch'] = '─── '



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
        print()
        print("--------- CALL TRACER ----------")
        print(f"Here are the {len(self.view_model)} traces captured\n")
        for idx, item in enumerate(self.view_model):
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

            if self.trace_capture_source_code:
                if self.print_show_caller:
                    print(f"{prefix}{tree_branch}🔼️{text_bold(source_code_caller)}")
                    print(f"{prefix}{tree_branch}➡️{emoji} {text_grey(node_text)}")
                else:
                    print(f"{prefix}{tree_branch}➡️{emoji} {text_bold(node_text)}")

                if self.print_show_source_code_path:

                    raise Exception("to implement path_source_code_root")
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
        self.view_model = self.create_view_model(self.stack)                                # Process data to create the view model

    def start(self):
        self.prev_trace_function = sys.gettrace()                                           # Store the current trace function
        sys.settrace(self.trace_calls)                                                      # Set the new trace function

    def stop(self):
        sys.settrace(self.prev_trace_function)                                              # Restore the previous trace function

    def trace_calls(self, frame, event, arg):
        if event == 'call':
            code        = frame.f_code                                                      # Get code object from frame
            func_name   = code.co_name                                                      # Get function name
            module      = frame.f_globals.get("__name__", "")                               # Get module name
            capture     = False
            if self.trace_capture_all:
                capture = True
            else:
                for item in self.trace_capture_start_with:                                  # Check if the module should be captured
                    if module.startswith(item):
                        capture = True
                        break
            if self.trace_ignore_internals and func_name.startswith('_'):                   # Skip private functions
                capture = False

            for item in self.trace_ignore_start_with:                                       # Check if the module should be ignored
                if module.startswith(item):
                    capture = False
                    break

            if capture:
                if self.trace_capture_source_code:
                    filename    = frame.f_code.co_filename
                    lineno      = frame.f_lineno
                    source_code = linecache.getline(filename, lineno).strip()

                    caller_filename      = frame.f_back.f_code.co_filename
                    caller_lineno        = frame.f_back.f_lineno
                    source_code_caller   = linecache.getline(caller_filename, caller_lineno).strip()
                    source_code_location = f'{filename}:{lineno}'
                else:
                    source_code          = ''
                    source_code_caller   = ''
                    source_code_location = ''

                locals = frame.f_locals
                instance = frame.f_locals.get("self", None)                                                           # Get instance if available
                try:
                    class_name = instance.__class__.__name__ if instance else ""
                except Exception:
                    class_name = "<unavailable>"
                full_name = f"{module}.{class_name}.{func_name}" if class_name else f"{module}.{func_name}"
                if "utils.for_testing.Trace_Call.Trace_Call" in full_name:                                          # Skip internal calls to this class
                    return self.trace_calls
                self.call_index += 1                                                                                # Increment the call index
                new_node = { "name"                : full_name            ,
                             "children"            : []                   ,
                             'call_index'          : self.call_index      ,
                             'locals'              : locals               ,
                             'source_code'         : source_code          ,
                             'source_code_caller'  : source_code_caller   ,
                             'source_code_location': source_code_location }     # Create a new node for this call
                self.stack[-1]["children"].append(new_node)                                                         # Insert the new node into the stack
                self.stack.append(new_node)                                                                         # Push the new node to the stack
                frame.f_locals['__trace_depth'] = len(self.stack)                                                   # Store the depth in frame locals
        elif event == 'return':
            if '__trace_depth' in frame.f_locals and frame.f_locals['__trace_depth'] == len(self.stack):
                self.stack.pop()                                                                                    # Pop the stack on return if corresponding call was captured

        return self.trace_calls
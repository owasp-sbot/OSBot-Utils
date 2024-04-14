from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.utils.Dev                          import pformat
from osbot_utils.helpers.trace.Trace_Call__Config   import Trace_Call__Config

# ANSI escape codes     #todo: refactor this color support to separate colors class
dark_mode = False

if dark_mode:
    BOLD       = "\033[1m\033[48;2;30;31;34m\033[38;2;255;255;255m"        # dark mode
    BLUE       = "\033[48;2;30;31;34m\033[94m"
    GREEN      = "\033[48;2;30;31;34m\033[92m"
    LIGHT_GREY = "\033[48;2;30;31;34m\033[38;2;130;130;130m"
    OLIVE      = "\033[48;2;30;31;34m\033[38;2;118;138;118m"
    GREY       = "\033[48;2;30;31;34m\033[90m"

else:
    BOLD  = "\033[1m"
    BLUE  = "\033[94m"
    GREEN = "\033[92m"
    LIGHT_GREY = "\033[38;2;120;120;120m"
    OLIVE = "\033[38;2;138;148;138m" #"\033[38;2;118;138;118m"
    GREY  = "\033[90m"

RED     = "\033[91m"
WHITE   = "\033[97m"
RESET   = "\033[0m"

text_blue       = lambda text: f"{BLUE}{text}{RESET}"
text_bold       = lambda text: f"{BOLD}{text}{RESET}"
text_bold_red   = lambda text: f"{BOLD}{RED}{text}{RESET}"
text_bold_green = lambda text: f"{BOLD}{GREEN}{text}{RESET}"
text_bold_blue  = lambda text: f"{BOLD}{BLUE}{text}{RESET}"
text_green      = lambda text: f"{GREEN}{text}{RESET}"
text_grey       = lambda text: f"{GREY}{text}{RESET}"
text_light_grey = lambda text: f"{BOLD}{LIGHT_GREY}{text}{RESET}"
text_olive      = lambda text: f"{OLIVE}{text}{RESET}"
text_red        = lambda text: f"{RED}{text}{RESET}"
text_white      = lambda text: f"{WHITE}{text}{RESET}"
text_none       = lambda text: f"{text}"
text_color      = lambda text, color: f"{color}{text}{RESET}"



class Trace_Call__Print_Traces(Kwargs_To_Self):

    config: Trace_Call__Config

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def formatted_local_data(self, local_data, formatted_line, emoji = '🔖'):
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
                elif isinstance(value, str) and len(value) > self.config.print_max_string_length:
                    formatted_data[key] = (value[:self.config.print_max_string_length] + "...", GREEN)    # Trim large strings
                else:
                    formatted_data[key] = (value, GREEN)

                # Update the maximum key length
                if len(key) > max_key_length:
                    max_key_length = len(key)

            def format_multiline(value, left_padding):
                lines = str(value).split('\n')
                indented_lines = [lines[0]] + [" " * (left_padding +1) + line for line in lines[1:]]
                return '\n│'.join(indented_lines)

            padding = " " * len(formatted_line)
            for key, (value, color) in formatted_data.items():
                # Calculate the number of spaces needed for alignment
                spaces = " " * (max_key_length - len(key))
                var_name = f"{padding}       {emoji} {text_light_grey(key)}{spaces} = "
                value = format_multiline(value, len(var_name)- len(text_light_grey('')))  # this logic makes sure that the local's values are column aligned
                print(f'│{var_name}{color}{value}{RESET}')

    def print_lines(self, lines, formatted_line):
        if lines:
            padding = " " * len(formatted_line)
            for line in lines:
                index       = line.get('index')
                #func_name   = line.get('func_name')
                #module      = line.get('module')
                event       = line.get('event')
                line        = line.get('line')
                if event == 'call':
                    print(f"{padding}       {text_grey(index):12} {text_bold_green(line)}")
                else:
                    print(f"{padding}       {text_grey(index):12} {text_olive(line)}")

    def print_traces(self, view_model):
        print()
        print("--------- CALL TRACER ----------")
        print(f"Here are the {len(view_model)} traces captured\n")
        for idx, item in enumerate(view_model):
            emoji                = item.get('emoji'             , '' )
            extra_data           = item.get('extra_data'        , {} )
            locals               = item.get('locals'            , {} )
            method_name          = item.get('method_name'       , '' )
            method_parent        = item.get('method_parent'     , '' )
            parent_info          = item.get('parent_info'       , '' )
            prefix               = item.get('prefix'            , '' )
            tree_branch          = item.get('tree_branch'       , '' )
            source_code          = item.get('source_code'       , '' )
            source_code_caller   = item.get('source_code_caller', '' )
            #source_code_location = item.get('source_code_location') or ''

            if self.config.show_method_class:
                if self.config.show_parent_info:
                    method_name = f'{text_olive(parent_info)}.{text_bold(method_name)}'
                else:
                    method_name = f'{text_olive(method_parent)}.{text_bold(method_name)}'


            node_text          = source_code or method_name
            formatted_line     = f"{prefix}{tree_branch}{emoji} {node_text}"
            if self.config.print_duration:
                duration         = item.get('duration',0) * 1000                    # todo: see if this can be optimised with the similar call below
                duration_rounded = round(duration, 3)
                padding_duration = self.config.print_padding_duration - len(formatted_line)
                duration_text    = "{:>{},.3f}ms".format(duration_rounded, padding_duration)
                formatted_line += f' {text_grey(duration_text)} '

            if self.config.with_duration_bigger_than:
                duration = item.get('duration', 0)
                if duration < self.config.with_duration_bigger_than:
                    continue

            if False and self.config.trace_capture_source_code:       # todo: fix show caller funcionality

                if self.config.show_caller:
                    print(f"{prefix}{tree_branch}🔼️{text_bold(source_code_caller)}")
                    print(f"{prefix}{tree_branch}➡️{emoji} {text_grey(node_text)}")
                else:
                    print(f"{prefix}{tree_branch}➡️{emoji} {text_bold(node_text)}")

                # if self.config.show_source_code_path:
                #
                #     raise Exception("to implement path_source_code_root")
                    # path_source_code_root = ...
                    #
                    # print(f" " * len(prefix), end="         ")
                    # fixed_source_code_location = source_code_location.replace(path_source_code_root, '')
                    # print(fixed_source_code_location)
            else:
                if idx == 0 or (self.config.show_parent_info is False or self.config.show_method_class is True):                            # Handle the first line and conditional parent info differently
                    print(f"{text_bold(formatted_line)}")                                                  # Don't add "|" to the first line
                else:
                    padding = " " * (self.config.print_padding_parent_info - len(formatted_line))

                    print(f"{text_bold(formatted_line)} {padding}         {parent_info}")

            if self.config.trace_capture_lines:
                self.print_lines(item.get('lines'), f'{prefix}{tree_branch}')

            if self.config.print_locals:
                self.formatted_local_data(locals, f'{prefix}{tree_branch}')

            if self.config.capture_extra_data:
                self.formatted_local_data(extra_data, f'{prefix}{tree_branch}', emoji='✨')
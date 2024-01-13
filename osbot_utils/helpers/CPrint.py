from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


# note these attributes will be replaced by methods by CPrint. This is done like this in order to:
#     - Have code complete on CPrint
#     - not have the write the code for each of the methods
#     - have a good and logical place to capture the ID of the color

class Colors:
    black           = "30"                          # todo: figure out if this needs to be a string or if it can be an int
    red             = "31"
    green           = "32"
    yellow          = "33"
    blue            = "34"
    magenta         = "35"
    cyan            = "36"
    white           = "37"
    bright_black    = "90"
    bright_red      = "91"
    bright_green    = "92"
    bright_yellow   = "93"
    bright_blue     = "94"
    bright_magenta  = "95"
    bright_cyan     = "96"
    bright_white    = "97"


class CPrint(Colors, Kwargs_To_Self):
    auto_new_line  : bool = True
    auto_print     : bool = True
    clear_on_print : bool = True
    current_line   : str
    lines          : list

    def __getattribute__(self, name):                                                       # this will replace the attributes defined in colors with methods that will call add_to_current_line with the params provided
        if name != '__getattribute__' and hasattr(Colors, name):                                                           # if name is one of the colors defined in Colors
            def method(*args, **kwargs):                                                    # create a method to replace the attribute
                return self.add_with_color(name, *args, **kwargs)                     # pass the data to add_with_color
            return method
        return super().__getattribute__(name)                                               # if the attribute name is not one of the attributes defined in colors, restore the normal behaviour of __getattribute__

    def add_with_color(self, color_name, *args, **kwargs):
        color_code = getattr(Colors, color_name)                                            # capture the color from the Colors class
        self.add_to_current_line(color_code, *args, **kwargs)                         # add the color code to the current line
        return self

    def add_to_current_line(self, color_code, *args, **kwargs):
        color_start      = f"\033[{color_code}m"                                            # ANSI color code start and end
        color_end        = "\033[0m"
        kwargs['end']    = ''                                                               # remove the default print end (which is \n)
        args             = [str(arg) for arg in args]                                       # Convert all non-string arguments to strings
        text             = "".join(args)                                                    # Concatenate all arguments without a space (to have beter support for multi-prints per line)
        text_with_colors = f"{color_start}{text}{color_end}"
        self.current_line += text_with_colors
        self.apply_config_options()
        return self

    def apply_config_options(self):
        if self.auto_new_line:
            self.flush()
        if self.auto_print:
            self.print()

    def flush(self):
        if self.current_line:
            self.lines.append(self.current_line)
        self.current_line = ''
        return self

    def new_line(self):
        self.flush()
        self.lines.append('')
        self.apply_config_options()
        return self

    def print(self):
        self.flush()
        for line in self.lines:
            print(line)
        if self.clear_on_print:
            self.lines = []
        return self

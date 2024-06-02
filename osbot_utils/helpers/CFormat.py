# note these attributes will be replaced by methods by CPrint. This is done like this in order to:
#     - Have code complete on CPrint
#     - not have the write the code for each of the methods
#     - have a good and logical place to capture the ID of the color
from osbot_utils.base_classes.Type_Safe import Type_Safe


class CFormat_Colors:
    black           = "30"
    blue            = "34"
    cyan            = "36"
    grey            = "38;5;15"
    green           = "32"
    none            = "0"
    magenta         = "35"
    red             = "31"
    white           = "38;5;15"
    yellow          = "33"
    bright_black    = "90"
    bright_red      = "91"
    bright_green    = "92"
    bright_yellow   = "93"
    bright_blue     = "94"
    bright_magenta  = "95"
    bright_cyan     = "96"
    bright_white    = "97"
    dark_red        = "38;5;124"            # see https://github.com/fidian/ansi for a full list

class CFormat(CFormat_Colors, Type_Safe):
    apply_colors: bool = True

    def __getattribute__(self, name):                                                       # this will replace the attributes defined in colors with methods that will call add_to_current_line with the params provided
        if name != '__getattribute__' and hasattr(CFormat_Colors, name):                                                           # if name is one of the colors defined in Colors
            def method(*args, **kwargs):                                                    # create a method to replace the attribute
                return self.apply_color_to_text(name, *args, **kwargs)                           # pass the data to add_with_color
            return method
        return super().__getattribute__(name)                                               # if the attribute name is not one of the attributes defined in colors, restore the normal behaviour of __getattribute__

    def apply_color_to_text(self, color_name, *args, **kwargs):
        color_code = getattr(CFormat_Colors, color_name)                                            # capture the color from the Colors class
        return self.apply_color_code_to_text(color_code, *args, **kwargs)

    def apply_color_code_to_text(self, color_code, *args, **kwargs):
        return self.text_with_colors(color_code, *args, **kwargs)

    def text_with_colors(self, text, color_code):
        if self.apply_colors:
            color_start      = f"\033[{color_code}m"                                            # ANSI color code start and end
            color_end        = "\033[0m"
            return f"{color_start}{text}{color_end}"
        else:
            return text

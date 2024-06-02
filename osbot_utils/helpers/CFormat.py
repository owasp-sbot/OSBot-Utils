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
    none            = "0"           # no color # note: this is using the ascii color reset code, see if there are any side effects
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

    def text_with_colors(self, color_code, *args, **kwargs):
        args = [str(arg) for arg in args]  # Convert all non-string arguments to strings
        text = "".join(args)
        if self.apply_colors:
            color_start      = f"\033[{color_code}m"                                            # ANSI color code start and end
            color_end        = "\033[0m"
            return f"{color_start}{text}{color_end}"
        else:
            return text

cformat = CFormat()

f_black          = cformat.black
f_red            = cformat.red
f_blue           = cformat.blue
f_cyan           = cformat.cyan
f_grey           = cformat.grey
f_green          = cformat.green
f_none           = cformat.none
f_magenta        = cformat.magenta
f_white          = cformat.white
f_yellow         = cformat.yellow
f_bright_black   = cformat.bright_black
f_bright_red     = cformat.bright_red
f_bright_green   = cformat.bright_green
f_bright_yellow  = cformat.bright_yellow
f_bright_blue    = cformat.bright_blue
f_bright_magenta = cformat.bright_magenta
f_bright_cyan    = cformat.bright_cyan
f_bright_white   = cformat.bright_white
f_dark_red       = cformat.dark_red
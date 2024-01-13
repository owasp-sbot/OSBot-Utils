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

    def _print_color(self, color_code, *args, **kwargs):
        color_start   = f"\033[{color_code}m"                   # ANSI color code start and end
        color_end     = "\033[0m"
        kwargs['end'] = ''                                       # remove the default print end (which is \n)
        args          = [str(arg) for arg in args]               # Convert all non-string arguments to strings
        text          = "".join(args)                            # Concatenate all arguments without a space (to have beter support for multi-prints per line)
        print(f"{color_start}{text}{color_end}", **kwargs)
        return self

    def __getattribute__(self, name):
        if hasattr(Colors, name):
            def method(*args, **kwargs):
                color_code = getattr(Colors, name)
                return self._print_color(color_code, *args, **kwargs)
            return method
        return super().__getattribute__(name)

    def line(self):
        print()
        return self


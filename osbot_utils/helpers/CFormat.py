# note these attributes will be replaced by methods by CPrint. This is done like this in order to:
#     - Have code complete on CPrint
#     - not have the write the code for each of the methods
#     - have a good and logical place to capture the ID of the color
from osbot_utils.base_classes.Type_Safe import Type_Safe


class CFormat_Colors:
    black            = "30"
    blue             = "34"
    cyan             = "36"
    grey             = "38;5;15"
    green            = "32"
    none             = "0"           # no color # note: this is using the ascii color reset code, see if there are any side effects
    magenta          = "35"
    red              = "31"
    white            = "38;5;15"
    yellow           = "33"
    bright_black     = "90"
    bright_red       = "91"
    bright_green     = "92"
    bright_yellow    = "93"
    bright_blue      = "94"
    bright_magenta   = "95"
    bright_cyan      = "96"
    bright_white     = "97"
    dark_red         = "38;5;124"            # see https://github.com/fidian/ansi for a full list
    dark_grey        = "38;5;8"

    bold             = "1"         # ANSI escape code for bold
    italic           = "3"         # ANSI escape code for italic
    underline        = "4"         # ANSI escape code for underline
    blink            = "5"         # (no visual change in pycharm console) ANSI escape code for blink (not widely supported)
    inverse          = "7"         # ANSI escape code for inverse/negative
    strikethrough    = "9"         # ANSI escape code for strikethrough
    double_underline = "21"        # ANSI escape code for double underline
    faint            = "2"         # (no visual change in pycharm console)  ANSI escape code for faint/dim
    framed           = "51"        # ANSI escape code for framed (rarely supported)
    encircled        = "52"        # ANSI escape code for encircled (rarely supported)
    overlined        = "53"        # (no visual change in pycharm console) ANSI escape code for overlined

class CFormat(CFormat_Colors, Type_Safe):
    apply_colors: bool = True
    auto_bold   : bool = False

    def __getattribute__(self, name):                                                       # this will replace the attributes defined in colors with methods that will call add_to_current_line with the params provided
        if name != '__getattribute__' and hasattr(CFormat_Colors, name):                                                           # if name is one of the colors defined in Colors
            def method(*args, **kwargs):                                                    # create a method to replace the attribute
                return self.apply_color_to_text(name, *args, **kwargs)                           # pass the data to add_with_color
            return method
        return super().__getattribute__(name)                                               # if the attribute name is not one of the attributes defined in colors, restore the normal behaviour of __getattribute__

    def rgb(self, r, g, b, *args):
        color_code = f"38;2;{r};{g};{b}"
        return self.text_with_colors(color_code, *args)

    def bg_rgb(self, r, g, b, *args):
        color_code = f"48;2;{r};{g};{b}"
        return self.text_with_colors(color_code, *args)

    def cmyk(self, c, m, y, k, *args):
        # CMYK to RGB conversion
        r = 255 * (1 - c / 100) * (1 - k / 100)
        g = 255 * (1 - m / 100) * (1 - k / 100)
        b = 255 * (1 - y / 100) * (1 - k / 100)
        color_code = f"38;2;{int(r)};{int(g)};{int(b)}"
        return self.text_with_colors(color_code, *args)

    def bg_cmyk(self, c, m, y, k, *args):
        # CMYK to RGB conversion
        r = 255 * (1 - c / 100) * (1 - k / 100)
        g = 255 * (1 - m / 100) * (1 - k / 100)
        b = 255 * (1 - y / 100) * (1 - k / 100)
        color_code = f"48;2;{int(r)};{int(g)};{int(b)}"
        return self.text_with_colors(color_code, *args)

    def hex(self, hex_code, *args):
        # Convert hex to RGB
        hex_code = hex_code.lstrip('#')
        r, g, b = int(hex_code[0:2], 16), int(hex_code[2:4], 16), int(hex_code[4:6], 16)
        color_code = f"38;2;{r};{g};{b}"
        return self.text_with_colors(color_code, *args)

    def bg_hex(self, hex_code, *args):
        # Convert hex to RGB
        hex_code = hex_code.lstrip('#')
        r, g, b = int(hex_code[0:2], 16), int(hex_code[2:4], 16), int(hex_code[4:6], 16)
        color_code = f"48;2;{r};{g};{b}"
        return self.text_with_colors(color_code, *args)

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
            text_with_color  = f"{color_start}{text}{color_end}"
            if self.auto_bold:
                return f"\033[1m{text_with_color}\033[0m"
            return text_with_color
        else:
            return text

cformat = CFormat()

# ascii formating static helper methods
f_bold             = cformat.bold
f_italic           = cformat.italic
f_underline        = cformat.underline
f_blink            = cformat.blink
f_inverse          = cformat.inverse
f_strikethrough    = cformat.strikethrough
f_double_underline = cformat.double_underline
f_faint            = cformat.faint
f_framed           = cformat.framed
f_encircled        = cformat.encircled
f_overlined        = cformat.overlined


# ascii colors static helper methods
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
f_dark_grey      = cformat.dark_grey
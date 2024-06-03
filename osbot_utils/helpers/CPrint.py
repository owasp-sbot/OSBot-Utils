from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.CFormat import CFormat, CFormat_Colors


class CPrint(CFormat):
    auto_new_line  : bool = True
    auto_print     : bool = True
    clear_on_print : bool = True
    current_line   : str
    lines          : list

    def apply_color_code_to_text(self, color_code, *args, **kwargs):
        self.add_to_current_line(color_code, *args, **kwargs)
        return self

    def add_to_current_line(self, color_code, *args, **kwargs):
        self.current_line += self.text_with_colors(color_code, *args, **kwargs)
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

    def lines_str(self):
        lines_str = ''
        for line in self.lines:
            lines_str += line + '\n'
        return lines_str

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



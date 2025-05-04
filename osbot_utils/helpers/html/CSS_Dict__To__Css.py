from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

class CSS_Dict__To__Css(Kwargs_To_Self):
    css: dict


    def add_css_entry(self, selector, data):
        self.css[selector] = data
        return self

    def convert(self, indent=''):
        css_lines = []                                                          # List to hold each line of CSS
        for selector, properties in self.css.items():
            css_line = f"{indent}{selector} {{"                                 # Start the selector line
            for prop, value in properties.items():                              # Add each property and value to the selector's CSS
                css_line += f"\n{indent}    {prop}: {value};"
            css_line += '\n' + indent + "}"                                     # Close the selector's CSS block
            css_lines.append(css_line)                                          # Add the completed selector's CSS to the list
        return "\n".join(css_lines)                                             # Join all selector CSS blocks with a newline and return

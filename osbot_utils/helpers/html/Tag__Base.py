from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

INDENT_SIZE = 4

class Tag__Base(Kwargs_To_Self):
    indent   : int
    tag_name : str

    new_line_before_elements : bool = True
    def render_attributes(self, attributes):
        html_attributes = ' '.join([f'{key}="{value}"' for key, value in attributes.items()])
        return html_attributes

    def render_element(self, attributes, elements):
        html_attributes = self.render_attributes(attributes)
        html_elements   = self.render_elements(elements)
        element_indent  = " " * self.indent * INDENT_SIZE

        html = f"{element_indent}<{self.tag_name}"
        if html_attributes:
            html += f" {html_attributes}"
        html += ">"
        if html_elements:
            if self.new_line_before_elements:
                html += "\n"
            html += f"{html_elements}"
            if self.new_line_before_elements:
                html += "\n"
        html += f"</{self.tag_name}>"
        return html

    def render_elements(self, elements):
        html_elements = ""
        for element in elements:
            html_element = element.render()
            html_elements += html_element
        return html_elements
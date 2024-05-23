from collections import defaultdict

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.Files import file_create

INDENT_SIZE = 4

class Tag__Base(Kwargs_To_Self):
    attributes               : dict
    elements                 : list
    end_tag                  : bool = True
    indent                   : int
    tag_name                 : str
    tag_classes              : list
    inner_html               : str
    new_line_before_elements : bool = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.locked()                                   # lock the object so that it is not possible to add new attributes via normal assigment

    def append(self, *elements):
        self.elements.extend(elements)
        return self

    def attributes_values(self, *attributes_names):
        attributes = {}
        for attribute_name in attributes_names:
            if hasattr(self, attribute_name):
                attribute_value = getattr(self, attribute_name)
                if attribute_value:
                    attributes[attribute_name] = attribute_value
        return attributes

    def elements__by_tag_name(self):
        result = defaultdict(list)
        for element in self.elements:
            result[element.tag_name].append(element)
        return dict(result)

    def elements__with_tag_name(self, tag_name):
        return self.elements__by_tag_name().get(tag_name)

    def save(self, file_path):
        return file_create(file_path, self.render())

    def render_attributes(self):
        attributes = self.attributes.copy()
        if self.tag_classes:
            attributes['class'] = ' '.join(self.tag_classes)

        html_attributes = ' '.join([f'{key}="{value}"' for key, value in attributes.items()])
        return html_attributes

    def render_element(self):
        html_attributes = self.render_attributes()
        html_elements   = self.render_elements()
        element_indent  = " " * self.indent * INDENT_SIZE

        html = f"{element_indent}<{self.tag_name}"
        if html_attributes:
            html += f" {html_attributes}"
        if self.end_tag:
            html += ">"
            if self.inner_html:
                html += self.inner_html
            if html_elements:
                if self.new_line_before_elements:
                    html += "\n"
                html += f"{html_elements}"
                if self.new_line_before_elements:
                    html += "\n"
                html += element_indent
            html += f"</{self.tag_name}>"
        else:
            html += "/>"

        return html

    def render_elements(self):
        html_elements = ""
        for index, element in enumerate(self.elements):
            if index:
                html_elements += '\n'
            element.indent = self.indent + 1        # set the indent of the child element based on the current one
            html_element = element.render()
            html_elements += html_element
        return html_elements

    def render(self):
        return self.render_element()

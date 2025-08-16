from collections                                import defaultdict

from osbot_utils.helpers.html.transformers.Html__To__Html_Dict import STRING__SCHEMA_TEXT
from osbot_utils.type_safe.Type_Safe            import Type_Safe
from osbot_utils.utils.Files                    import file_create

INDENT_SIZE = 4

class Tag__Base(Type_Safe):
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
        element_indent = " " * self.indent * INDENT_SIZE

        html = f"{element_indent}<{self.tag_name}"
        if html_attributes:
            html += f" {html_attributes}"

        if self.end_tag:
            html += ">"

            # Check for text nodes and regular element nodes
            text_nodes = [e for e in self.elements if hasattr(e, 'type') and e.type == STRING__SCHEMA_TEXT]
            element_nodes = [e for e in self.elements if not hasattr(e, 'type') or e.type != STRING__SCHEMA_TEXT]

            has_text = bool(text_nodes) or bool(self.inner_html)
            has_elements = bool(element_nodes)

            # Add inner_html if it exists
            if self.inner_html:
                html += self.inner_html

            # Get the rendered element HTML
            html_elements = self.render_elements()

            # Add element nodes with proper formatting
            if html_elements:
                # Only add newlines if we have element nodes and no text nodes,
                # or if we explicitly want newlines before elements
                if (has_elements and not has_text) or (self.new_line_before_elements and not has_text):
                    html += "\n"

                html += html_elements

                # Add closing newline and indent only for pure element content
                if (has_elements and not has_text) or (self.new_line_before_elements and not has_text):
                    html += "\n"
                    html += element_indent

            html += f"</{self.tag_name}>"
        else:
            html += "/>"

        return html

    def render_elements(self):
        html_elements = ""
        has_element_nodes = False

        for index, element in enumerate(self.elements):
            # Handle text nodes
            if hasattr(element, 'type') and element.type == STRING__SCHEMA_TEXT:
                html_elements += element.data
                continue

            # Only add newlines between element nodes (not text nodes)
            if has_element_nodes:
                html_elements += '\n'

            has_element_nodes = True
            element.indent = self.indent + 1        # set the indent of the child element based on the current one
            html_element = element.render()
            html_elements += html_element

        return html_elements

    def render(self):
        return self.render_element()

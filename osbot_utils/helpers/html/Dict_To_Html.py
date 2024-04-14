
HTML_SELF_CLOSING_TAGS = {'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

class Dict_To_Html:
    def __init__(self, root):
        # Define a list of self-closing tags
        self.self_closing_tags =HTML_SELF_CLOSING_TAGS # {'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
        self.root = root

    def convert(self):
        return self.convert_element(self.root, 0)               # Start conversion with the root element and initial indentation level 0

    def convert_attrs(self, attrs):
        attrs_str_parts = []                                                # List to hold each attribute's string representation
        for key, value in attrs.items():
            if '"' in value:                                                # Check if the attribute value contains double quotes
                escaped_value = "&quot;".join(value.split("\""))            # If so, escape double quotes and format the attribute string
                attr_str      = f'{key}="{escaped_value}"'
            else:
                attr_str = f'{key}="{value}"'                               # If not, simply format the attribute string
            attrs_str_parts.append(attr_str)

        attrs_str = ' '.join(attrs_str_parts)                               # Join the parts into the final attributes string

        if attrs_str:
            attrs_str = " " + attrs_str                                     # Prepend a space if there are attributes
        return attrs_str

    def convert_element(self, element, indent_level):
        """Recursively converts a dictionary to an HTML string with indentation."""
        tag      = element.get("tag")
        attrs    = element.get("attrs", {})
        children = element.get("children", [])
        data     = element.get("data", "")

        attrs_str = self.convert_attrs(attrs)                           # Convert attributes dictionary to a string
        indent = "    " * indent_level                                  # Indentation for the current level, assuming 4 spaces per indent level

        if tag in self.self_closing_tags:                               # Check if the tag is self-closing
            return f"{indent}<{tag}{attrs_str} />\n"

        html = f"{indent}<{tag}{attrs_str}>"                            # Opening tag with indentation
        if not data:
            html += '\n'

        for child in children:                                          # Process children with incremented indent level
            html += self.convert_element(child, indent_level + 1)

        if data:                                                        # Add data if present
            html += data

        if children:                                                    # Closing tag for non-self-closing tags, with indentation
            html += f"{indent}</{tag}>\n"                               # Add closing tag on a new line if there are children
        elif data:
            html += f"</{tag}>\n"
        else:                                                           # Place closing tag directly after opening tag if there are no children or data
            html = f"{indent}<{tag}{attrs_str}></{tag}>\n"

        return html
class Dict_To_Html:
    def __init__(self, root):
        # Define a list of self-closing tags
        self.self_closing_tags = {'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
        self.root = root

    def convert(self):
        # Start conversion with the root element and initial indentation level 0
        return self.convert_element(self.root, 0)

    def convert_element(self, element, indent_level):
        """Recursively converts a dictionary to an HTML string with indentation."""
        tag = element.get("tag")
        attrs = element.get("attrs", {})
        children = element.get("children", [])
        data = element.get("data", "")

        # Convert attributes dictionary to a string
        attrs_str = ' '.join(f'{key}="{"&quot;".join(value.split("\""))}"' if '"' in value else f'{key}="{value}"' for key, value in attrs.items())
        if attrs_str:
            attrs_str = " " + attrs_str

        # Indentation for the current level
        indent = "    " * indent_level  # Assuming 4 spaces per indent level

        # Check if the tag is self-closing
        if tag in self.self_closing_tags:
            return f"{indent}<{tag}{attrs_str} />\n"

        # Opening tag with indentation
        html = f"{indent}<{tag}{attrs_str}>"
        if not data:
            html += '\n'

        # Process children with incremented indent level
        for child in children:
            html += self.convert_element(child, indent_level + 1)

        # Add data if present, directly without additional indentation
        if data:
            #html += f"{indent}    {data}\n"
            html += data

        # Closing tag for non-self-closing tags, with indentation
        if children:  # Add closing tag on a new line if there are children or data
            html += f"{indent}</{tag}>\n"
        elif data:
            html += f"</{tag}>\n"
        else:  # Place closing tag directly after opening tag if there are no children or data
            html = f"{indent}<{tag}{attrs_str}></{tag}>\n"

        return html
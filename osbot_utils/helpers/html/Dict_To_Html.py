class Dict_To_Html:
    def __init__(self, root):
        # Define a list of self-closing tags
        self.self_closing_tags = {'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
        self.root = root

    def convert(self):
        return self.convert_element(self.root)

    def convert_element(self, element):
        """Recursively converts a dictionary to an HTML string."""
        tag         = element.get("tag")
        attrs       = element.get("attrs", {})
        children    = element.get("children", [])
        data        = element.get("data", "")

        # Convert attributes dictionary to a string
        attrs_str = ' '.join(f'{key}="{"&quot;".join(value.split("\""))}"' if '"' in value else f'{key}="{value}"' for key, value in attrs.items())
        if attrs_str:
            attrs_str = " " + attrs_str

        # Check if the tag is self-closing
        if tag in self.self_closing_tags:
            return f"<{tag}{attrs_str} />"

        # Opening tag
        html = f"<{tag}{attrs_str}>"

        # Add data if present
        if data:
            html += data

        # Recursively add children
        for child in children:
            html += self.convert_element(child)

        # Closing tag for non-self-closing tags
        html += f"</{tag}>"

        return html
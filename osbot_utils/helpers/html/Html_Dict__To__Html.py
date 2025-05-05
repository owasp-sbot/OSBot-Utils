from osbot_utils.helpers.html.Html__To__Html_Dict import STRING__SCHEMA_TEXT, STRING__SCHEMA_NODES

HTML_SELF_CLOSING_TAGS     = {'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
HTML_DEFAULT_DOCTYPE_VALUE = "<!DOCTYPE html>\n"

class Html_Dict__To__Html:
    def __init__(self, root, include_doctype=True, doctype=HTML_DEFAULT_DOCTYPE_VALUE):
        self.self_closing_tags = HTML_SELF_CLOSING_TAGS             # Define a list of self-closing tags
        self.root              = root
        self.include_doctype   = include_doctype
        self.doctype           = doctype

    def convert(self):
        html = self.convert_element(self.root, 0)
        if self.include_doctype:
            return self.doctype + html
        return html

    def convert_attrs(self, attrs):
        attrs_str_parts = []                                                # List to hold each attribute's string representation
        for key, value in attrs.items():
            if value is None:                                               # Handle None values
                attr_str = f'{key}'
            elif '"' in str(value):                                         # Check if the attribute value contains double quotes
                escaped_value = "&quot;".join(str(value).split("\""))       # If so, escape double quotes and format the attribute string
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
        # Check if this is a text node
        if element.get("type") == STRING__SCHEMA_TEXT:
            return element.get("data", "")                                  # Return text content directly for text nodes

        tag   = element.get("tag")
        attrs = element.get("attrs", {})
        nodes = element.get(STRING__SCHEMA_NODES, [])

        attrs_str = self.convert_attrs(attrs)                               # Convert attributes dictionary to a string
        indent = "    " * indent_level                                      # Indentation for the current level, assuming 4 spaces per indent level

        # Handle self-closing tags
        if tag in self.self_closing_tags and not nodes:                  # Check if the tag is self-closing and has no nodes
            return f"{indent}<{tag}{attrs_str} />\n"

        # Start building the HTML
        html = f"{indent}<{tag}{attrs_str}>"                                # Opening tag with indentation

        # Separate nodes into text nodes and element nodes
        text_nodes    = [node for node in nodes if node.get("type") == STRING__SCHEMA_TEXT]
        element_nodes = [node for node in nodes if node.get("type") != STRING__SCHEMA_TEXT]

        # If there are only element nodes, add a newline after the opening tag
        if element_nodes and not text_nodes:
            html += "\n"

        # Process nodes, maintaining the original order but with proper formatting
        if nodes:
            # Track if we're currently in a text section or element section
            # This helps us add newlines only between elements, not text
            previous_was_element = False

            for node in nodes:
                if node.get("type") == STRING__SCHEMA_TEXT:
                    # Text node - directly append content
                    html += node.get("data", "")
                    previous_was_element = False
                else:
                    # Element node - format with proper indentation
                    if previous_was_element:
                        # If previous child was also an element, we may already have a newline
                        if not html.endswith("\n"):
                            html += "\n"

                    html += self.convert_element(node, indent_level + 1)
                    previous_was_element = True

        # Handle closing tag based on content
        if element_nodes and not text_nodes:
            # If only element nodes, add indented closing tag
            html += f"{indent}</{tag}>\n"
        elif nodes:  # Any type of nodes
            # If mixed content or only text, add closing tag without indentation
            html += f"</{tag}>\n"
        else:
            # Empty tag, replace with self-contained format
            html = f"{indent}<{tag}{attrs_str}></{tag}>\n"

        return html
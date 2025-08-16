from osbot_utils.helpers.html.transformers.Html__To__Html_Dict import STRING__SCHEMA_TEXT, STRING__SCHEMA_NODES

HTML_SELF_CLOSING_TAGS = {'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'link', 'meta',
                          'param', 'source', 'track', 'wbr'}
HTML_DEFAULT_DOCTYPE_VALUE = "<!DOCTYPE html>\n"


class Html_Dict__To__Html:
    def __init__(self, root,  # Root element dictionary
                 include_doctype=True,  # Whether to include DOCTYPE
                 doctype=HTML_DEFAULT_DOCTYPE_VALUE  # DOCTYPE string to use
                 ):
        self.self_closing_tags = HTML_SELF_CLOSING_TAGS
        self.root = root
        self.include_doctype = include_doctype
        self.doctype = doctype

    def convert(self):  # Convert dictionary to HTML string
        if not self.root:
            return ""

        html = self.convert_element(self.root, 0)

        if self.include_doctype and self.root.get("tag") == "html":  # Only add DOCTYPE for html root
            return self.doctype + html
        return html

    def convert_attrs(self, attrs):  # Convert attributes dict to HTML string
        if not attrs:
            return ""

        attrs_str_parts = []

        for key, value in attrs.items():  # Preserve original order
            if value is None:
                attr_str = f'{key}'
            elif value == "":  # Handle empty string values
                attr_str = f'{key}=""'
            elif '"' in str(value) and "'" in str(value):  # Both quotes present
                escaped_value = str(value).replace('"', '&quot;')
                attr_str = f'{key}="{escaped_value}"'
            elif '"' in str(value):  # Use single quotes if double quotes present
                attr_str = f"{key}='{value}'"
            else:
                attr_str = f'{key}="{value}"'
            attrs_str_parts.append(attr_str)

        attrs_str = ' '.join(attrs_str_parts)
        return f" {attrs_str}" if attrs_str else ""

    def convert_element(self, element,  # Element dictionary to convert
                        indent_level  # Current indentation level
                        ):
        if element.get("type") == STRING__SCHEMA_TEXT:
            return element.get("data", "")

        tag = element.get("tag")
        attrs = element.get("attrs", {})
        nodes = element.get(STRING__SCHEMA_NODES, [])

        if not tag:  # Safety check
            return ""

        attrs_str = self.convert_attrs(attrs)
        indent = "    " * indent_level

        # Special handling for void elements
        if tag in self.self_closing_tags:
            if nodes:  # Void elements shouldn't have content
                print(f"Warning: void element <{tag}> has child nodes")
            return f"{indent}<{tag}{attrs_str} />\n"

        # Start building the HTML
        html = f"{indent}<{tag}{attrs_str}>"

        # Analyze content type
        has_text_nodes = any(node.get("type") == STRING__SCHEMA_TEXT for node in nodes)
        has_element_nodes = any(node.get("type") != STRING__SCHEMA_TEXT for node in nodes)

        # Determine formatting strategy
        if not nodes:  # Empty element
            html += f"</{tag}>\n"
        elif has_element_nodes and not has_text_nodes:  # Only element children
            html += "\n"
            html += self.convert_children(nodes, indent_level + 1)
            html += f"{indent}</{tag}>\n"
        elif has_text_nodes and not has_element_nodes:  # Only text content
            html += self.convert_children(nodes, indent_level + 1)
            html += f"</{tag}>\n"
        else:  # Mixed content
            # For mixed content, don't add extra formatting
            for node in nodes:
                if node.get("type") == STRING__SCHEMA_TEXT:
                    html += node.get("data", "")
                else:
                    # Recursively convert child elements with no indentation
                    child_html = self.convert_element(node, 0)
                    # Remove the trailing newline from child elements in mixed content
                    if child_html.endswith('\n'):
                        child_html = child_html[:-1]
                    html += child_html
            html += f"</{tag}>\n"

        return html

    def convert_children(self, nodes,  # List of child nodes
                         indent_level  # Current indentation level
                         ):
        html = ""
        for node in nodes:
            html += self.convert_element(node, indent_level)
        return html
from html.parser import HTMLParser

HTML_SELF_CLOSING_TAGS = {'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
STRING__SCHEMA_ATTRS   = 'attrs'
STRING__SCHEMA_NODES   = 'nodes'
STRING__SCHEMA_TEXT    = 'TEXT'
STRING__SCHEMA_TAG     = 'tag'

STRING__DATA_TEXT      = f'{STRING__SCHEMA_TEXT}:'


class Html__To__Html_Dict(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.root            = None                               # No root initially
        self.current         = None                               # No current node at the start
        self.stack           = []                                 # Empty stack for hierarchy management
        self.html            = html or ''
        self.void_elements   = HTML_SELF_CLOSING_TAGS             # List of void elements that are self-closing by nature
        self.strip_text_data = True

    def convert(self):
        self.feed(self.html)
        return self.root

    def handle_starttag(self, tag, attrs):
        new_tag = {"tag": tag, "attrs": dict(attrs), STRING__SCHEMA_NODES: []}

        if self.current is None:
            # When the first tag is encountered, it becomes the root
            self.root = new_tag
            self.current = new_tag
        else:
            # Otherwise, append the new tag as a child of the current tag
            self.current[STRING__SCHEMA_NODES].append(new_tag)

        # If this tag is not a void element, push it onto the stack
        if tag.lower() not in self.void_elements:
            self.stack.append(new_tag)
            self.current = new_tag

    def handle_endtag(self, tag):
        # Find and pop the matching start tag
        if tag.lower() not in self.void_elements and len(self.stack) > 1:
            # Look for the matching start tag in the stack
            for i in range(len(self.stack) - 1, 0, -1):
                if self.stack[i]["tag"].lower() == tag.lower():
                    # Pop all tags up to and including the matching start tag
                    self.stack = self.stack[:i]
                    break
            # Update current to the top of stack
            self.current = self.stack[-1]

    def handle_data(self, data):
        if data.strip():  # Ignore whitespace
            # Create a text node as a child
            text_node = {"type": STRING__SCHEMA_TEXT, "data": data}
            self.current[STRING__SCHEMA_NODES].append(text_node)

    def print__generate_lines(self, node, indent="", last=True, is_root=True):
        lines = []

        prefix = "" if is_root else ("└── " if last else "├── ")

        if node.get("type") == STRING__SCHEMA_TEXT:
            text_data = node.get('data')
            if self.strip_text_data:
                text_data = text_data.strip()
            lines.append(f"{indent}{prefix}{STRING__DATA_TEXT} {text_data}")
        else:
            tag       = node.get("tag")
            attrs     = node.get("attrs", {})
            nodes     = node.get(STRING__SCHEMA_NODES, [])
            attrs_str = ' '.join(f'{key}="{value}"' for key, value in attrs.items())
            attrs_str = f' ({attrs_str})' if attrs_str else ''

            lines.append(f"{indent}{prefix}{tag}{attrs_str}")

            child_indent = indent + ("    " if last else "│   ")

            for i, node in enumerate(nodes):
                is_last = i == len(nodes) - 1
                child_lines = self.print__generate_lines(node, indent=child_indent, last=is_last, is_root=False)
                lines.extend(child_lines if isinstance(child_lines, list) else [child_lines])

        return lines if is_root else "\n".join(lines)

    def print(self, just_return_lines=False):
        if self.root:
            lines = self.print__generate_lines(self.root, is_root=True)
            if just_return_lines:
                return lines
            else:
                self.print__lines(lines)
        return self

    def print__lines(self, lines):
        for line in lines:
            print(line)


def html_to_dict(html_code: str) -> dict:
    try:
        html_to_dict = Html__To__Html_Dict(html_code)
        html_dict = html_to_dict.convert()
        return html_dict
    except:  # todo: see if there is a better Exception to capture
        return None  # if we couldn't parse the html, just return None
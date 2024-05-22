from html.parser import HTMLParser

class Html_To_Dict(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.root    = None            # No root initially
        self.current = None         # No current node at the start
        self.stack   = []             # Empty stack for hierarchy management
        self.html    = html or ''

    def convert(self):
        self.feed(self.html)
        return self.root

    def handle_starttag(self, tag, attrs):
        new_tag = {"tag": tag, "attrs": dict(attrs), "children": [], "data": ""}

        if self.current is None:
            # When the first tag is encountered, it becomes the root
            self.root = new_tag
            self.current = new_tag
        else:
            # Otherwise, append the new tag as a child of the current tag
            self.current["children"].append(new_tag)

        # Update the stack and current pointers
        self.stack.append(new_tag)
        self.current = new_tag

    def handle_endtag(self, tag):
        if len(self.stack) > 1:
            self.stack.pop()
            self.current = self.stack[-1]

    def handle_data(self, data):
        if data.strip():  # Ignore whitespace
            if "data" in self.current:
                self.current["data"] += data
            else:
                self.current["data"] = data

    def print__generate_lines(self, node, indent="", last=True, is_root=True):
        lines = []

        prefix = "" if is_root else ("└── " if last else "├── ")

        tag = node.get("tag")
        attrs = node.get("attrs", {})
        children = node.get("children", [])
        attrs_str = ' '.join(f'{key}="{value}"' for key, value in attrs.items())
        attrs_str = f' ({attrs_str})' if attrs_str else ''

        lines.append(f"{indent}{prefix}{tag}{attrs_str}")

        child_indent = indent + ("    " if last else "│   ")

        for i, child in enumerate(children):
            is_last = i == len(children) - 1
            child_lines = self.print__generate_lines(child, indent=child_indent, last=is_last, is_root=False)
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
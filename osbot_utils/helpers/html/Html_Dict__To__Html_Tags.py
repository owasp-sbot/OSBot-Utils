from osbot_utils.helpers.html.Html_Dict__To__Html import HTML_SELF_CLOSING_TAGS
from osbot_utils.helpers.html.Html__To__Html_Dict import STRING__SCHEMA_TEXT, STRING__SCHEMA_NODES
from osbot_utils.helpers.html.Tag__Base           import Tag__Base
from osbot_utils.helpers.html.Tag__Body           import Tag__Body
from osbot_utils.helpers.html.Tag__Head           import Tag__Head
from osbot_utils.helpers.html.Tag__Html           import Tag__Html
from osbot_utils.helpers.html.Tag__Link           import Tag__Link
from osbot_utils.helpers.html.Tag__Text           import Tag__Text


class Html_Dict__To__Html_Tags:

    def __init__(self, root):
        self.root = root

    def convert(self):
        return self.convert_element(self.root)

    def convert_element(self, element):
        tag_name = element.get("tag")

        # Handle special tag types with dedicated conversion methods
        if tag_name == 'html':
            return self.convert_to__tag__html(element)
        elif tag_name == 'head':
            return self.convert_to__tag__head(element, 0)  # Default indent 0
        elif tag_name == 'link':
            return self.convert_to__tag__link(element)
        else:
            # Default case: convert to a generic Tag__Base
            return self.convert_to__tag(Tag__Base, element, 0)  # Default indent 0

    def collect_inner_text(self, element):
        """Extract all text from an element's text node nodes."""
        inner_text = ""
        for node in element.get(STRING__SCHEMA_NODES, []):
            if node.get("type") == STRING__SCHEMA_TEXT:
                inner_text += node.get("data", "")
        return inner_text

    def convert_to__tag(self, target_tag, element, indent):
        if element.get("type") == STRING__SCHEMA_TEXT:
            # Handle text nodes directly
            return Tag__Text(element.get("data", ""))

        tag_name   = element.get("tag")
        attrs      = element.get("attrs", {})
        nodes      = element.get(STRING__SCHEMA_NODES, [])
        end_tag    = tag_name not in HTML_SELF_CLOSING_TAGS
        tag_indent = indent + 1

        # Collect inner text from all text node nodes
        inner_html = self.collect_inner_text(element)

        tag_kwargs = dict(
            tag_name   = tag_name,
            attributes = attrs,
            end_tag    = end_tag,
            indent     = tag_indent,
            inner_html = inner_html
        )

        tag = target_tag(**tag_kwargs)

        # Process only element nodes as nodes (text is already handled via inner_html)
        for node in nodes:
            if node.get("type") != STRING__SCHEMA_TEXT:  # Skip text nodes, they're in inner_html
                child_tag = self.convert_to__tag(Tag__Base, node, tag_indent)
                tag.elements.append(child_tag)

        return tag

    def convert_to__tag__head(self, element, indent):
        attrs = element.get("attrs", {})
        nodes = element.get(STRING__SCHEMA_NODES, [])

        head_indent = indent + 1
        tag_head = Tag__Head(indent=head_indent, **attrs)

        for node in nodes:
            tag_name = node.get("tag")

            if tag_name == 'title':
                # Extract title text from text node nodes
                tag_head.title = self.collect_inner_text(node)
            elif tag_name == 'link':
                tag_head.links.append(self.convert_to__tag__link(node))
            elif tag_name == 'meta':
                tag_head.elements.append(self.convert_to__tag(Tag__Base, node, head_indent))
            elif tag_name == 'style':
                # For style tags, collect the CSS content from text nodes
                style_element = self.convert_to__tag(Tag__Base, node, head_indent)
                tag_head.elements.append(style_element)
            else:
                # Handle any other head elements
                tag_head.elements.append(self.convert_to__tag(Tag__Base, node, head_indent))

        return tag_head

    def convert_to__tag__html(self, element):
        attrs = element.get("attrs", {})
        nodes = element.get(STRING__SCHEMA_NODES, [])
        lang  = attrs.get("lang")

        tag_html = Tag__Html(attributes=attrs, lang=lang, doc_type=False)

        # Initialize head and body if not found
        head_found = False
        body_found = False

        for node in nodes:
            tag_name = node.get("tag")

            if tag_name == 'head':
                tag_html.head = self.convert_to__tag__head(node, tag_html.indent)
                head_found = True
            elif tag_name == 'body':
                tag_html.body = self.convert_to__tag(Tag__Body, node, tag_html.indent)
                body_found = True
            else:
                # Log unexpected child elements of html
                print(f'Unexpected child of html tag: {tag_name}')

        # Handle missing head or body (required for valid HTML structure)
        if not head_found:
            #print("Warning: No head element found, creating empty one")
            tag_html.head = Tag__Head(indent=tag_html.indent + 1)

        if not body_found:
            #print("Warning: No body element found, creating empty one")
            tag_html.body = Tag__Body(indent=tag_html.indent + 1)

        return tag_html

    def convert_to__tag__link(self, element):
        attrs    = element.get("attrs", {})
        tag_link = Tag__Link(**attrs)
        return tag_link
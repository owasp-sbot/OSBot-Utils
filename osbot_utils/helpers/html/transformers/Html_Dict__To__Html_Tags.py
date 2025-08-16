from osbot_utils.helpers.html.transformers.Html_Dict__To__Html import HTML_SELF_CLOSING_TAGS
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict import STRING__SCHEMA_TEXT, STRING__SCHEMA_NODES
from osbot_utils.helpers.html.tags.Tag__Base                   import Tag__Base
from osbot_utils.helpers.html.tags.Tag__Body                   import Tag__Body
from osbot_utils.helpers.html.tags.Tag__Head                   import Tag__Head
from osbot_utils.helpers.html.tags.Tag__Html                   import Tag__Html
from osbot_utils.helpers.html.tags.Tag__Link                   import Tag__Link
from osbot_utils.helpers.html.tags.Tag__Text                   import Tag__Text


class Html_Dict__To__Html_Tags:

    def __init__(self, root):
        self.root = root

    def convert(self):
        return self.convert_element(self.root)

    def convert_element(self, element):
        tag_name = element.get("tag")


        if tag_name == 'html':                                  # Handle special tag types with dedicated conversion methods
            return self.convert_to__tag__html(element)
        elif tag_name == 'head':
            return self.convert_to__tag__head(element, 0)       # Default indent 0
        elif tag_name == 'link':
            return self.convert_to__tag__link(element)
        else:                                                   # Default case: convert to a generic Tag__Base
            return self.convert_to__tag(Tag__Base, element, 0)  # Default indent 0

    def collect_inner_text(self, element):                      # Extract all text from an element's text node nodes.
        inner_text = ""
        for node in element.get(STRING__SCHEMA_NODES, []):
            if node.get("type") == STRING__SCHEMA_TEXT:
                inner_text += node.get("data", "")
        return inner_text

    def convert_to__tag(self, target_tag, element, indent):
        if element.get("type") == STRING__SCHEMA_TEXT:          # Handle text nodes directly
            return Tag__Text(element.get("data", ""))

        tag_name   = element.get("tag")
        attrs      = element.get("attrs", {})
        nodes      = element.get(STRING__SCHEMA_NODES, [])
        end_tag    = tag_name not in HTML_SELF_CLOSING_TAGS
        tag_indent = indent + 1

        node_positions = []                                                     # Create node lists with position tracking

        for idx, node in enumerate(nodes):                                      # Process all nodes and track their positions
            if node.get("type") == STRING__SCHEMA_TEXT:
                text_obj = Tag__Text(node.get("data", ""))                      # Create text node with position info
                node_positions.append((idx, 'text', text_obj))
            else:
                child_tag = self.convert_to__tag(Tag__Base, node, tag_indent)   # Create element node
                node_positions.append((idx, 'element', child_tag))

        node_positions.sort(key=lambda x: x[0])                                 # Sort by position (though they should already be in order)


        inner_html = ""                                                         # Collect consecutive text nodes at the beginning for inner_html
        first_element_idx = None

        for idx, (pos, node_type, node_obj) in enumerate(node_positions):
            if node_type == 'element':
                first_element_idx = idx
                break
            else:
                inner_html += node_obj.data


        if first_element_idx is None:                                                           # If all nodes are text, use them all as inner_html
            inner_html = "".join(n[2].data for n in node_positions if n[1] == 'text')
            elements = []
        else:
            inner_html = "".join(n[2].data for i, n in enumerate(node_positions)                # Only use text before first element as inner_html
                               if n[1] == 'text' and i < first_element_idx)
            elements = [n[2] for i, n in enumerate(node_positions) if i >= first_element_idx]   # All nodes go into elements (including remaining text nodes)

        tag_kwargs   = dict(tag_name   = tag_name   ,
                            attributes = attrs     ,
                            end_tag    = end_tag   ,
                            indent     = tag_indent,
                            inner_html = inner_html)
        tag          = target_tag(**tag_kwargs)
        tag.elements = elements

        return tag

    def convert_to__tag__head(self, element, indent):
        attrs       = element.get("attrs", {})
        nodes       = element.get(STRING__SCHEMA_NODES, [])
        head_indent = indent + 1
        tag_head    = Tag__Head(indent=head_indent, **attrs)

        for node in nodes:
            tag_name = node.get("tag")

            if tag_name == 'title':
                tag_head.title = self.collect_inner_text(node)                                  # Extract title text from text node nodes
            elif tag_name == 'link':
                tag_head.links.append(self.convert_to__tag__link(node))
            elif tag_name == 'meta':
                tag_head.elements.append(self.convert_to__tag(Tag__Base, node, head_indent))
            elif tag_name == 'style':
                style_element = self.convert_to__tag(Tag__Base, node, head_indent)              # For style tags, collect the CSS content from text nodes
                tag_head.elements.append(style_element)
            else:
                tag_head.elements.append(self.convert_to__tag(Tag__Base, node, head_indent))    # Handle any other head elements

        return tag_head

    def convert_to__tag__html(self, element):
        attrs = element.get("attrs", {})
        nodes = element.get(STRING__SCHEMA_NODES, [])
        lang  = attrs.get("lang")

        tag_html = Tag__Html(attributes=attrs, lang=lang, doc_type=False)

        head_found = False                                                      # Initialize head and body if not found
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
                print(f'Unexpected child of html tag: {tag_name}')                          # Log unexpected child elements of html

        if not head_found:                                                                  # Handle missing head or body (required for valid HTML structure)
            tag_html.head = Tag__Head(indent=tag_html.indent + 1)

        if not body_found:
            tag_html.body = Tag__Body(indent=tag_html.indent + 1)

        return tag_html

    def convert_to__tag__link(self, element):
        attrs    = element.get("attrs", {})
        tag_link = Tag__Link(**attrs)
        return tag_link
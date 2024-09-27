from osbot_utils.helpers.html.Dict_To_Html import HTML_SELF_CLOSING_TAGS
from osbot_utils.helpers.html.Tag__Base     import Tag__Base
from osbot_utils.helpers.html.Tag__Body     import Tag__Body
from osbot_utils.helpers.html.Tag__Head     import Tag__Head
from osbot_utils.helpers.html.Tag__Html     import Tag__Html
from osbot_utils.helpers.html.Tag__Link     import Tag__Link


class Dict_To_Tags:

    def __init__(self, root):
        self.root = root

    def convert(self):
        return self.convert_element(self.root)

    def convert_element(self, element):
        tag_name = element.get("tag"                )
        attrs    = element.get("attrs"      , {}    )
        children = element.get("children"   , []    )
        data     = element.get("data"       , ""    )
        if tag_name == 'html':
            return self.convert_to__tag__html(element)
        if tag_name == 'head':
            return self.convert_to__tag__head(element)
        if tag_name == 'link':
            return self.convert_to__tag__link(element)

    def convert_to__tag(self, target_tag, element, indent):
        tag_name   = element.get("tag"                )
        attrs      = element.get("attrs"      , {}    )
        children   = element.get("children"   , []    )
        data       = element.get("data"       , ''    )
        end_tag    = tag_name not in HTML_SELF_CLOSING_TAGS
        tag_indent = indent + 1
        tag_kwargs  = dict(tag_name  = tag_name    ,
                           attributes = attrs      ,
                           end_tag    = end_tag    ,
                           indent     = tag_indent ,
                           inner_html = data       )
        tag        = target_tag(**tag_kwargs)
        for child in children:
            child_tag = self.convert_to__tag(Tag__Base, child, tag_indent)
            tag.elements.append(child_tag)

        return tag

    def convert_to__tag__head(self, element, indent):
        attrs    = element.get("attrs"      , {}    )
        children = element.get("children"   , []    )
        print()
        head_indent = indent+1
        tag_head = Tag__Head(indent=head_indent, **attrs)
        for child in children:
            tag_name = child.get("tag"     )
            data     = child.get("data", "")
            if tag_name == 'title':
                tag_head.title = data
            elif tag_name == 'link':
                tag_head.links.append(self.convert_to__tag__link(child))
            elif tag_name == 'meta':
                tag_head.elements.append((self.convert_to__tag(Tag__Base, child, indent=head_indent)))
            elif tag_name == 'style':
                tag_head.elements.append((self.convert_to__tag(Tag__Base, child, indent=head_indent)))      # todo: add proper roundtrip of css data into Tag__Style (which already exists)
            else:
                print(f'[convert_to__tag__head] Unknown tag: {tag_name}')
        #pprint(tag_head.__locals__())
        return tag_head

    def convert_to__tag__html(self, element):
        attrs    = element.get("attrs"      , {}    )
        children = element.get("children"   , []    )
        tag_html = Tag__Html(**attrs)
        for child in children:
            tag_name = child.get("tag" )
            if tag_name == 'head':
                tag_html.head = self.convert_to__tag__head(child, tag_html.indent)
            elif tag_name == 'body':
                tag_html.body = self.convert_to__tag(Tag__Body, child, tag_html.indent)
            else:
                print(f'unknown tag: {tag_name}')
        return tag_html

    def convert_to__tag__link(self, element):
        attrs    = element.get("attrs", {})
        tag_link = Tag__Link(**attrs)
        return tag_link
from osbot_utils.helpers.html.Tag__Base import Tag__Base
from osbot_utils.helpers.html.Tag__Head import Tag__Head

ATTRIBUTES_NAMES__LINK = ['lang']


class Tag__Html(Tag__Base):
    doc_type: bool = True
    head    : Tag__Head
    lang    : str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.head.indent = self.indent + 1
        self.tag_name    = 'html'

    def render(self):
        self.elements = [self.head]
        self.attributes = self.attributes_values(*ATTRIBUTES_NAMES__LINK)
        if self.doc_type:
            html = "<!DOCTYPE html>\n"
        else:
            html = ""
        attributes = {}
        if self.lang:
            attributes['lang'] = self.lang

        html += self.render_element()
        return html



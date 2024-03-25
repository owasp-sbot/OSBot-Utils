from osbot_utils.helpers.html.Tag__Base import Tag__Base
from osbot_utils.helpers.html.Tag__Head import Tag__Head

class Tag__Html(Tag__Base):
    doc_type: bool = True
    head    : Tag__Head
    lang    : str

    def __init__(self):
        super().__init__()
        self.head.indent = self.indent + 1
        self.tag_name    = 'html'

    def render(self):
        elements = [self.head]
        if self.doc_type:
            html = "<!DOCTYPE html>\n"
        else:
            html = ""
        attributes = {}
        if self.lang:
            attributes['lang'] = self.lang

        html += self.render_element(attributes, elements)
        return html



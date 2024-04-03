from osbot_utils.helpers.html.Tag__Base import Tag__Base
from osbot_utils.helpers.html.Tag__Link import Tag__Link
from osbot_utils.utils.Dev import pprint


class Tag__Head(Tag__Base):
    title    : str
    links    : list[Tag__Link]
    meta     : list[Tag__Base]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag_name = 'head'

    def render(self):
        #elements   = []
        if self.title:
            title_element = Tag__Base(tag_name='title', inner_html=self.title, indent=self.indent + 1)
            self.elements.append(title_element)
        for link in self.links:
            link.indent  = self.indent + 1
            self.elements.append(link)
        #self.elements = elements
        html = self.render_element()
        return html
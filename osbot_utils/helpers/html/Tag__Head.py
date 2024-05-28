from typing import List

from osbot_utils.helpers.html.Tag__Base import Tag__Base
from osbot_utils.helpers.html.Tag__Link import Tag__Link
from osbot_utils.helpers.html.Tag__Style import Tag__Style
from osbot_utils.utils.Dev import pprint


class Tag__Head(Tag__Base):
    title    : str
    links    : List[Tag__Link]
    meta     : List[Tag__Base]
    style    : Tag__Style

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag_name = 'head'

    def add_css_bootstrap(self):
        link = Tag__Link(href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css", rel="stylesheet")
        self.links.append(link)
        return self

    def render(self):
        if self.title:
            title_element = Tag__Base(tag_name='title', inner_html=self.title, indent=self.indent + 1)
            self.elements.append(title_element)
        for link in self.links:
            link.indent  = self.indent + 1
            self.elements.append(link)
        if self.style.css():
            self.elements.append(self.style)
        html = self.render_element()
        return html
from osbot_utils.helpers.html.Tag__Base import Tag__Base
from osbot_utils.utils.Dev import pprint

ATTRIBUTES_NAMES__LINK = ['href', 'integrity', 'rel']

class Tag__Link(Tag__Base):
    end_tag    : bool = False
    tag_name   : str  = 'link'
    crossorigin: str
    href       : str
    rel        : str
    integrity  : str

    def render(self):
        self.attributes = self.attributes_values(*ATTRIBUTES_NAMES__LINK)

        return self.render_element()
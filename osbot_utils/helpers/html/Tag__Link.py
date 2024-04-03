from osbot_utils.helpers.html.Tag__Base import Tag__Base

ATTRIBUTES_NAMES__LINK = ['crossorigin', 'href', 'integrity', 'rel']

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
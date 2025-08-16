from osbot_utils.helpers.html.tags.Tag__Base import Tag__Base


class Tag__H(Tag__Base):
    def __init__(self, size, value):
        tag_name     = f'h{size}'
        inner_html   = value
        init__kwargs = dict(tag_name=tag_name, inner_html=inner_html)
        super().__init__(**init__kwargs)

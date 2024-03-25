from osbot_utils.helpers.html.Tag__Base import Tag__Base


class Tag__Head(Tag__Base):
    title    : str

    def __init__(self):
        super().__init__()
        self.tag_name = 'head'

    def render(self):
        elements = []

        html = self.render_element( {}, [])
        return html
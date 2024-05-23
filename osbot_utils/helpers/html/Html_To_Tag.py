from osbot_utils.helpers.html.Dict_To_Tags import Dict_To_Tags

from osbot_utils.helpers.html.Html_To_Dict import Html_To_Dict


class Html_To_Tag:

    def __init__(self,html):
        self.html_to_dict = Html_To_Dict(html)

    def __enter__(self):
        return self.convert()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def convert(self):
        html_dict = self.html_to_dict.convert()
        html_tag  = Dict_To_Tags(html_dict).convert()
        return html_tag

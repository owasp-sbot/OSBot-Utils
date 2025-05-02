from osbot_utils.helpers.html.Dict__To__Tags import Dict__To__Tags
from osbot_utils.helpers.html.Html__To__Dict import Html__To__Dict


class Html__To__Tag:

    def __init__(self,html):
        self.html_to_dict = Html__To__Dict(html)

    def __enter__(self):
        return self.convert()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def convert(self):
        html_dict = self.html_to_dict.convert()
        html_tag  = Dict__To__Tags(html_dict).convert()
        return html_tag

from osbot_utils.helpers.html.transformers.Html_Dict__To__Html_Tags import Html_Dict__To__Html_Tags
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict      import Html__To__Html_Dict


class Html__To__Html_Tag:

    def __init__(self,html):
        self.html_to_dict = Html__To__Html_Dict(html)

    def __enter__(self):
        return self.convert()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def convert(self):
        html_dict = self.html_to_dict.convert()
        html_tag  = Html_Dict__To__Html_Tags(html_dict).convert()
        return html_tag

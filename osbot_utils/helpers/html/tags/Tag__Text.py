from osbot_utils.helpers.html.transformers.Html__To__Html_Dict import STRING__SCHEMA_TEXT


class Tag__Text:
    def __init__(self, data=""):
        self.type = STRING__SCHEMA_TEXT
        self.data = data

    def render(self):
        return self.data
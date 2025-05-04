from osbot_utils.helpers.html.schemas.Schema__HTML_Document import Schema__HTML_Document
from osbot_utils.type_safe.Type_Safe                        import Type_Safe


class Html_Dict__To__Html_Document(Type_Safe):
    html__dict  : dict                   = None
    html__json  : Schema__HTML_Document = None

    def convert(self):
        return ""
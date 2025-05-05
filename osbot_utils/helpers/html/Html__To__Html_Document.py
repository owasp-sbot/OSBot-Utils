from osbot_utils.helpers.html.schemas.Schema__Html_Document import Schema__Html_Document
from osbot_utils.type_safe.Type_Safe import Type_Safe


class Html__To__Html_Document(Type_Safe):
    html: str
    html_dict    : dict
    html_document: Schema__Html_Document

    def convert(self):
        pass
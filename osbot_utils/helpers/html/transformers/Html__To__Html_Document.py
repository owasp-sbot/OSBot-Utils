from osbot_utils.helpers.html.transformers.Html_Dict__To__Html_Document  import Html_Dict__To__Html_Document
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict           import Html__To__Html_Dict
from osbot_utils.helpers.html.schemas.Schema__Html_Document              import Schema__Html_Document
from osbot_utils.type_safe.Type_Safe                                     import Type_Safe

class Html__To__Html_Document(Type_Safe):
    html: str
    html__dict    : dict
    html__document: Schema__Html_Document

    def convert(self) -> Schema__Html_Document:
        if self.html:
            html__dict =  Html__To__Html_Dict(self.html).convert()
            if html__dict:
                with Html_Dict__To__Html_Document(html__dict=html__dict).convert()  as html__document:
                    if html__document:
                        self.html__document = html__document
                        return html__document
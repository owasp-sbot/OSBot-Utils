from typing                                                         import Dict, Union, Any
from osbot_utils.helpers.html.Html__To__Html_Dict                   import STRING__SCHEMA_TEXT, STRING__SCHEMA_NODES
from osbot_utils.helpers.html.schemas.Schema__Html_Document         import Schema__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Node             import Schema__Html_Node
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data       import Schema__Html_Node__Data
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data__Type import Schema__Html_Node__Data__Type
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class Html_Dict__To__Html_Document(Type_Safe):
    html__dict    : dict                  = None
    html__document: Schema__Html_Document = None

    def convert(self):
        self.html__document = self.parse_html_dict(self.html__dict)
        return self.html__document

    def parse_html_dict(self, target: Dict[str, Any]) -> Schema__Html_Document:
        if not target or not isinstance(target, dict):
            raise ValueError("Invalid HTML dictionary structure")

        root_node = self.parse_node(target)
        return Schema__Html_Document(root_node=root_node)

    def parse_node(self, target: Dict[str, Any]) -> Union[Schema__Html_Node, Schema__Html_Node__Data]:

        if target.get('type') == STRING__SCHEMA_TEXT:                                           # Handle text nodes
            return Schema__Html_Node__Data(data = target.get('data', ''),
                                           type = Schema__Html_Node__Data__Type.TEXT)
        else:                                                                                   # Handle element nodes
            nodes = []
            for node in target.get(STRING__SCHEMA_NODES, []):
                nodes.append(self.parse_node(node))

            return Schema__Html_Node(attrs = target.get('attrs', {})           ,
                                     nodes = nodes                              ,
                                     tag   = target.get('tag', ''))
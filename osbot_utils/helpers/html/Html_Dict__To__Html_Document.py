from typing                                                         import Dict, Union, Any

from osbot_utils.helpers.html.Html__To__Html_Dict import STRING__SCHEMA_TEXT
from osbot_utils.helpers.html.schemas.Schema__HTML_Document         import Schema__HTML_Document
from osbot_utils.helpers.html.schemas.Schema__HTML_Node             import Schema__HTML_Node
from osbot_utils.helpers.html.schemas.Schema__HTML_Node__Data       import Schema__HTML_Node__Data
from osbot_utils.helpers.html.schemas.Schema__HTML_Node__Data__Type import Schema__HTML_Node__Data__Type
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class Html_Dict__To__Html_Document(Type_Safe):
    html__dict    : dict                  = None
    html__document: Schema__HTML_Document = None

    def convert(self):
        self.html__document = self.parse_html_dict(self.html__dict)
        return self.html__document

    def parse_html_dict(self, target: Dict[str, Any]) -> Schema__HTML_Document:                    # Parse the Html__To__Dict output
        if not target or not isinstance(target, dict):
            raise ValueError("Invalid HTML dictionary structure")

        children = []                                                                           # Parse root node and its children
        if target.get('tag'):                                                               # Root has a tag, treat it as a child
            root_child = self.parse_node(target)
            children.append(root_child)
        else:                                                                                  # Root doesn't have tag, parse children directly
            for child in target.get('children', []):
                children.append(self.parse_node(child))

        return Schema__HTML_Document(attrs    = target.get('attrs', {}),
                                     children = children)

    def parse_node(self, target: Dict[str, Any]) -> Union[Schema__HTML_Node, Schema__HTML_Node__Data]:

        if target.get('type') == STRING__SCHEMA_TEXT:                                           # Handle text nodes
            return Schema__HTML_Node__Data(data = target.get('data', ''),
                                           type = Schema__HTML_Node__Data__Type.TEXT)
        else:                                                                                   # Handle element nodes
            children = []
            for child in target.get('children', []):
                children.append(self.parse_node(child))

            return Schema__HTML_Node(attrs    = target.get('attrs', {})           ,
                                     children = children                              ,
                                     tag      = target.get('tag', ''))
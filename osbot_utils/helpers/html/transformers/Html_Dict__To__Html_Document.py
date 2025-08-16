from typing                                                         import Dict, Any
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict      import STRING__SCHEMA_TEXT, STRING__SCHEMA_NODES
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

        root_node = self.parse_node(target, position=-1)                                # Root has position -1
        return Schema__Html_Document(root_node=root_node)

    def parse_node(self, target: Dict[str, Any], position: int) -> Schema__Html_Node:   # Parse a node and separate child nodes from text nodes with positions

        if target.get('type') == STRING__SCHEMA_TEXT:                                   # This shouldn't happen at this level since we're parsing element nodes
            raise ValueError("Unexpected text node at element level")


        child_nodes = []                                                                # Create lists for child nodes and text nodes
        text_nodes  = []


        nodes_list = target.get(STRING__SCHEMA_NODES, [])                               # Process all nodes and assign positions
        for idx, node in enumerate(nodes_list):
            if node.get('type') == STRING__SCHEMA_TEXT:                                 # Create text node with position
                text_node = Schema__Html_Node__Data(data     = node.get('data', '')              ,
                                                    type     = Schema__Html_Node__Data__Type.TEXT,
                                                    position = idx                               )
                text_nodes.append(text_node)
            else:
                child_node = self.parse_node(node, position=idx)                        # Create element node with position
                child_nodes.append(child_node)

        return Schema__Html_Node(attrs       = target.get('attrs', {}),                 # Create the element node with separated lists
                                 child_nodes = child_nodes            ,
                                 text_nodes  = text_nodes             ,
                                 tag         = target.get('tag'  , ''),
                                 position    = position               )
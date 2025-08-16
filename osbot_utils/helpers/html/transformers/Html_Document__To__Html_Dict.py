from typing                                                     import Dict, Any, List, Union
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict  import STRING__SCHEMA_TEXT, STRING__SCHEMA_NODES, STRING__SCHEMA_TAG, STRING__SCHEMA_ATTRS
from osbot_utils.helpers.html.schemas.Schema__Html_Document     import Schema__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Node         import Schema__Html_Node
from osbot_utils.type_safe.Type_Safe                            import Type_Safe


class Html_Document__To__Html_Dict(Type_Safe):
    html__document : Schema__Html_Document = None
    html__dict     : dict                  = None

    def convert(self) -> dict:                                                  # Convert Schema__Html_Document back to html dict format
        if not self.html__document:
            raise ValueError("No document to convert")

        self.html__dict = self.node_to_dict(self.html__document.root_node)
        return self.html__dict

    def node_to_dict(self, node: Schema__Html_Node) -> Dict[str, Any]:          # Convert a Schema__Html_Node back to dict format, merging child and text nodes by position

        result = {  STRING__SCHEMA_TAG   : node.tag,                # Create the basic dict structure
                    STRING__SCHEMA_ATTRS : node.attrs,
                    STRING__SCHEMA_NODES : []}

        all_nodes = []                                              # Merge child_nodes and text_nodes back together based on position

        for child in node.child_nodes:                              # Add child nodes with their positions
            all_nodes.append((child.position, 'child', child))

        for text in node.text_nodes:                                # Add text nodes with their positions
            all_nodes.append((text.position, 'text', text))

        all_nodes.sort(key=lambda x: x[0])                          # Sort by position

        for position, node_type, node_obj in all_nodes:             # Build the nodes list in the correct order
            if node_type == 'text':
                text_dict = { 'type': STRING__SCHEMA_TEXT,          # Convert text node to dict
                              'data': node_obj.data      }
                result[STRING__SCHEMA_NODES].append(text_dict)
            else:
                child_dict = self.node_to_dict(node_obj)            # Recursively convert child node
                result[STRING__SCHEMA_NODES].append(child_dict)

        return result
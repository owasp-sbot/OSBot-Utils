from typing                                 import Dict, Any
from osbot_utils.base_classes.Type_Safe     import Type_Safe
from osbot_utils.helpers.xml.Xml__Element   import XML__Element
from osbot_utils.helpers.xml.Xml__File      import Xml__File


class Xml__File__To_Dict(Type_Safe):
    def to_dict(self, xml_file: Xml__File) -> Dict[str, Any]:   # Convert Xml__File to dictionary
        if not xml_file.root_element:
            return {}
        return self.element_to_dict(xml_file.root_element)

    def element_to_dict(self, element: XML__Element) -> Dict[str, Any]:    # Convert XML__Element to dictionary
        result = {}

        for key, attr in element.attributes.items():             # Convert attributes
            result[key] = attr.value

        child_nodes: Dict[str, Any] = {}                        # Process children
        text_content = []

        for child in element.children:
            if isinstance(child, str):
                text_content.append(child)
            else:
                if child.tag in child_nodes:                     # Handle child elements
                    if not isinstance(child_nodes[child.tag], list):
                        child_nodes[child.tag] = [child_nodes[child.tag]]
                    child_nodes[child.tag].append(self.element_to_dict(child))
                else:
                    child_nodes[child.tag] = self.element_to_dict(child)

        if text_content:                                        # Handle text content
            if child_nodes:
                result['_text'] = ' '.join(text_content)
            else:
                return ' '.join(text_content)

        result.update(child_nodes)
        return result
from typing                 import Dict, Any, Union
from xml.etree.ElementTree  import Element

from osbot_utils.base_classes.Type_Safe import Type_Safe

class XML_Attribute(Type_Safe):
    name     : str
    value    : str
    namespace: str

class XML_Element(Type_Safe):
    attributes: Dict[str, XML_Attribute]
    children  : Dict[str, Union[str, 'XML_Element']]


class Xml_To_Dict(Type_Safe):
    xml_data    : str             = None       # Input XML string
    root        : Element         = None       # Root ElementTree.Element
    namespaces  : Dict[str, str]               # XML namespaces
    xml_dict    : Dict[str, Any]               # Parsed XML as dictionary

    def setup(self) :
        from xml.etree.ElementTree import ParseError
        try:
            self.load_namespaces()
            self.load_root()

        except ParseError as e:
            raise ValueError(f"Invalid XML: {str(e)}")
        return self


    def load_namespaces(self):
        from xml.etree.ElementTree import iterparse
        from io import StringIO

        for event, elem in iterparse(StringIO(self.xml_data), events=("start-ns",)):
            self.namespaces[elem[0]] = elem[1]

    def load_root(self):
        from xml.etree.ElementTree import fromstring

        self.root = fromstring(self.xml_data)

    def element_to_dict(self, element: Element) -> Union[Dict[str, Any], str]:
        """Convert an ElementTree.Element to a dictionary"""
        result: Dict[str, Any] = {}


        if element.attrib:                                  # Handle attributes
            result.update(element.attrib)

        # Handle child elements
        child_nodes: Dict[str, Any] = {}
        for child in element:
            tag = child.tag                                 # Remove namespace prefix if present
            if '}' in tag:
                tag = tag.split('}', 1)[1]

            child_data = self.element_to_dict(child)

            if tag in child_nodes:
                if not isinstance(child_nodes[tag], list):
                    child_nodes[tag] = [child_nodes[tag]]
                child_nodes[tag].append(child_data)
            else:
                child_nodes[tag] = child_data

        # Handle text content
        text = element.text.strip() if element.text else ''
        if text:
            if child_nodes or result:
                result['_text'] = text
            else:
                return text
        elif not child_nodes and not result:                # Make sure we return text content even for empty nodes
            return text

        # Combine results
        if child_nodes:
            result.update(child_nodes)

        return result

    def parse(self) -> Dict[str, Any]:   # Convert parsed XML to dictionary
        self.xml_dict = self.element_to_dict(self.root)
        return self
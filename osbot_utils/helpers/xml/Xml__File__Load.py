from io                                     import StringIO
from typing                                 import List, Union, Dict
from xml.etree.ElementTree                  import iterparse, Element, fromstring, ParseError
from osbot_utils.type_safe.Type_Safe        import Type_Safe
from osbot_utils.helpers.xml.Xml__Attribute import Xml__Attribute
from osbot_utils.helpers.xml.Xml__Element   import XML__Element
from osbot_utils.helpers.xml.Xml__File      import Xml__File


class Xml__File__Load(Type_Safe):

    def load_from_string(self, xml_data: str) -> Xml__File:    # Create Xml__File from string
        xml_file = Xml__File(xml_data=xml_data)
        self.load_namespaces(xml_file)
        self.parse_xml      (xml_file)
        return xml_file

    def load_namespaces(self, xml_file: Xml__File):           # Extract namespaces from XML
        if not xml_file.xml_data:
            raise ValueError("XML data cannot be empty")

        for event, elem in iterparse(StringIO(xml_file.xml_data), events=("start-ns",)):
            prefix, uri = elem
            xml_file.namespaces[prefix] = uri

    def parse_xml(self, xml_file: Xml__File):                 # Parse XML into type-safe structure
        if not xml_file.xml_data:
            raise ValueError("XML data cannot be empty")

        try:
            root       = fromstring(xml_file.xml_data)
            namespaces = xml_file.namespaces
            xml_file.root_element = self.convert_element(namespaces,root)
        except ParseError as error:
            raise ValueError(f"Invalid XML: {str(error)}")

    def convert_element(self, namespaces: Dict[str,str], element: Element) -> XML__Element:
        attributes = self.convert_attributes(element)
        children: List[Union[str, XML__Element]] = []

        tag             = element.tag
        namespace        = ''
        namespace_prefix = ''

        if '}' in tag:
            namespace, tag = tag.split('}', 1)          # Split namespace and tag
            namespace = namespace[1:]                   # Remove the '{' prefix

            for prefix, uri in namespaces.items(): # Find prefix for this namespace
                if uri == namespace:
                    namespace_prefix = prefix
                    break

        # Handle text content
        if element.text and element.text.strip():
            children.append(element.text.strip())

        # Process child elements
        for child in element:
            child_element = self.convert_element(namespaces, child)
            children.append(child_element)

            if child.tail and child.tail.strip():
                children.append(child.tail.strip())

        return XML__Element(tag=tag,
                          namespace=namespace,
                          namespace_prefix=namespace_prefix,
                          attributes=attributes,
                          children=children)

    def convert_attributes(self, element: Element) -> Dict[str, Xml__Attribute]:    # Convert element attributes
        attributes = {}
        for key, value in element.attrib.items():
            if '}' in key:                                        # Handle namespaced attributes
                namespace, name = key.split('}', 1)
                namespace = namespace[1:]                         # Remove the '{' prefix
            else:
                namespace = ''
                name = key

            attribute = Xml__Attribute(
                name=name,
                value=value,
                namespace=namespace
            )
            attributes[key] = attribute
        return attributes
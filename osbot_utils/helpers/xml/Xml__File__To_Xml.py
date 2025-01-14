from typing                                 import Optional
from xml.etree.ElementTree                  import Element, SubElement, tostring
from xml.dom                                import minidom
from osbot_utils.type_safe.Type_Safe        import Type_Safe
from osbot_utils.helpers.xml.Xml__Element   import XML__Element
from osbot_utils.helpers.xml.Xml__File      import Xml__File

class Xml__File__To_Xml(Type_Safe):

    def convert_to_xml(self, xml_file: Xml__File, pretty_print: bool = True) -> str:
        if not xml_file.root_element:
            raise ValueError("XML file must have a root element")

        # Create XML element tree
        root = self.create_element(xml_file.root_element, xml_file.namespaces)

        # Add all namespace declarations to root element
        for prefix, uri in xml_file.namespaces.items():
            if prefix == '':
                root.set('xmlns', uri)
            else:
                root.set(f'xmlns:{prefix}', uri)

        # Convert to string
        xml_string = tostring(root, encoding='unicode', method='xml')

        # Pretty print if requested
        if pretty_print:
            return self.pretty_print(xml_string)
        return xml_string

    def create_element(self, xml_element: XML__Element, namespaces: Optional[dict] = None, parent: Optional[Element] = None) -> Element:
        # Create tag with namespace if applicable
        tag = xml_element.tag
        if xml_element.namespace_prefix:
            tag = f"{xml_element.namespace_prefix}:{tag}"
        # Don't add namespace URI for default namespace - let it be inherited

        # Create new element or sub-element
        if parent is not None:
            element = SubElement(parent, tag)
        else:
            element = Element(tag)

        # Add attributes including namespace declarations
        for attr_key, attr in xml_element.attributes.items():
            if attr.namespace:
                attr_name = f"{{{attr.namespace}}}{attr.name}"
            else:
                attr_name = attr.name
            element.set(attr_name, attr.value)

        # Process children
        text_parts = []
        for child in xml_element.children:
            if isinstance(child, str):
                text_parts.append(child)
            elif isinstance(child, XML__Element):
                self.create_element(child, namespaces, element)

        # Set text content if any
        if text_parts:
            element.text = ''.join(text_parts)

        return element

    def pretty_print(self, xml_string: str) -> str:
        """Format XML string with proper indentation."""
        parsed = minidom.parseString(xml_string)
        pretty_xml = parsed.toprettyxml(indent='  ').rstrip() + '\n'
        # Remove empty lines (common issue with toprettyxml)
        return '\n'.join(line for line in pretty_xml.split('\n') if line.strip())
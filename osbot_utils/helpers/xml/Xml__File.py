from typing                                 import Dict
from osbot_utils.type_safe.Type_Safe        import Type_Safe
from osbot_utils.helpers.xml.Xml__Element   import XML__Element

class Xml__File(Type_Safe):
    xml_data    : str                           # Raw XML content
    root_element: XML__Element                  # Parsed root element
    namespaces  : Dict[str, str]                # XML namespace mappings


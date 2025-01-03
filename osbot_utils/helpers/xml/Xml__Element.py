from typing                                 import Dict, List, Union
from osbot_utils.type_safe.Type_Safe     import Type_Safe
from osbot_utils.helpers.xml.Xml__Attribute import Xml__Attribute

class XML__Element(Type_Safe):
    tag             : str                                   # Element's local name
    namespace       : str                                   # Element's namespace URI
    namespace_prefix: str                                   # Element's namespace prefix
    attributes      : Dict[str, Xml__Attribute]             # Element attributes
    children        : List[Union[str, 'XML__Element']]      # Child elements/text

    # def qualified_name(self) -> str:                        # Get fully qualified name with prefix
    #     if self.namespace_prefix:
    #         return f"{self.namespace_prefix}:{self.tag}"
    #     return self.tag
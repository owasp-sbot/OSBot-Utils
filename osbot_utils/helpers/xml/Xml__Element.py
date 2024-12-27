from typing                                  import Dict, List, Union
from osbot_utils.base_classes.Type_Safe      import Type_Safe
from osbot_utils.helpers.xml.Xml__Attribute  import Xml__Attribute

class XML__Element(Type_Safe):
    tag       : str
    attributes: Dict[str, Xml__Attribute]
    children  : List[Union[str, 'XML__Element']]
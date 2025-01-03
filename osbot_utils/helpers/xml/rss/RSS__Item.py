from typing                                         import Dict, List, Any
from osbot_utils.type_safe.Type_Safe             import Type_Safe
from osbot_utils.helpers.Guid                       import Guid
from osbot_utils.helpers.xml.rss.RSS__Enclosure     import RSS__Enclosure

class RSS__Item(Type_Safe):
    title       : str
    link        : str
    description : str
    guid        : Guid
    pubDate     : str
    creator     : str
    categories  : List[str]
    enclosure   : RSS__Enclosure = None
    content     : Dict[str, Any]
    thumbnail   : Dict[str, Any]
    extensions  : Dict[str, Any]

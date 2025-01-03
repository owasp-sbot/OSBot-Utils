from typing                                     import Dict, Any
from osbot_utils.type_safe.Type_Safe         import Type_Safe
from osbot_utils.helpers.xml.rss.RSS__Channel   import RSS__Channel

DEFAULT__RSS_FEED__VERSION = "2.0"

class RSS__Feed(Type_Safe):
    version    : str           = DEFAULT__RSS_FEED__VERSION
    channel    : RSS__Channel  = None
    namespaces : Dict[str, str]
    extensions : Dict[str, Any]

from typing                                     import Any, Dict, List
from osbot_utils.type_safe.Type_Safe            import Type_Safe
from osbot_utils.helpers.xml.rss.RSS__Image     import RSS__Image
from osbot_utils.helpers.xml.rss.RSS__Item      import RSS__Item


class RSS__Channel(Type_Safe):
    description     : str
    extensions      : Dict[str, Any]
    image           : RSS__Image         = None
    items           : List[RSS__Item]
    language        : str
    last_build_date : str
    link            : str
    title           : str
    update_frequency: str
    update_period   : str

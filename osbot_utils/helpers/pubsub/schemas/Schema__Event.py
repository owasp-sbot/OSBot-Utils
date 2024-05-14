from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.Misc import random_guid


class Schema__Event(Kwargs_To_Self):
    event_id     : str
    topic_id     : str
    event_data   : dict
    event_message: str
    event_target : str
    event_type   : str
    timestamp    : int
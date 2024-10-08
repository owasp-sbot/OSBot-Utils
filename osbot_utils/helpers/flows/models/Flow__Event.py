from osbot_utils.base_classes.Type_Safe import Type_Safe

class Flow__Event(Type_Safe):
    event_type  : str
    event_source: object
    event_data  : dict
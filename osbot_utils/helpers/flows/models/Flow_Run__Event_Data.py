import logging
from osbot_utils.type_safe.Type_Safe import Type_Safe

class Flow_Run__Event_Data(Type_Safe):
    data        : dict
    event_source: str
    #flow_id     : str = None           # todo: add support for capturing the actual flow_idq
    flow_name   : str = None
    flow_run_id : str = None
    log_level   : int = logging.INFO
    task_name   : str = None
    task_run_id : str = None
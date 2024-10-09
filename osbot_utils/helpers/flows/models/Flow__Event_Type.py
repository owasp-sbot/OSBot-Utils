from osbot_utils.base_classes.Type_Safe import Type_Safe

class Flow__Event_Type(Type_Safe):
    FLOW_MESSAGE: str = 'flow_message'
    FLOW_START  : str = 'flow_start'
    FLOW_STOP   : str = 'flow_stop'
    NEW_ARTIFACT: str = 'new_artifact'
    NEW_RESULT  : str = 'new_result'
    TASK_START  : str = 'task_start'
    TASK_STOP   : str = 'task_stop'
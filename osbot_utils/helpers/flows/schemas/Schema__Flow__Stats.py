from typing                                                 import Dict
from osbot_utils.helpers.duration.schemas.Schema__Duration  import Schema__Duration
from osbot_utils.helpers.flows.schemas.Schema__Flow__Status import Schema__Flow__Status
from osbot_utils.helpers.flows.schemas.Schema__Task__Stats  import Schema__Task__Stats
from osbot_utils.type_safe.Type_Safe                        import Type_Safe


class Schema__Flow__Stats(Type_Safe):
    duration     : Schema__Duration                         # How long the flow took to execute
    error_message: str                             =  None  # Error message if flow failed
    failed_tasks : int                                      # Number of failed tasks
    flow_id      : str                                      # Unique identifier for the flow
    flow_name    : str                                      # Name of the flow
    status       : Schema__Flow__Status                     # 'completed', 'failed', 'running'
    tasks_stats  : Dict[str, Schema__Task__Stats]           # Map of task_id to task stats
    total_tasks  : int                                      # Total number of tasks executed

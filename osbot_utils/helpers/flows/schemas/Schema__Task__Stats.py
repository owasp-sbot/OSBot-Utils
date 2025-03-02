from osbot_utils.helpers.duration.schemas.Schema__Duration  import Schema__Duration
from osbot_utils.helpers.flows.schemas.Schema__Flow__Status import Schema__Flow__Status
from osbot_utils.type_safe.Type_Safe                        import Type_Safe


class Schema__Task__Stats(Type_Safe):
    task_id        : str                        # Unique identifier for the task
    task_name      : str                        # Name of the task
    execution_order: int                        # Order in which the task was executed
    duration       : Schema__Duration           # How long the task took to execute
    status         : Schema__Flow__Status       # 'completed', 'failed', 'running'
    parent_flow_id : str                        # ID of the flow that contains this task
    error_message  : str           = None       # Error message if task failed
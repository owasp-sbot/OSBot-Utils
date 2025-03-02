from enum import Enum

class Schema__Flow__Status(Enum):
    COMPLETED: str = 'completed'
    FAILED   : str = 'failed'
    STOPPED  : str = 'stopped'
    RUNNING  : str = 'running'
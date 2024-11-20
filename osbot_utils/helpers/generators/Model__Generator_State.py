from enum import Enum

class Model__Generator_State(Enum):                                         # Enum representing possible states of a generator
    CREATED   : str = "created"                                             # Initial state when the generator is created
    RUNNING   : str = "running"                                             # State when the generator is actively running
    STOPPING  : str = "stopping"                                            # State when the generator is in the process of stopping
    STOPPED   : str = "stopped"                                             # State when the generator is fully stopped
    COMPLETED : str = "completed"                                           # State when the generator has completed its execution
    ERROR     : str = "error"                                               # State when the generator encounters an error


from enum import Enum


class Enum__Call_Graph__Node_Type(str, Enum):                                                       # Node type identifier
    FUNCTION = 'function'
    METHOD   = 'method'
    CLASS    = 'class'
    MODULE   = 'module'
from enum import Enum


class Enum__Call_Graph__Edge_Type(str, Enum):                                        # Edge type identifier
    # Structural relationships
    CONTAINS = 'contains'                                                            # Class contains method/function

    # Behavioral relationships
    CALLS    = 'calls'                                                               # Direct function call
    SELF     = 'self'                                                                # self.method() call within class
    CHAIN    = 'chain'                                                               # obj.attr.method() chained call

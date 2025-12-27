"""
Schema for Call Tree Node - hierarchical execution structure
"""

from typing                              import List
from osbot_utils.type_safe.Type_Safe     import Type_Safe


class Schema__Call_Tree_Node(Type_Safe):                                         # Hierarchical call tree node
    name        : str                            = ''
    start_ns    : int                            = 0
    end_ns      : int                            = 0
    duration_ns : int                            = 0
    duration_ms : float                          = 0.0
    self_ns     : int                            = 0                              # Exclusive time (minus children)
    self_ms     : float                          = 0.0
    depth       : int                            = 0
    call_index  : int                            = 0                              # Position in call sequence
    children    : List['Schema__Call_Tree_Node']                                  # Type_Safe auto-initializes

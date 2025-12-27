"""
Schema for Full Export - complete timestamp collection export
"""

from typing                                                                              import List
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Export_Metadata        import Schema__Export_Metadata
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Export_Entry           import Schema__Export_Entry
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Export_Method_Timing   import Schema__Export_Method_Timing
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Call_Tree_Node         import Schema__Call_Tree_Node


class Schema__Export_Full(Type_Safe):                                            # Complete export of timestamp collection
    metadata       : Schema__Export_Metadata
    entries        : List[Schema__Export_Entry]
    method_timings : List[Schema__Export_Method_Timing]
    call_tree      : List[Schema__Call_Tree_Node]

# osbot_utils/helpers/ast/call_flow/schemas/Schema__Call_Graph__Node.py

from typing                                                                          import List
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Node_Type  import Enum__Call_Graph__Node_Type
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label   import Safe_Str__Label
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text         import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path    import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.core.Safe_UInt                                 import Safe_UInt

# todo: improve the types for some of these attributes like: full_name, module
#       see if Safe_Str__Text  is too restrictive for source_code
class Schema__Call_Graph__Node(Type_Safe):                                           # Single node in call graph
    node_id      : Node_Id                                                           # Unique node identifier
    name         : Safe_Str__Label                                                   # Short display name (e.g., 'process')
    full_name    : Safe_Str__Label                                                   # Fully qualified name (e.g., 'MyClass.process')
    node_type    : Enum__Call_Graph__Node_Type                                       # 'function', 'method', 'class'
    module       : Safe_Str__Label                                                   # Source module path
    file_path    : Safe_Str__File__Path                                              # File where defined (if known)
    depth        : Safe_UInt                                                         # Distance from entry point
    calls        : List[Node_Id]                                                     # Outgoing call targets (node_ids)
    called_by    : List[Node_Id]                                                     # Incoming callers (node_ids)
    source_code  : Safe_Str__Text                                                    # Source code snippet (optional)
    line_number  : Safe_UInt                                                         # Line number in file
    is_entry     : bool                         = False                              # Is this the entry point?
    is_external  : bool                         = False                              # External/unresolved call?
    is_recursive : bool                         = False                              # Calls itself?
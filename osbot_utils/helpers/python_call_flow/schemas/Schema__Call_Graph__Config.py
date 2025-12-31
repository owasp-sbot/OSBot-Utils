from typing                                                                          import List
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label   import Safe_Str__Label
from osbot_utils.type_safe.primitives.core.Safe_UInt                                 import Safe_UInt

# todo: module_allowlist should be a dedicated Safe_Str_* primitive ,not List[Safe_Str__Label]
class Schema__Call_Graph__Config(Type_Safe):                                         # Configuration for call graph traversal
    # Depth Control
    max_depth              : Safe_UInt             = Safe_UInt(5)                    # Maximum traversal depth

    # Method Visibility
    include_private        : bool                  = True                            # Include _private methods
    include_dunder         : bool                  = False                           # Include __dunder__ methods

    # Scope Control
    include_stdlib         : bool                  = False                           # Follow into Python stdlib
    include_external       : bool                  = False                           # Follow into pip packages

    # Fine-grained Scope
    module_allowlist       : List[Safe_Str__Label]                                   # ONLY follow these module prefixes
    module_blocklist       : List[Safe_Str__Label]                                   # NEVER follow these modules
    class_allowlist        : List[Safe_Str__Label]                                   # ONLY follow these classes
    class_blocklist        : List[Safe_Str__Label]                                   # NEVER follow these classes

    # Analysis Options
    resolve_self_calls     : bool                  = True                            # Resolve self.method() calls
    capture_source         : bool                  = False                           # Store source code in nodes
    create_external_nodes  : bool                  = True                            # Create placeholders for external

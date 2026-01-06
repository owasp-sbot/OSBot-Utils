# ═══════════════════════════════════════════════════════════════════════════════
# Schema for extracted call information
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__Extracted__Call(Type_Safe):                                        # Info about an extracted call from AST
    call_name       : str  = ''                                                  # Name of the call (e.g., 'method', 'func')
    full_expression : str  = ''                                                  # Full expression (e.g., 'self.method', 'obj.attr.func')
    line_number     : int  = 0                                                   # Line number in source
    is_self_call    : bool = False                                               # Is this a self.method() call?
    is_chain_call   : bool = False                                               # Is this a chain call (obj.attr.method())?
    is_conditional  : bool = False                                               # Is this inside an if/else?
    receiver        : str  = ''                                                  # The receiver object (e.g., 'self', 'obj')

# ═══════════════════════════════════════════════════════════════════════════════
# AST Visitor for extracting calls
# ═══════════════════════════════════════════════════════════════════════════════
import ast
from typing                                                               import List
from osbot_utils.helpers.python_call_flow.schemas.Schema__Extracted__Call import Schema__Extracted__Call


class Call_Extractor(ast.NodeVisitor):                                           # AST visitor to extract function/method calls
    def __init__(self):
        self.calls          : List[Schema__Extracted__Call] = []
        self.in_conditional : bool                          = False

    def visit_If(self, node):                                                    # Track conditional context
        old_conditional     = self.in_conditional
        self.in_conditional = True
        self.generic_visit(node)
        self.in_conditional = old_conditional

    def visit_Call(self, node):                                                  # Extract call information
        call_info = Schema__Extracted__Call(line_number    = node.lineno        ,
                                            is_conditional = self.in_conditional)

        if isinstance(node.func, ast.Attribute):                                 # Method call: obj.method() or self.method()
            call_info.call_name = node.func.attr

            if isinstance(node.func.value, ast.Name):                            # Simple attribute: self.method() or obj.method()
                call_info.receiver        = node.func.value.id
                call_info.full_expression = f"{node.func.value.id}.{node.func.attr}"
                call_info.is_self_call    = node.func.value.id == 'self'

            elif isinstance(node.func.value, ast.Attribute):                     # Chain: obj.attr.method()
                call_info.is_chain_call   = True
                call_info.full_expression = self._get_full_attr_chain(node.func)

        elif isinstance(node.func, ast.Name):                                    # Direct function call: func()
            call_info.call_name       = node.func.id
            call_info.full_expression = node.func.id

        if call_info.call_name:
            self.calls.append(call_info)

        self.generic_visit(node)

    def _get_full_attr_chain(self, node) -> str:                                 # Build full attribute chain string
        parts = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        return '.'.join(reversed(parts))

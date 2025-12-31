from typing                                                                         import List
from osbot_utils.helpers.ast.nodes.Ast_Module                                       import Ast_Module
from osbot_utils.helpers.ast.Ast_Visit                                              import Ast_Visit
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


class Call_Flow__AST__Extractor(Type_Safe):                                          # Extracts function calls from source using AST

    def extract_calls(self, func) -> List:                                           # Extract all Ast_Call nodes from function
        try:
            ast_module = Ast_Module(func)                                            # Parse function with AST helpers
        except Exception:
            return []                                                                # Can't get source, return empty

        calls = []
        with Ast_Visit(ast_module) as visitor:
            visitor.capture_calls()                                                  # Enable call capture
            visitor.visit()                                                          # Execute visitor

            captured = visitor.captured_nodes()
            calls    = captured.get('Ast_Call', [])

        return calls

    def can_parse(self, func) -> bool:                                               # Check if function source can be parsed
        try:
            Ast_Module(func)
            return True
        except Exception:
            return False

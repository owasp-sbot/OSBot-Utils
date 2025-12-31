import inspect
from typing                                                                         import Optional, Any
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call__Info                import Schema__Call__Info
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Config        import Schema__Call_Graph__Config
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type import Enum__Call_Graph__Edge_Type
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label  import Safe_Str__Label
from osbot_utils.type_safe.primitives.core.Safe_UInt                                import Safe_UInt


class Call_Flow__Call__Resolver(Type_Safe):                                          # Resolves AST call nodes to call information
    config : Schema__Call_Graph__Config                                              # Configuration for resolution

    def resolve(self, call, class_context: type = None) -> Optional[Schema__Call__Info]:  # Resolve Ast_Call to Schema__Call__Info
        call_name = self.extract_call_name(call)
        if not call_name:
            return None

        line_number = self.extract_line_number(call)
        func_node   = self.extract_func_node(call)
        func_type   = type(func_node).__name__ if func_node else ''

        if func_type == 'Ast_Attribute':                                             # Check for attribute access pattern
            call_info = self.resolve_attribute_call(func_node, call_name, class_context, line_number)
            if call_info:
                return call_info

        if func_type == 'Ast_Name':                                                  # Direct call: func()
            return Schema__Call__Info(
                name        = Safe_Str__Label(call_name)                             ,
                edge_type   = Enum__Call_Graph__Edge_Type.CALLS                      ,
                resolved    = None                                                   ,
                class_ref   = None                                                   ,
                line_number = Safe_UInt(line_number)                                 ,
            )

        return Schema__Call__Info(                                                   # Default to chain for anything else
            name        = Safe_Str__Label(call_name)                                 ,
            edge_type   = Enum__Call_Graph__Edge_Type.CHAIN                          ,
            resolved    = None                                                       ,
            class_ref   = None                                                       ,
            line_number = Safe_UInt(line_number)                                     ,
        )

    def resolve_attribute_call(self, func_node, call_name: str,                      # Resolve obj.method() pattern
                               class_context: type, line_number: int) -> Optional[Schema__Call__Info]:
        try:
            value = func_node.value()
            if type(value).__name__ == 'Ast_Name' and value.id() == 'self':
                if class_context and self.config.resolve_self_calls:                 # This is self.method()
                    attr_name = func_node.node.attr                                  # Access raw AST node for attr name
                    resolved  = self.resolve_self_method(attr_name, class_context)

                    return Schema__Call__Info(
                        name        = Safe_Str__Label(attr_name)                     ,
                        edge_type   = Enum__Call_Graph__Edge_Type.SELF               ,
                        resolved    = resolved                                       ,
                        class_ref   = class_context                                  ,
                        line_number = Safe_UInt(line_number)                         ,
                    )
            else:                                                                    # obj.method() - chain call
                return Schema__Call__Info(
                    name        = Safe_Str__Label(call_name)                         ,
                    edge_type   = Enum__Call_Graph__Edge_Type.CHAIN                  ,
                    resolved    = None                                               ,
                    class_ref   = None                                               ,
                    line_number = Safe_UInt(line_number)                             ,
                )
        except Exception:
            pass

        return None

    def resolve_self_method(self, method_name: str,                                  # Resolve self.method() to actual method
                            class_context: type) -> Optional[Any]:
        if hasattr(class_context, method_name):
            return getattr(class_context, method_name)

        for base in inspect.getmro(class_context)[1:]:                               # Check base classes
            if hasattr(base, method_name):
                return getattr(base, method_name)

        return None

    def extract_call_name(self, call) -> Optional[str]:                              # Extract call name from Ast_Call
        try:
            return call.name()                                                       # Built-in resolution from Ast_Call
        except Exception:
            return None

    def extract_func_node(self, call) -> Optional[Any]:                              # Extract func node from Ast_Call
        try:
            return call.func()
        except Exception:
            return None

    def extract_line_number(self, call) -> int:                                      # Extract line number from Ast_Call
        try:
            return call.node.lineno if hasattr(call, 'node') else 0
        except Exception:
            return 0

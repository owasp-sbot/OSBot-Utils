from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Config        import Schema__Call_Graph__Config
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Node          import Schema__Call_Graph__Node
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Node_Type import Enum__Call_Graph__Node_Type
from osbot_utils.helpers.python_call_flow.Call_Flow__Node__Registry                 import Call_Flow__Node__Registry
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label  import Safe_Str__Label
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path   import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.core.Safe_UInt                                import Safe_UInt


class Call_Flow__Node__Factory(Type_Safe):                                           # Factory for creating Schema__Call_Graph__Node instances
    config   : Schema__Call_Graph__Config                                            # Configuration for node creation
    registry : Call_Flow__Node__Registry                                             # Registry for metadata extraction

    def create_class_node(self, cls: type, depth: int) -> Schema__Call_Graph__Node:  # Create node for a class
        full_name   = self.registry.qualified_name(cls)
        short_name  = self.registry.short_name(cls)
        module      = self.registry.module_name(cls)
        file_path   = self.registry.file_path(cls)
        line_number = self.registry.line_number(cls)

        return Schema__Call_Graph__Node(
            node_id     = Node_Id(Obj_Id())                                          ,
            name        = Safe_Str__Label(short_name)                                ,
            full_name   = Safe_Str__Label(full_name)                                 ,
            node_type   = Enum__Call_Graph__Node_Type.CLASS                          ,
            module      = Safe_Str__Label(module)                                    ,
            file_path   = Safe_Str__File__Path(file_path) if file_path else Safe_Str__File__Path(''),
            depth       = Safe_UInt(depth)                                           ,
            line_number = Safe_UInt(line_number)                                     ,
        )

    def create_method_node(self, func, depth: int,                                   # Create node for method or function
                           is_method: bool = False) -> Schema__Call_Graph__Node:
        full_name   = self.registry.qualified_name(func)
        short_name  = self.registry.short_name(func)
        module      = self.registry.module_name(func)
        file_path   = self.registry.file_path(func)
        line_number = self.registry.line_number(func)
        node_type   = Enum__Call_Graph__Node_Type.METHOD if is_method else Enum__Call_Graph__Node_Type.FUNCTION

        source = ''
        if self.config.capture_source:
            source = self.registry.source_code(func)
            source = source[:4000] if source else ''                                 # Truncate long source

        return Schema__Call_Graph__Node(
            node_id     = Node_Id(Obj_Id())                                          ,
            name        = Safe_Str__Label(short_name)                                ,
            full_name   = Safe_Str__Label(full_name)                                 ,
            node_type   = node_type                                                  ,
            module      = Safe_Str__Label(module)                                    ,
            file_path   = Safe_Str__File__Path(file_path) if file_path else Safe_Str__File__Path(''),
            depth       = Safe_UInt(depth)                                           ,
            source_code = Safe_Str__Text(source) if source else Safe_Str__Text('')   ,
            line_number = Safe_UInt(line_number)                                     ,
        )

    def create_function_node(self, func, depth: int) -> Schema__Call_Graph__Node:    # Create node for standalone function
        return self.create_method_node(func, depth, is_method=False)

    def create_external_node(self, call_name: str, depth: int) -> Schema__Call_Graph__Node:  # Create placeholder for external call
        short_name = call_name.split('.')[-1] if '.' in call_name else call_name

        return Schema__Call_Graph__Node(
            node_id     = Node_Id(Obj_Id())                                          ,
            name        = Safe_Str__Label(short_name)                                ,
            full_name   = Safe_Str__Label(call_name)                                 ,
            node_type   = Enum__Call_Graph__Node_Type.FUNCTION                       ,
            module      = Safe_Str__Label('')                                        ,
            file_path   = Safe_Str__File__Path('')                                   ,
            depth       = Safe_UInt(depth)                                           ,
            is_external = True                                                       ,
        )

    def create_module_node(self, module, depth: int) -> Schema__Call_Graph__Node:    # Create node for a module
        full_name  = self.registry.qualified_name(module)
        short_name = self.registry.short_name(module)
        file_path  = self.registry.file_path(module)

        return Schema__Call_Graph__Node(
            node_id     = Node_Id(Obj_Id())                                          ,
            name        = Safe_Str__Label(short_name)                                ,
            full_name   = Safe_Str__Label(full_name)                                 ,
            node_type   = Enum__Call_Graph__Node_Type.MODULE                         ,
            module      = Safe_Str__Label(full_name)                                 ,
            file_path   = Safe_Str__File__Path(file_path) if file_path else Safe_Str__File__Path(''),
            depth       = Safe_UInt(depth)                                           ,
        )

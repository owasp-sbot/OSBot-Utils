import inspect
from typing                                                                         import Dict, Optional
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                   import Node_Id


class Call_Flow__Node__Registry(Type_Safe):                                          # Manages qualified name → Node_Id mapping
    name_to_node_id : Dict[str, Node_Id]                                             # qualified_name → Node_Id

    def reset(self):                                                                 # Clear all registrations
        self.name_to_node_id = {}

    def register(self, full_name: str, node_id: Node_Id):                            # Register a node mapping
        self.name_to_node_id[full_name] = node_id

    def lookup(self, full_name: str) -> Optional[Node_Id]:                           # Lookup node by qualified name
        return self.name_to_node_id.get(full_name)

    def exists(self, full_name: str) -> bool:                                        # Check if name is registered
        return full_name in self.name_to_node_id

    def qualified_name(self, target) -> str:                                         # Get fully qualified name for target
        if hasattr(target, '__qualname__'):
            module = getattr(target, '__module__', '')
            return f"{module}.{target.__qualname__}" if module else target.__qualname__
        return str(target)

    def short_name(self, target) -> str:                                             # Get short name (just the name)
        if hasattr(target, '__name__'):
            return target.__name__
        return str(target).split('.')[-1]

    def module_name(self, target) -> str:                                            # Get module name
        return getattr(target, '__module__', '')

    def file_path(self, target) -> str:                                              # Get file path for target
        try:
            return inspect.getfile(target)
        except (TypeError, OSError):
            return ''

    def line_number(self, target) -> int:                                            # Get line number for target
        try:
            _, line_number = inspect.getsourcelines(target)
            return line_number
        except (TypeError, OSError):
            return 0

    def source_code(self, target) -> str:                                            # Get source code for target
        try:
            return inspect.getsource(target)
        except (TypeError, OSError):
            return ''

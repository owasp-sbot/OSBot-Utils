import inspect
import sys
from typing                                                                          import Dict, Optional, Any
from osbot_utils.helpers.ast.nodes.Ast_Module                                        import Ast_Module
from osbot_utils.helpers.ast.Ast_Visit                                               import Ast_Visit
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph                 import Schema__Call_Graph
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Config         import Schema__Call_Graph__Config
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Edge           import Schema__Call_Graph__Edge
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Node           import Schema__Call_Graph__Node
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Node_Type  import Enum__Call_Graph__Node_Type
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type  import Enum__Call_Graph__Edge_Type
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                   import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                    import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                     import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label   import Safe_Str__Label
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text         import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path    import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.core.Safe_UInt                                 import Safe_UInt


class Call_Flow__Analyzer(Type_Safe):                                                # Analyzes Python code to extract call graphs
    config          : Schema__Call_Graph__Config                                     # Traversal configuration
    graph           : Schema__Call_Graph                                             # The resulting call graph
    name_to_node_id : Dict[str, Node_Id]                                             # qualified_name → Node_Id mapping
    visited_methods : Dict[str, bool]                                                # Track analyzed methods
    class_context   : Dict[str, type]                                                # Track class for self resolution

    def analyze(self, target) -> Schema__Call_Graph:                                 # Main entry point - analyze a function/class/module
        self.reset_state()
        self.initialize_graph(target)

        if inspect.isclass(target):
            self.analyze_class(target, depth=0)
        elif inspect.isfunction(target) or inspect.ismethod(target):
            self.analyze_function(target, depth=0)
        else:
            raise ValueError(f"Cannot analyze target of type: {type(target)}")

        return self.graph

    def reset_state(self):                                                           # Reset internal state for fresh analysis
        self.name_to_node_id = {}
        self.visited_methods = {}
        self.class_context   = {}
        self.graph           = Schema__Call_Graph()

    def initialize_graph(self, target):                                              # Set up graph metadata
        target_name             = self.get_qualified_name(target)
        self.graph.graph_id     = Graph_Id(Obj_Id())
        self.graph.name         = Safe_Str__Label(target_name)
        self.graph.config       = self.config

    def register_node(self, full_name: str, node_id: Node_Id):                       # Register a node in the name→id mapping
        self.name_to_node_id[full_name] = node_id

    def lookup_node_id(self, full_name: str) -> Optional[Node_Id]:                   # Lookup a node by qualified name
        return self.name_to_node_id.get(full_name)

    def get_qualified_name(self, target) -> str:                                     # Get fully qualified name for target
        if hasattr(target, '__qualname__'):
            module = getattr(target, '__module__', '')
            return f"{module}.{target.__qualname__}" if module else target.__qualname__
        return str(target)

    def analyze_class(self, cls: type, depth: int) -> Optional[Node_Id]:             # Analyze a class, creating class node and method nodes
        if depth > int(self.config.max_depth):
            return None

        full_name = self.get_qualified_name(cls)

        existing_id = self.lookup_node_id(full_name)                                 # Check if already analyzed
        if existing_id:
            return existing_id

        class_node = self.create_class_node(cls, depth)                              # Create class node (depth=0 for entry)
        self.graph.add_node(class_node)
        self.register_node(full_name, class_node.node_id)

        if depth == 0:                                                               # Set entry point
            self.graph.entry_point = class_node.node_id
            class_node.is_entry    = True

        self.class_context[full_name] = cls                                          # Track for self resolution

        methods_to_analyze = []                                                      # Collect methods for two-phase analysis

        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):   # Phase 1: Create all method nodes first
            if name.startswith('__') and not self.config.include_dunder:
                continue
            if name.startswith('_') and not name.startswith('__') and not self.config.include_private:
                continue

            method_full_name = self.get_qualified_name(method)
            existing_method  = self.lookup_node_id(method_full_name)

            if not existing_method:                                                  # Create method node if not exists
                method_node = self.create_method_node(method, depth + 1, cls)
                self.graph.add_node(method_node)
                self.register_node(method_full_name, method_node.node_id)
                method_node_id = method_node.node_id
            else:
                method_node_id = existing_method

            self.create_edge(class_node.node_id                                     ,  # CONTAINS edge: class → method
                            method_node_id                                          ,
                            Enum__Call_Graph__Edge_Type.CONTAINS                    ,
                            line_number=0                                           )

            methods_to_analyze.append((method, method_node_id))

        for method, method_node_id in methods_to_analyze:                            # Phase 2: Extract calls from all methods
            method_node = self.graph.nodes.get(str(method_node_id))
            if method_node and str(method_node_id) not in self.visited_methods:
                self.visited_methods[str(method_node_id)] = True
                self.extract_calls(method, method_node, depth + 1, cls)

        if int(depth + 1) > int(self.graph.max_depth_found):                         # Update max depth
            self.graph.max_depth_found = Safe_UInt(depth + 1)

        return class_node.node_id

    def analyze_function(self, func, depth: int,                                     # Analyze a single function or method
                         class_context: type = None) -> Optional[Node_Id]:
        if depth > int(self.config.max_depth):
            return None

        full_name = self.get_qualified_name(func)

        existing_id = self.lookup_node_id(full_name)                                 # Check if already analyzed
        if existing_id:
            return existing_id

        node = self.create_method_node(func, depth, class_context)                   # Create node for this function/method
        self.graph.add_node(node)
        self.register_node(full_name, node.node_id)

        self.visited_methods[full_name] = True                                       # Mark as visited

        self.extract_calls(func, node, depth, class_context)                         # Extract calls from this function

        if int(depth) > int(self.graph.max_depth_found):                             # Track max depth
            self.graph.max_depth_found = Safe_UInt(depth)

        return node.node_id

    def create_class_node(self, cls: type, depth: int) -> Schema__Call_Graph__Node:  # Create a node for a class
        full_name  = self.get_qualified_name(cls)
        short_name = cls.__name__
        module     = getattr(cls, '__module__', '')
        node_id    = Node_Id(Obj_Id())

        try:
            file_path = inspect.getfile(cls)
        except (TypeError, OSError):
            file_path = ''

        try:
            _, line_number = inspect.getsourcelines(cls)
        except (TypeError, OSError):
            line_number = 0

        return Schema__Call_Graph__Node(
            node_id     = node_id                                                   ,
            name        = Safe_Str__Label(short_name)                               ,
            full_name   = Safe_Str__Label(full_name)                                ,
            node_type   = Enum__Call_Graph__Node_Type.CLASS                         ,
            module      = Safe_Str__Label(module)                                   ,
            file_path   = Safe_Str__File__Path(file_path) if file_path else Safe_Str__File__Path(''),
            depth       = Safe_UInt(depth)                                          ,
            line_number = Safe_UInt(line_number)                                    ,
        )

    def create_method_node(self, func, depth: int,                                   # Create a node for a method or function
                           class_context: type = None) -> Schema__Call_Graph__Node:
        full_name  = self.get_qualified_name(func)
        short_name = func.__name__
        module     = getattr(func, '__module__', '')
        node_id    = Node_Id(Obj_Id())
        node_type  = Enum__Call_Graph__Node_Type.METHOD if class_context else Enum__Call_Graph__Node_Type.FUNCTION

        try:
            file_path = inspect.getfile(func)
        except (TypeError, OSError):
            file_path = ''

        try:
            source = inspect.getsource(func) if self.config.capture_source else ''
        except (TypeError, OSError):
            source = ''

        try:
            _, line_number = inspect.getsourcelines(func)
        except (TypeError, OSError):
            line_number = 0

        return Schema__Call_Graph__Node(
            node_id     = node_id                                                   ,
            name        = Safe_Str__Label(short_name)                               ,
            full_name   = Safe_Str__Label(full_name)                                ,
            node_type   = node_type                                                 ,
            module      = Safe_Str__Label(module)                                   ,
            file_path   = Safe_Str__File__Path(file_path) if file_path else Safe_Str__File__Path(''),
            depth       = Safe_UInt(depth)                                          ,
            source_code = Safe_Str__Text(source[:4000]) if source else Safe_Str__Text(''),
            line_number = Safe_UInt(line_number)                                    ,
        )

    def create_external_node(self, call_name: str, depth: int) -> Schema__Call_Graph__Node:  # Create placeholder for external call
        node_id = Node_Id(Obj_Id())

        short_name = call_name.split('.')[-1] if '.' in call_name else call_name

        return Schema__Call_Graph__Node(
            node_id     = node_id                                                   ,
            name        = Safe_Str__Label(short_name)                               ,
            full_name   = Safe_Str__Label(call_name)                                ,
            node_type   = Enum__Call_Graph__Node_Type.FUNCTION                      ,
            module      = Safe_Str__Label('')                                       ,
            file_path   = Safe_Str__File__Path('')                                  ,
            depth       = Safe_UInt(depth)                                          ,
            is_external = True                                                      ,
        )

    def create_edge(self, from_node: Node_Id, to_node: Node_Id,                      # Create an edge between two nodes
                    edge_type: Enum__Call_Graph__Edge_Type, line_number: int = 0):
        edge = Schema__Call_Graph__Edge(
            edge_id     = Edge_Id(Obj_Id())                                         ,
            from_node   = from_node                                                 ,
            to_node     = to_node                                                   ,
            edge_type   = edge_type                                                 ,
            line_number = Safe_UInt(line_number)                                    ,
        )
        self.graph.add_edge(edge)
        return edge

    def extract_calls(self, func, caller_node: Schema__Call_Graph__Node,             # Extract all function calls using AST helpers
                      depth: int, class_context: type = None):
        try:
            ast_module = Ast_Module(func)                                            # Parse function with AST helpers
        except Exception:
            return                                                                   # Can't get source, skip

        with Ast_Visit(ast_module) as visitor:
            visitor.capture_calls()                                                  # Enable call capture
            visitor.visit()                                                          # Execute visitor

            for call in visitor.captured_nodes().get('Ast_Call', []):
                call_info = self.resolve_call(call, class_context)
                if call_info:
                    self.process_call(call_info, caller_node, depth)

    def resolve_call(self, call, class_context: type = None) -> Optional[Dict[str, Any]]:  # Resolve an Ast_Call to target info
        try:
            call_name = call.name()                                                  # Built-in resolution from Ast_Call
        except Exception:
            call_name = None

        if not call_name:
            return None

        func_node = call.func()
        func_type = type(func_node).__name__

        if func_type == 'Ast_Attribute':                                             # Check for self.method() pattern
            try:
                value = func_node.value()
                if type(value).__name__ == 'Ast_Name' and value.id() == 'self':
                    if class_context and self.config.resolve_self_calls:             # This is self.method()
                        attr_name = func_node.node.attr                              # Access raw AST node for attr name
                        return {
                            'name'    : attr_name                                   ,
                            'type'    : Enum__Call_Graph__Edge_Type.SELF            ,
                            'class'   : class_context                               ,
                            'resolved': self.resolve_self_method(attr_name, class_context),
                        }
                else:                                                                # obj.method() - chain call
                    return {
                        'name'    : call_name                                       ,
                        'type'    : Enum__Call_Graph__Edge_Type.CHAIN               ,
                        'resolved': None                                            ,
                    }
            except Exception:
                pass

        if func_type == 'Ast_Name':                                                  # Direct call: func()
            return {
                'name'    : call_name                                               ,
                'type'    : Enum__Call_Graph__Edge_Type.CALLS                       ,
                'resolved': None                                                    ,
            }

        return {                                                                     # Default to chain for anything else
            'name'    : call_name                                                   ,
            'type'    : Enum__Call_Graph__Edge_Type.CHAIN                           ,
            'resolved': None                                                        ,
        }

    def resolve_self_method(self, method_name: str,                                  # Resolve self.method() to actual method
                            class_context: type) -> Optional[Any]:
        if hasattr(class_context, method_name):
            return getattr(class_context, method_name)

        for base in inspect.getmro(class_context)[1:]:                               # Check base classes
            if hasattr(base, method_name):
                return getattr(base, method_name)
        return None

    def process_call(self, call_info: Dict[str, Any],                                # Process a resolved call
                     caller_node: Schema__Call_Graph__Node, depth: int):
        call_name = call_info['name']
        edge_type = call_info['type']
        resolved  = call_info.get('resolved')

        if self.should_skip_call(call_name):                                         # Apply filters
            return

        callee_node_id = None

        if resolved:                                                                 # Resolved call - analyze target
            callee_node_id = self.analyze_function(resolved, depth + 1, call_info.get('class'))

        if not callee_node_id and self.config.create_external_nodes:                 # Create external placeholder node
            existing_id = self.lookup_node_id(call_name)
            if existing_id:
                callee_node_id = existing_id
            else:
                external_node  = self.create_external_node(call_name, depth + 1)
                self.graph.add_node(external_node)
                self.register_node(call_name, external_node.node_id)
                callee_node_id = external_node.node_id

                if int(depth + 1) > int(self.graph.max_depth_found):
                    self.graph.max_depth_found = Safe_UInt(depth + 1)

        if callee_node_id:
            caller_node.calls.append(callee_node_id)                                 # Update caller's outgoing calls
            self.create_edge(caller_node.node_id, callee_node_id, edge_type)         # Create edge

            if str(callee_node_id) in self.graph.nodes:                              # Update callee's incoming calls
                self.graph.nodes[str(callee_node_id)].called_by.append(caller_node.node_id)

    def should_skip_call(self, call_name: str) -> bool:                              # Check if call should be filtered out
        if call_name.startswith('__') and not self.config.include_dunder:
            return True

        if call_name.startswith('_') and not call_name.startswith('__') and not self.config.include_private:
            return True

        if not self.config.include_stdlib and self.is_stdlib(call_name):             # Check stdlib
            return True

        if self.is_blocked(call_name):                                               # Check blocklist
            return True

        if not self.is_allowed(call_name):                                           # Check allowlist
            return True

        return False

    def is_stdlib(self, call_name: str) -> bool:                                     # Check if name is Python standard library
        stdlib_builtins = {'print', 'len', 'str', 'int', 'list', 'dict', 'set',
                           'tuple', 'range', 'enumerate', 'zip', 'map', 'filter',
                           'sorted', 'reversed', 'type', 'isinstance', 'hasattr',
                           'getattr', 'setattr', 'delattr', 'super', 'open',
                           'abs', 'all', 'any', 'bin', 'bool', 'bytes', 'callable',
                           'chr', 'complex', 'dir', 'divmod', 'float', 'format',
                           'frozenset', 'hash', 'hex', 'id', 'input', 'iter',
                           'max', 'min', 'next', 'object', 'oct', 'ord', 'pow',
                           'repr', 'round', 'slice', 'sum', 'vars'}

        base_name = call_name.split('.')[0] if '.' in call_name else call_name
        return base_name in stdlib_builtins

    def is_external(self, module: str) -> bool:                                      # Check if module is external (pip package)
        if not module:
            return True

        stdlib_modules = set(sys.stdlib_module_names) if hasattr(sys, 'stdlib_module_names') else set()
        base_module    = module.split('.')[0]

        return base_module not in stdlib_modules

    def is_blocked(self, call_name: str) -> bool:                                    # Check if target is in any blocklist
        if not self.config.module_blocklist and not self.config.class_blocklist:
            return False

        for blocked in self.config.module_blocklist:
            if call_name.startswith(str(blocked)):
                return True

        for blocked in self.config.class_blocklist:
            if call_name.startswith(str(blocked)):
                return True

        return False

    def is_allowed(self, call_name: str) -> bool:                                    # Check if target passes allowlists
        if not self.config.module_allowlist and not self.config.class_allowlist:     # No allowlist = allow all
            return True

        for allowed in self.config.module_allowlist:
            if call_name.startswith(str(allowed)):
                return True

        for allowed in self.config.class_allowlist:
            if call_name.startswith(str(allowed)):
                return True

        return False

import inspect
from typing                                                                         import Dict, Optional, List, Tuple
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph                import Schema__Call_Graph
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Config        import Schema__Call_Graph__Config
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Node          import Schema__Call_Graph__Node
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call__Info                import Schema__Call__Info
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type import Enum__Call_Graph__Edge_Type
from osbot_utils.helpers.python_call_flow.Call_Flow__Node__Factory                  import Call_Flow__Node__Factory
from osbot_utils.helpers.python_call_flow.Call_Flow__Edge__Factory                  import Call_Flow__Edge__Factory
from osbot_utils.helpers.python_call_flow.Call_Flow__Call__Resolver                 import Call_Flow__Call__Resolver
from osbot_utils.helpers.python_call_flow.Call_Flow__Call__Filter                   import Call_Flow__Call__Filter
from osbot_utils.helpers.python_call_flow.Call_Flow__AST__Extractor                 import Call_Flow__AST__Extractor
from osbot_utils.helpers.python_call_flow.Call_Flow__Node__Registry                 import Call_Flow__Node__Registry
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                  import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label  import Safe_Str__Label
from osbot_utils.type_safe.primitives.core.Safe_UInt                                import Safe_UInt


class Call_Flow__Analyzer(Type_Safe):                                                # Orchestrates call graph analysis
    config        : Schema__Call_Graph__Config                                       # Analysis configuration
    graph         : Schema__Call_Graph                                               # The resulting call graph

    node_factory  : Call_Flow__Node__Factory                                         # Creates graph nodes
    edge_factory  : Call_Flow__Edge__Factory                                         # Creates graph edges
    call_resolver : Call_Flow__Call__Resolver                                        # Resolves AST calls
    call_filter   : Call_Flow__Call__Filter                                          # Filters calls
    ast_extractor : Call_Flow__AST__Extractor                                        # Extracts calls from AST
    node_registry : Call_Flow__Node__Registry                                        # Manages name→id mapping

    visited_methods : Dict[str, bool]                                                # Track analyzed methods
    class_context   : Dict[str, type]                                                # Track class for self resolution

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_components()

    def setup_components(self):                                                      # Initialize component dependencies
        self.node_factory.config    = self.config
        self.node_factory.registry  = self.node_registry
        self.call_resolver.config   = self.config
        self.call_filter.config     = self.config

    def analyze(self, target) -> Schema__Call_Graph:                                 # Main entry point - analyze function/class/module
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
        self.node_registry.reset()
        self.visited_methods = {}
        self.class_context   = {}
        self.graph           = Schema__Call_Graph()
        self.setup_components()                                                      # Re-wire components

    def initialize_graph(self, target):                                              # Set up graph metadata
        target_name         = self.node_registry.qualified_name(target)
        self.graph.graph_id = Graph_Id(Obj_Id())
        self.graph.name     = Safe_Str__Label(target_name)
        self.graph.config   = self.config

    def analyze_class(self, cls: type, depth: int) -> Optional[Node_Id]:             # Analyze a class
        if depth > int(self.config.max_depth):
            return None

        full_name = self.node_registry.qualified_name(cls)

        existing_id = self.node_registry.lookup(full_name)                           # Check if already analyzed
        if existing_id:
            return existing_id

        class_node = self.node_factory.create_class_node(cls, depth)                 # Create class node
        self.graph.add_node(class_node)
        self.node_registry.register(full_name, class_node.node_id)

        if depth == 0:                                                               # Set entry point
            self.graph.entry_point = class_node.node_id
            class_node.is_entry    = True

        self.class_context[full_name] = cls                                          # Track for self resolution

        methods_to_analyze = self.collect_methods(cls, class_node, depth)            # Phase 1: Create method nodes

        for method, method_node_id in methods_to_analyze:                            # Phase 2: Extract calls
            self.analyze_method_calls(method, method_node_id, depth + 1, cls)

        self.update_max_depth(depth + 1)

        return class_node.node_id

    def collect_methods(self, cls: type, class_node: Schema__Call_Graph__Node,       # Collect and create method nodes
                        depth: int) -> List[Tuple]:
        methods_to_analyze = []

        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            if not self.call_filter.should_include_method(name):
                continue

            method_full_name = self.node_registry.qualified_name(method)
            existing_method  = self.node_registry.lookup(method_full_name)

            if not existing_method:                                                  # Create method node
                method_node = self.node_factory.create_method_node(method, depth + 1, is_method=True)
                self.graph.add_node(method_node)
                self.node_registry.register(method_full_name, method_node.node_id)
                method_node_id = method_node.node_id
            else:
                method_node_id = existing_method

            edge = self.edge_factory.create_contains(class_node.node_id, method_node_id)  # CONTAINS edge
            self.graph.add_edge(edge)

            methods_to_analyze.append((method, method_node_id))

        return methods_to_analyze

    def analyze_method_calls(self, method, method_node_id: Node_Id,                  # Analyze calls within a method
                             depth: int, class_context: type):
        method_node = self.graph.nodes.get(str(method_node_id))
        if not method_node:
            return

        full_name = self.node_registry.qualified_name(method)                        # Use qualified name as key
        if full_name in self.visited_methods:
            return

        self.visited_methods[full_name] = True
        self.extract_and_process_calls(method, method_node, depth, class_context)

    def analyze_function(self, func, depth: int,                                     # Analyze a standalone function
                         class_context: type = None) -> Optional[Node_Id]:
        if depth > int(self.config.max_depth):
            return None

        full_name = self.node_registry.qualified_name(func)

        existing_id = self.node_registry.lookup(full_name)                           # Check if already analyzed
        if existing_id:
            return existing_id

        is_method = class_context is not None
        node      = self.node_factory.create_method_node(func, depth, is_method=is_method)
        self.graph.add_node(node)
        self.node_registry.register(full_name, node.node_id)

        if depth == 0:                                                               # Set entry point for functions
            self.graph.entry_point = node.node_id
            node.is_entry          = True

        self.visited_methods[full_name] = True

        self.extract_and_process_calls(func, node, depth, class_context)

        self.update_max_depth(depth)

        return node.node_id

    def extract_and_process_calls(self, func, caller_node: Schema__Call_Graph__Node, # Extract calls and process them
                                  depth: int, class_context: type = None):
        calls = self.ast_extractor.extract_calls(func)

        for call in calls:
            call_info = self.call_resolver.resolve(call, class_context)
            if call_info:
                self.process_call(call_info, caller_node, depth)

    def process_call(self, call_info: Schema__Call__Info,                            # Process a resolved call
                     caller_node: Schema__Call_Graph__Node, depth: int):
        call_name = str(call_info.name)

        if self.call_filter.should_skip(call_name):                                  # Apply filters
            return

        callee_node_id = None

        if call_info.resolved:                                                       # Resolved call - analyze target
            callee_node_id = self.analyze_function(call_info.resolved, depth + 1, call_info.class_ref)

        if not callee_node_id and self.config.create_external_nodes:                 # Create external placeholder
            callee_node_id = self.get_or_create_external_node(call_name, depth + 1)

        if callee_node_id:
            self.link_nodes(caller_node, callee_node_id, call_info.edge_type, int(call_info.line_number))

    def get_or_create_external_node(self, call_name: str, depth: int) -> Node_Id:    # Get existing or create external node
        existing_id = self.node_registry.lookup(call_name)
        if existing_id:
            return existing_id

        external_node = self.node_factory.create_external_node(call_name, depth)
        self.graph.add_node(external_node)
        self.node_registry.register(call_name, external_node.node_id)

        self.update_max_depth(depth)

        return external_node.node_id

    def link_nodes(self, caller_node: Schema__Call_Graph__Node, callee_node_id: Node_Id,  # Link caller to callee
                   edge_type: Enum__Call_Graph__Edge_Type, line_number: int = 0):
        caller_node.calls.append(callee_node_id)                                     # Update caller's outgoing calls

        edge = self.edge_factory.create(caller_node.node_id, callee_node_id, edge_type, line_number)
        self.graph.add_edge(edge)

        if str(callee_node_id) in self.graph.nodes:                                  # Update callee's incoming calls
            self.graph.nodes[str(callee_node_id)].called_by.append(caller_node.node_id)

    def update_max_depth(self, depth: int):                                          # Update max depth if needed
        if depth > int(self.graph.max_depth_found):
            self.graph.max_depth_found = Safe_UInt(depth)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Delegated Methods - For backward compatibility and convenience
    # ═══════════════════════════════════════════════════════════════════════════════

    def register_node(self, full_name: str, node_id: Node_Id):                       # Delegate to registry
        self.node_registry.register(full_name, node_id)

    def lookup_node_id(self, full_name: str) -> Optional[Node_Id]:                   # Delegate to registry
        return self.node_registry.lookup(full_name)

    def get_qualified_name(self, target) -> str:                                     # Delegate to registry
        return self.node_registry.qualified_name(target)

    def should_skip_call(self, call_name: str) -> bool:                              # Delegate to filter
        return self.call_filter.should_skip(call_name)

    def is_stdlib(self, call_name: str) -> bool:                                     # Delegate to filter
        return self.call_filter.is_stdlib(call_name)
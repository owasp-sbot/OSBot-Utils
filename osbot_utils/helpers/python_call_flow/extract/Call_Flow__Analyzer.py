# ═══════════════════════════════════════════════════════════════════════════════
# Call Flow Analyzer - Refactored to use Semantic Graph Framework
# Analyzes Python call flows and produces semantic graphs
# ═══════════════════════════════════════════════════════════════════════════════

import ast
import inspect
import textwrap
from typing                                                                     import Set, Dict, Any, List
from osbot_utils.helpers.python_call_flow.core.Call_Flow__Builder               import Call_Flow__Builder
from osbot_utils.helpers.python_call_flow.extract.Call_Extractor                import Call_Extractor
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Config     import Schema__Call_Flow__Config
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Result     import Schema__Call_Flow__Result
from osbot_utils.helpers.python_call_flow.schemas.Schema__Extracted__Call       import Schema__Extracted__Call
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe


# ═══════════════════════════════════════════════════════════════════════════════
# Main Analyzer
# ═══════════════════════════════════════════════════════════════════════════════

class Call_Flow__Analyzer(Type_Safe):                                            # Analyzes Python call flows using semantic graph framework
    config            : Schema__Call_Flow__Config                                # Analysis configuration
    builder           : Call_Flow__Builder                                       # Graph builder
    visited           : Set[str]                                                 # Visited qualified names
    class_methods     : Dict[str, Dict[str, Any]]                                # class_name -> {method_name -> method}
    current_depth     : int                         = 0                          # Current analysis depth
    max_depth_reached : int                         = 0                          # Maximum depth reached


    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, *args):
        pass

    def setup(self) -> 'Call_Flow__Analyzer':                                    # Initialize analyzer components
        self.builder = Call_Flow__Builder().setup()
        self.visited = set()
        self.class_methods = {}
        self.current_depth = 0
        self.max_depth_reached = 0
        return self

    # ═══════════════════════════════════════════════════════════════════════════
    # Main Entry Point
    # ═══════════════════════════════════════════════════════════════════════════

    def analyze(self, target) -> Schema__Call_Flow__Result:                      # Analyze a class or function
        self.setup()

        entry_point = self._get_qualified_name(target)

        if inspect.isclass(target):
            self._analyze_class(target, is_entry=True)
        elif inspect.isfunction(target) or inspect.ismethod(target):
            self._analyze_function(target, is_entry=True)
        else:
            raise ValueError(f"Cannot analyze {type(target)}: must be class or function")

        graph = self.builder.build()

        return Schema__Call_Flow__Result(graph             = graph                                              ,
                                         node_properties   = self.builder.node_properties                       ,
                                         name_to_node_id   = {k: str(v) for k, v in
                                                              self.builder.name_to_node_id.items()}             ,
                                         entry_point       = entry_point                                        ,
                                         max_depth_reached = self.max_depth_reached                             ,
                                         total_nodes       = len(graph.nodes)                                   ,
                                         total_edges       = len(graph.edges)                                   )

    # ═══════════════════════════════════════════════════════════════════════════
    # Class Analysis
    # ═══════════════════════════════════════════════════════════════════════════

    def _analyze_class(self                                                      ,
                       cls                                                       ,
                       is_entry   : bool = False                                 ,
                       class_name : str  = None                                  ):
        qualified_name = class_name or self._get_qualified_name(cls)

        if qualified_name in self.visited:
            return
        self.visited.add(qualified_name)

        module_name = getattr(cls, '__module__', '')                             # Create class node
        file_path   = self._get_file_path(cls)
        line_number = self._get_line_number(cls)

        self.builder.add_class(qualified_name = qualified_name                   ,
                               module_name    = module_name                      ,
                               file_path      = file_path                        ,
                               line_number    = line_number                      )

        methods = self._collect_methods(cls, qualified_name)                     # Collect and store methods for self-call resolution
        self.class_methods[qualified_name] = methods

        for method_name, method in methods.items():                              # Analyze each method
            method_qualified_name = f"{qualified_name}.{method_name}"

            if method_qualified_name not in self.visited:                        # Analyze if not already visited
                self._analyze_method(method                                      ,
                                     method_name          = method_name          ,
                                     class_qualified_name = qualified_name       ,
                                     is_entry             = False                )

            if self.builder.has_node(method_qualified_name):
                self.builder.add_contains(qualified_name, method_qualified_name)     # Always add containment edge

    def _collect_methods(self, cls, class_name: str) -> Dict[str, Any]:          # Collect methods from a class
        methods = {}

        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            if self._should_include_method(name):
                methods[name] = method

        return methods

    def _should_include_method(self, name: str) -> bool:                         # Check if method should be included
        if name.startswith('__') and name.endswith('__'):                        # Dunder methods
            return self.config.include_builtins

        if name.startswith('_'):                                                 # Private methods
            return True                                                          # Include by default

        return True

    # ═══════════════════════════════════════════════════════════════════════════
    # Method/Function Analysis
    # ═══════════════════════════════════════════════════════════════════════════

    def _analyze_method(self                                                     ,
                        method                                                   ,
                        method_name          : str                               ,
                        class_qualified_name : str                               ,
                        is_entry             : bool = False                      ):
        qualified_name = f"{class_qualified_name}.{method_name}"

        if qualified_name in self.visited:
            return
        self.visited.add(qualified_name)

        if self.current_depth > self.config.max_depth:
            return

        self.current_depth += 1
        self.max_depth_reached = max(self.max_depth_reached, self.current_depth)

        module_name = getattr(method, '__module__', '')                          # Create method node
        file_path   = self._get_file_path(method)
        line_number = self._get_line_number(method)

        self.builder.add_method(qualified_name = qualified_name                  ,
                                module_name    = module_name                     ,
                                file_path      = file_path                       ,
                                line_number    = line_number                     ,
                                is_entry       = is_entry                        )

        calls = self._extract_calls(method)                                      # Extract and process calls

        for call in calls:
            self._process_call(caller_qualified_name = qualified_name            ,
                               call                  = call                      ,
                               class_qualified_name  = class_qualified_name      )

        self.current_depth -= 1

    def _analyze_function(self                                                   ,
                          func                                                   ,
                          is_entry       : bool = False                          ,
                          qualified_name : str  = None                           ):
        qualified_name = qualified_name or self._get_qualified_name(func)

        if qualified_name in self.visited:
            return
        self.visited.add(qualified_name)

        if self.current_depth > self.config.max_depth:
            return

        self.current_depth += 1
        self.max_depth_reached = max(self.max_depth_reached, self.current_depth)

        module_name = getattr(func, '__module__', '')                            # Create function node
        file_path   = self._get_file_path(func)
        line_number = self._get_line_number(func)

        self.builder.add_function(qualified_name = qualified_name                ,
                                  module_name    = module_name                   ,
                                  file_path      = file_path                     ,
                                  line_number    = line_number                   ,
                                  is_entry       = is_entry                      )

        calls = self._extract_calls(func)                                        # Extract and process calls

        for call in calls:
            self._process_call(caller_qualified_name = qualified_name            ,
                               call                  = call                      ,
                               class_qualified_name  = None                      )

        self.current_depth -= 1

    # ═══════════════════════════════════════════════════════════════════════════
    # Call Processing
    # ═══════════════════════════════════════════════════════════════════════════

    def _process_call(self                                                       ,
                      caller_qualified_name : str                                ,
                      call                  : Schema__Extracted__Call            ,
                      class_qualified_name  : str = None                         ):
        if self._should_skip_call(call.call_name):                               # Skip stdlib/builtins
            return

        if call.is_self_call and class_qualified_name:                           # Handle self.method() calls
            self._process_self_call(caller_qualified_name                        ,
                                    call                                         ,
                                    class_qualified_name                         )

        elif call.is_chain_call:                                                 # Handle chain calls (obj.attr.method())
            self._process_chain_call(caller_qualified_name, call)

        else:                                                                    # Handle regular function calls
            self._process_regular_call(caller_qualified_name, call)

    def _process_self_call(self                                                  ,
                           caller_qualified_name : str                           ,
                           call                  : Schema__Extracted__Call       ,
                           class_qualified_name  : str                           ):
        method_name        = call.call_name
        target_method_name = f"{class_qualified_name}.{method_name}"

        if class_qualified_name in self.class_methods:                           # Check if method exists in class
            methods = self.class_methods[class_qualified_name]
            if method_name in methods:
                if target_method_name not in self.visited:                       # Analyze target method if not visited
                    method = methods[method_name]
                    self._analyze_method(method                                  ,
                                         method_name          = method_name      ,
                                         class_qualified_name = class_qualified_name)

                if self.builder.has_node(target_method_name):                    # Only add edge if target node exists
                    self.builder.add_calls_self(caller_qualified_name            ,
                                                target_method_name               ,
                                                call_line_number = call.line_number,
                                                is_conditional   = call.is_conditional)
                return

        if self.config.include_external:                                         # Create as external if not found
            if not self.builder.has_node(target_method_name):
                self.builder.add_external(qualified_name = target_method_name    ,
                                          module_name    = ''                    )

            self.builder.add_calls_self(caller_qualified_name                    ,
                                        target_method_name                       ,
                                        call_line_number = call.line_number      ,
                                        is_conditional   = call.is_conditional   )


    def _process_chain_call(self                                                 ,
                            caller_qualified_name : str                          ,
                            call                  : Schema__Extracted__Call      ):
        target_name = call.full_expression                                       # Use full expression as target name

        if self.config.include_external:
            if not self.builder.has_node(target_name):
                self.builder.add_external(qualified_name = target_name           ,
                                          module_name    = ''                    )

            self.builder.add_calls_chain(caller_qualified_name                   ,
                                         target_name                             ,
                                         call_line_number = call.line_number     ,
                                         is_conditional   = call.is_conditional  )

    def _process_regular_call(self                                               ,
                              caller_qualified_name : str                        ,
                              call                  : Schema__Extracted__Call    ):
        target_name = call.call_name

        if self.config.include_external:                                         # Create external node for unresolved calls
            if not self.builder.has_node(target_name):
                self.builder.add_external(qualified_name = target_name           ,
                                          module_name    = ''                    )

            self.builder.add_calls(caller_qualified_name                         ,
                                   target_name                                   ,
                                   call_line_number = call.line_number           ,
                                   is_conditional   = call.is_conditional        )

    # ═══════════════════════════════════════════════════════════════════════════
    # Call Extraction
    # ═══════════════════════════════════════════════════════════════════════════

    def _extract_calls(self, func) -> List[Schema__Extracted__Call]:             # Extract calls from function/method using AST
        source = inspect.getsource(func)
        source = textwrap.dedent(source)                                     # Remove leading indentation
        tree   = ast.parse(source)

        extractor = Call_Extractor()
        extractor.visit(tree)

        return extractor.calls

    # ═══════════════════════════════════════════════════════════════════════════
    # Filtering
    # ═══════════════════════════════════════════════════════════════════════════

    def _should_skip_call(self, name: str) -> bool:                              # Check if call should be skipped
        if self._is_stdlib(name):
            return not self.config.include_builtins
        return False

    def _is_stdlib(self, name: str) -> bool:                                     # Check if name is a Python builtin/stdlib
        builtins = {'print', 'len', 'str', 'int', 'float', 'bool', 'list',
                    'dict', 'set', 'tuple', 'range', 'enumerate', 'zip',
                    'map', 'filter', 'sorted', 'reversed', 'sum', 'min',
                    'max', 'abs', 'round', 'pow', 'divmod', 'hex', 'oct',
                    'bin', 'ord', 'chr', 'type', 'isinstance', 'issubclass',
                    'hasattr', 'getattr', 'setattr', 'delattr', 'callable',
                    'repr', 'hash', 'id', 'dir', 'vars', 'locals', 'globals',
                    'iter', 'next', 'open', 'input', 'format', 'super',
                    'staticmethod', 'classmethod', 'property', 'object',
                    'Exception', 'BaseException', 'ValueError', 'TypeError',
                    'AttributeError', 'KeyError', 'IndexError', 'RuntimeError'}
        return name in builtins

    # ═══════════════════════════════════════════════════════════════════════════
    # Utility Methods
    # ═══════════════════════════════════════════════════════════════════════════

    def _get_qualified_name(self, obj) -> str:                                   # Get fully qualified name for object
        module = getattr(obj, '__module__', '')
        name   = getattr(obj, '__qualname__', getattr(obj, '__name__', str(obj)))

        if module:
            return f"{module}.{name}"
        return name

    def _get_file_path(self, obj) -> str:                                        # Get file path for object
        return inspect.getfile(obj)

    def _get_line_number(self, obj) -> int:                                      # Get line number for object
        _, line_number = inspect.getsourcelines(obj)
        return line_number


    # ═══════════════════════════════════════════════════════════════════════════
    # Convenience Methods (for backward compatibility with tests)
    # ═══════════════════════════════════════════════════════════════════════════


    def should_skip_call(self, name: str) -> bool:                               # Public wrapper for tests
        return self._should_skip_call(name)

    def is_stdlib(self, name: str) -> bool:                                      # Public wrapper for tests
        return self._is_stdlib(name)

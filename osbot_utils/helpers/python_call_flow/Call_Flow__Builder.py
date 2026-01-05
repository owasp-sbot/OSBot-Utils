# ═══════════════════════════════════════════════════════════════════════════════
# Call Flow Builder - Domain-specific builder for call flow semantic graphs
# Wraps Semantic_Graph__Builder with convenience methods for call flow nodes/edges
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                           import Dict, Optional, Any
from osbot_utils.helpers.python_call_flow.Call_Flow__Ontology                         import Call_Flow__Ontology
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Builder                import Semantic_Graph__Builder
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph         import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id              import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id              import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type           import Enum__Id__Source_Type
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source        import Schema__Id__Source
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                     import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                     import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                      import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id       import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed




class Call_Flow__Builder(Type_Safe):                                                 # Domain-specific builder for call flow graphs
    ontology          : Call_Flow__Ontology                                          # Loaded call flow ontology
    builder           : Semantic_Graph__Builder                                      # Underlying graph builder
    name_to_node_id   : Dict[str, Node_Id]                                           # qualified_name -> node_id mapping
    node_properties   : Dict[str, Dict[str, Any]]                                    # node_id -> properties mapping

    def setup(self) -> 'Call_Flow__Builder':                                         # Initialize ontology and builder
        self.ontology.setup()
        self.builder.with_ontology_id(self.ontology.ontology_id())

        return self

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Operations - Add nodes by type
    # ═══════════════════════════════════════════════════════════════════════════

    def add_class(self                                                               ,
                  qualified_name : str                                               ,
                  module_name    : str  = None                                       ,
                  file_path      : str  = None                                       ,
                  line_number    : int  = None                                       ,
                  source_code    : str  = None                                       ) -> 'Call_Flow__Builder':
        return self._add_node(node_type_id   = self.ontology.node_type_id__class()   ,
                              qualified_name = qualified_name                        ,
                              module_name    = module_name                           ,
                              file_path      = file_path                             ,
                              line_number    = line_number                           ,
                              source_code    = source_code                           )

    def add_method(self                                                              ,
                   qualified_name : str                                              ,
                   module_name    : str  = None                                      ,
                   file_path      : str  = None                                      ,
                   line_number    : int  = None                                      ,
                   source_code    : str  = None                                      ,
                   is_entry       : bool = False                                     ,
                   is_recursive   : bool = False                                     ) -> 'Call_Flow__Builder':
        return self._add_node(node_type_id   = self.ontology.node_type_id__method()  ,
                              qualified_name = qualified_name                        ,
                              module_name    = module_name                           ,
                              file_path      = file_path                             ,
                              line_number    = line_number                           ,
                              source_code    = source_code                           ,
                              is_entry       = is_entry                              ,
                              is_recursive   = is_recursive                          )

    def add_function(self                                                            ,
                     qualified_name : str                                            ,
                     module_name    : str  = None                                    ,
                     file_path      : str  = None                                    ,
                     line_number    : int  = None                                    ,
                     source_code    : str  = None                                    ,
                     is_entry       : bool = False                                   ,
                     is_recursive   : bool = False                                   ) -> 'Call_Flow__Builder':
        return self._add_node(node_type_id   = self.ontology.node_type_id__function(),
                              qualified_name = qualified_name                        ,
                              module_name    = module_name                           ,
                              file_path      = file_path                             ,
                              line_number    = line_number                           ,
                              source_code    = source_code                           ,
                              is_entry       = is_entry                              ,
                              is_recursive   = is_recursive                          )

    def add_module(self                                                              ,
                   qualified_name : str                                              ,
                   file_path      : str  = None                                      ) -> 'Call_Flow__Builder':
        return self._add_node(node_type_id   = self.ontology.node_type_id__module()  ,
                              qualified_name = qualified_name                        ,
                              module_name    = qualified_name                        ,
                              file_path      = file_path                             )

    def add_external(self                                                            ,
                     qualified_name : str                                            ,
                     module_name    : str  = None                                    ) -> 'Call_Flow__Builder':
        return self._add_node(node_type_id   = self.ontology.node_type_id__external(),
                              qualified_name = qualified_name                        ,
                              module_name    = module_name                           ,
                              is_external    = True                                  )

    def _add_node(self                                                               ,
                  node_type_id   : Node_Type_Id                                      ,
                  qualified_name : str                                               ,
                  module_name    : str  = None                                       ,
                  file_path      : str  = None                                       ,
                  line_number    : int  = None                                       ,
                  source_code    : str  = None                                       ,
                  is_entry       : bool = False                                      ,
                  is_external    : bool = False                                      ,
                  is_recursive   : bool = False                                      ) -> 'Call_Flow__Builder':
        if qualified_name in self.name_to_node_id:                                   # Skip if node already exists
            return self

        seed        = Safe_Str__Id__Seed(f'call_flow:node:{qualified_name}')         # Generate deterministic node ID
        node_id     = Node_Id(Obj_Id.from_seed(seed))
        node_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                         seed        = seed                              )

        name = Safe_Str__Id(qualified_name.split('.')[-1])                           # Use short name for display

        self.builder.add_node(node_type_id = node_type_id                            ,
                              name         = name                                    ,
                              node_id      = node_id                                 ,
                              node_source  = node_source                             )

        self.name_to_node_id[qualified_name] = node_id                               # Store the mapping

        properties = { 'qualified_name' : qualified_name }                           # Store properties
        if module_name  is not None: properties['module_name' ] = module_name
        if file_path    is not None: properties['file_path'   ] = file_path
        if line_number  is not None: properties['line_number' ] = line_number
        if source_code  is not None: properties['source_code' ] = source_code
        if is_entry                : properties['is_entry'    ] = True
        if is_external             : properties['is_external' ] = True
        if is_recursive            : properties['is_recursive'] = True

        self.node_properties[str(node_id)] = properties

        return self

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Operations - Add edges by type
    # ═══════════════════════════════════════════════════════════════════════════

    def add_contains(self                                                            ,
                     from_name      : str                                            ,
                     to_name        : str                                            ) -> 'Call_Flow__Builder':
        return self._add_edge(predicate_id = self.ontology.predicate_id__contains()  ,
                              from_name    = from_name                               ,
                              to_name      = to_name                                 )

    def add_calls(self                                                               ,
                  from_name        : str                                             ,
                  to_name          : str                                             ,
                  call_line_number : int  = None                                     ,
                  is_conditional   : bool = False                                    ) -> 'Call_Flow__Builder':
        return self._add_edge(predicate_id     = self.ontology.predicate_id__calls() ,
                              from_name        = from_name                           ,
                              to_name          = to_name                             ,
                              call_line_number = call_line_number                    ,
                              is_conditional   = is_conditional                      )

    def add_calls_self(self                                                          ,
                       from_name        : str                                        ,
                       to_name          : str                                        ,
                       call_line_number : int  = None                                ,
                       is_conditional   : bool = False                               ) -> 'Call_Flow__Builder':
        return self._add_edge(predicate_id     = self.ontology.predicate_id__calls_self(),
                              from_name        = from_name                               ,
                              to_name          = to_name                                 ,
                              call_line_number = call_line_number                        ,
                              is_conditional   = is_conditional                          )

    def add_calls_chain(self                                                         ,
                        from_name        : str                                       ,
                        to_name          : str                                       ,
                        call_line_number : int  = None                               ,
                        is_conditional   : bool = False                              ) -> 'Call_Flow__Builder':
        return self._add_edge(predicate_id     = self.ontology.predicate_id__calls_chain(),
                              from_name        = from_name                                ,
                              to_name          = to_name                                  ,
                              call_line_number = call_line_number                         ,
                              is_conditional   = is_conditional                           )

    def _add_edge(self                                                               ,
                  predicate_id     : Predicate_Id                                    ,
                  from_name        : str                                             ,
                  to_name          : str                                             ,
                  call_line_number : int  = None                                     ,
                  is_conditional   : bool = False                                    ) -> 'Call_Flow__Builder':
        from_node_id = self.name_to_node_id.get(from_name)
        to_node_id   = self.name_to_node_id.get(to_name)

        if from_node_id is None:
            raise ValueError(f"Source node not found: {from_name}")
        if to_node_id is None:
            raise ValueError(f"Target node not found: {to_name}")

        seed        = Safe_Str__Id__Seed(f'call_flow:edge:{from_name}:{to_name}:{predicate_id}')
        edge_id     = Edge_Id(Obj_Id.from_seed(seed))
        edge_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                         seed        = seed                              )

        self.builder.add_edge(from_node_id = from_node_id                            ,
                              predicate_id = predicate_id                            ,
                              to_node_id   = to_node_id                              ,
                              edge_id      = edge_id                                 ,
                              edge_source  = edge_source                             )

        return self

    # ═══════════════════════════════════════════════════════════════════════════
    # Lookup Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def lookup_node_id(self, qualified_name: str) -> Optional[Node_Id]:              # Get node ID by qualified name
        return self.name_to_node_id.get(qualified_name)

    def has_node(self, qualified_name: str) -> bool:                                 # Check if node exists
        return qualified_name in self.name_to_node_id

    def get_node_properties(self, qualified_name: str) -> Optional[Dict[str, Any]]:  # Get properties for a node
        node_id = self.name_to_node_id.get(qualified_name)
        if node_id:
            return self.node_properties.get(str(node_id))
        return None

    # ═══════════════════════════════════════════════════════════════════════════
    # Build
    # ═══════════════════════════════════════════════════════════════════════════

    def build(self) -> Schema__Semantic_Graph:                                       # Return the completed graph
        return self.builder.build()

    def graph(self) -> Schema__Semantic_Graph:                                       # Alias for build()
        return self.build()

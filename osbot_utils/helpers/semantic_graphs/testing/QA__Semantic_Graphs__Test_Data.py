# ═══════════════════════════════════════════════════════════════════════════════
# QA__Semantic_Graphs__Test_Data - Reusable test data factories for semantic graphs
#
# Provides factory methods for creating:
#   - Taxonomies with hierarchical categories
#   - Ontologies with node types and relationships
#   - Rule sets with transitivity and cardinality rules
#   - Semantic graphs with nodes and edges
#
# All methods use the new ID/Ref architecture:
#   - *_Ref for human-readable references (labels from config)
#   - *_Id for unique instance identifiers
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Ref      import Dict__Categories__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Ref      import Dict__Node_Types__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id            import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Relationships__By_Verb  import Dict__Relationships__By_Verb
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Refs           import List__Category_Refs
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Node_Type_Refs          import List__Node_Type_Refs
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Cardinality      import List__Rules__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Transitivity     import List__Rules__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges   import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph             import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge       import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node       import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                  import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type               import Enum__Id__Source_Type
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                 import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                   import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref                  import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                   import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref                  import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source            import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                   import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref                  import Taxonomy_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type     import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Relationship  import Schema__Ontology__Relationship
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                    import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality           import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity          import Schema__Rule__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb        import Safe_Str__Ontology__Verb
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy                import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category      import Schema__Taxonomy__Category
from osbot_utils.type_safe.Type_Safe                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                      import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text              import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version           import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                         import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                        import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                         import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                          import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id           import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed     import Safe_Str__Id__Seed
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                            import type_safe


class QA__Semantic_Graphs__Test_Data(Type_Safe):                                         # Test data factory for semantic graphs

    # ═══════════════════════════════════════════════════════════════════════════
    # Taxonomy Creation
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_category(self                                   ,
                        category_ref : Category_Ref            ,
                        name         : Safe_Str__Id      = None,
                        description  : Safe_Str__Text    = None,
                        parent_ref   : Category_Ref      = None,
                        child_refs   : List__Category_Refs = None) -> Schema__Taxonomy__Category:
        return Schema__Taxonomy__Category(category_ref = category_ref                      ,
                                          name         = name         or Safe_Str__Id(category_ref),
                                          description  = description  or Safe_Str__Text()          ,
                                          parent_ref   = parent_ref   or Category_Ref()            ,
                                          child_refs   = child_refs   or List__Category_Refs()     )

    @type_safe
    def create_taxonomy__code_elements(self) -> Schema__Taxonomy:                        # Standard code elements taxonomy
        root = self.create_category(category_ref = Category_Ref('code_element')        ,
                                    description  = Safe_Str__Text('Root category')     ,
                                    child_refs   = List__Category_Refs([Category_Ref('container'),
                                                                        Category_Ref('code_unit')]))

        container = self.create_category(category_ref = Category_Ref('container')             ,
                                         description  = Safe_Str__Text('Container elements')  ,
                                         parent_ref   = Category_Ref('code_element')          )

        code_unit = self.create_category(category_ref = Category_Ref('code_unit')             ,
                                         description  = Safe_Str__Text('Executable code')     ,
                                         parent_ref   = Category_Ref('code_element')          ,
                                         child_refs   = List__Category_Refs([Category_Ref('callable')]))

        callable_cat = self.create_category(category_ref = Category_Ref('callable')           ,
                                            description  = Safe_Str__Text('Callable code')    ,
                                            parent_ref   = Category_Ref('code_unit')          )

        categories = Dict__Categories__By_Ref()
        categories[Category_Ref('code_element')] = root
        categories[Category_Ref('container')]    = container
        categories[Category_Ref('code_unit')]    = code_unit
        categories[Category_Ref('callable')]     = callable_cat
        obj_id__from_seed                        = Obj_Id.from_seed('test:taxonomy:code_elements')
        return Schema__Taxonomy(taxonomy_id   = Taxonomy_Id(obj_id__from_seed)              ,
                                taxonomy_ref  = Taxonomy_Ref('code_elements')               ,
                                version       = Safe_Str__Version('1.0.0')                  ,
                                description   = Safe_Str__Text('Code elements taxonomy')    ,
                                root_category = Category_Ref('code_element')                ,
                                categories    = categories                                  )

    @type_safe
    def create_taxonomy__minimal(self) -> Schema__Taxonomy:                              # Minimal single-category taxonomy
        root = self.create_category(category_ref = Category_Ref('root')              ,
                                    description  = Safe_Str__Text('Root category')   )

        categories = Dict__Categories__By_Ref()
        categories[Category_Ref('root')] = root

        return Schema__Taxonomy(taxonomy_id   = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy:minimal')),
                                taxonomy_ref  = Taxonomy_Ref('minimal')                               ,
                                version       = Safe_Str__Version('1.0.0')                            ,
                                description   = Safe_Str__Text('Minimal test taxonomy')               ,
                                root_category = Category_Ref('root')                                  ,
                                categories    = categories                                            )

    # ═══════════════════════════════════════════════════════════════════════════
    # Ontology Creation
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_relationship(self                              ,
                            inverse : Safe_Str__Ontology__Verb,
                            targets : List__Node_Type_Refs    ) -> Schema__Ontology__Relationship:
        return Schema__Ontology__Relationship(inverse = inverse,
                                              targets = targets)

    @type_safe
    def create_node_type(self                                            ,
                         description   : Safe_Str__Text                  ,
                         taxonomy_ref  : Category_Ref                    ,
                         relationships : Dict__Relationships__By_Verb = None) -> Schema__Ontology__Node_Type:
        return Schema__Ontology__Node_Type(description   = description                              ,
                                           taxonomy_ref  = taxonomy_ref                             ,
                                           relationships = relationships or Dict__Relationships__By_Verb())

    @type_safe
    def create_ontology__code_structure(self) -> Schema__Ontology:                       # Standard code structure ontology
        contains_rel = self.create_relationship(inverse = Safe_Str__Ontology__Verb('in')                           ,
                                                targets = List__Node_Type_Refs([Node_Type_Ref('class')  ,
                                                                                 Node_Type_Ref('method'),
                                                                                 Node_Type_Ref('function')]))

        in_rel = self.create_relationship(inverse = Safe_Str__Ontology__Verb('contains'),
                                          targets = List__Node_Type_Refs([Node_Type_Ref('class'),
                                                                          Node_Type_Ref('module')]))

        calls_rel = self.create_relationship(inverse = Safe_Str__Ontology__Verb('called_by')                   ,
                                             targets = List__Node_Type_Refs([Node_Type_Ref('method')  ,
                                                                              Node_Type_Ref('function')]))

        module_rels = Dict__Relationships__By_Verb()
        module_rels[Safe_Str__Ontology__Verb('contains')] = contains_rel

        class_rels = Dict__Relationships__By_Verb()
        class_rels[Safe_Str__Ontology__Verb('contains')] = self.create_relationship(
            inverse = Safe_Str__Ontology__Verb('in'),
            targets = List__Node_Type_Refs([Node_Type_Ref('method')]))
        class_rels[Safe_Str__Ontology__Verb('in')] = in_rel

        method_rels = Dict__Relationships__By_Verb()
        method_rels[Safe_Str__Ontology__Verb('in')]    = in_rel
        method_rels[Safe_Str__Ontology__Verb('calls')] = calls_rel

        function_rels = Dict__Relationships__By_Verb()
        function_rels[Safe_Str__Ontology__Verb('in')]    = in_rel
        function_rels[Safe_Str__Ontology__Verb('calls')] = calls_rel

        node_types = Dict__Node_Types__By_Ref()
        node_types[Node_Type_Ref('module')]   = self.create_node_type(description   = Safe_Str__Text('Python module'),
                                                                       taxonomy_ref  = Category_Ref('container')      ,
                                                                       relationships = module_rels                    )
        node_types[Node_Type_Ref('class')]    = self.create_node_type(description   = Safe_Str__Text('Python class') ,
                                                                       taxonomy_ref  = Category_Ref('container')      ,
                                                                       relationships = class_rels                     )
        node_types[Node_Type_Ref('method')]   = self.create_node_type(description   = Safe_Str__Text('Class method') ,
                                                                       taxonomy_ref  = Category_Ref('callable')       ,
                                                                       relationships = method_rels                    )
        node_types[Node_Type_Ref('function')] = self.create_node_type(description   = Safe_Str__Text('Standalone function'),
                                                                       taxonomy_ref  = Category_Ref('callable')            ,
                                                                       relationships = function_rels                       )
        obj_id__from_seed                    = Obj_Id.from_seed('test:ontology:code_structure')

        return Schema__Ontology(ontology_id   = Ontology_Id(obj_id__from_seed)                               ,
                                ontology_ref  = Ontology_Ref('code_structure')                               ,
                                version       = Safe_Str__Version('1.0.0')                                   ,
                                description   = Safe_Str__Text('Python code structure ontology')             ,
                                taxonomy_ref  = Taxonomy_Ref('code_elements')                                ,
                                node_types    = node_types                                                   )

    @type_safe
    def create_ontology__minimal(self) -> Schema__Ontology:                              # Minimal ontology with single node type
        node_types = Dict__Node_Types__By_Ref()
        node_types[Node_Type_Ref('entity')] = self.create_node_type(
            description  = Safe_Str__Text('Generic entity'),
            taxonomy_ref = Category_Ref('root')            )

        return Schema__Ontology(ontology_id   = Ontology_Id(Obj_Id.from_seed('test:ontology:minimal')),
                                ontology_ref  = Ontology_Ref('minimal')                               ,
                                version       = Safe_Str__Version('1.0.0')                            ,
                                description   = Safe_Str__Text('Minimal test ontology')               ,
                                taxonomy_ref  = Taxonomy_Ref('minimal')                               ,
                                node_types    = node_types                                            )

    # ═══════════════════════════════════════════════════════════════════════════
    # Rule Set Creation
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_rule_set__code_structure(self) -> Schema__Rule_Set:                       # Rules for code structure
        transitivity_rules = List__Rules__Transitivity()
        transitivity_rules.append(Schema__Rule__Transitivity(source_type = Node_Type_Ref('method'),
                                                             verb        = Safe_Str__Ontology__Verb('in'),
                                                             target_type = Node_Type_Ref('module')        ))

        cardinality_rules = List__Rules__Cardinality()
        cardinality_rules.append(Schema__Rule__Cardinality(source_type = Node_Type_Ref('method')              ,
                                                           verb        = Safe_Str__Ontology__Verb('in')       ,
                                                           target_type = Node_Type_Ref('class')               ,
                                                           min_targets = Safe_UInt(1)                         ,
                                                           max_targets = Safe_UInt(1)                         ,
                                                           description = Safe_Str__Text('Method must be in exactly one class')))
        obj_id__from_seed = Obj_Id.from_seed('test:rules:code_structure')

        return Schema__Rule_Set(rule_set_id        = Rule_Set_Id(obj_id__from_seed)                            ,
                                rule_set_ref       = Rule_Set_Ref('code_structure_rules')                      ,
                                ontology_ref       = Ontology_Ref('code_structure')                            ,
                                version            = Safe_Str__Version('1.0.0')                                ,
                                description        = Safe_Str__Text('Code structure validation rules')         ,
                                transitivity_rules = transitivity_rules                                        ,
                                cardinality_rules  = cardinality_rules                                         )

    @type_safe
    def create_rule_set__empty(self) -> Schema__Rule_Set:                                # Empty rule set for testing
        return Schema__Rule_Set(rule_set_id        = Rule_Set_Id(Obj_Id.from_seed('test:rules:empty')),
                                rule_set_ref       = Rule_Set_Ref('empty_rules')                      ,
                                ontology_ref       = Ontology_Ref('minimal')                          ,
                                version            = Safe_Str__Version('1.0.0')                       ,
                                description        = Safe_Str__Text('Empty rule set for testing')     ,
                                transitivity_rules = List__Rules__Transitivity()                      ,
                                cardinality_rules  = List__Rules__Cardinality()                       )

    # ═══════════════════════════════════════════════════════════════════════════
    # Graph Creation
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_node(self                               ,
                    node_type   : Node_Type_Ref        ,
                    name        : Safe_Str__Id         ,
                    seed        : Safe_Str__Id__Seed = None,
                    line_number : Safe_UInt          = None) -> Schema__Semantic_Graph__Node:
        if seed:
            node_id     = Node_Id(Obj_Id.from_seed(seed))
            node_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                             seed        = seed                               )
        else:
            node_id     = Node_Id(Obj_Id())
            node_source = None

        return Schema__Semantic_Graph__Node(node_id        = node_id                    ,
                                            node_id_source = node_source                ,
                                            node_type      = node_type                  ,
                                            name           = name                       ,
                                            line_number    = line_number or Safe_UInt(0))

    @type_safe
    def create_edge(self                                  ,
                    from_node   : Node_Id                 ,
                    verb        : Safe_Str__Ontology__Verb,
                    to_node     : Node_Id                 ,
                    seed        : Safe_Str__Id__Seed = None,
                    line_number : Safe_UInt          = None) -> Schema__Semantic_Graph__Edge:
        if seed:
            edge_id     = Edge_Id(Obj_Id.from_seed(seed))
            edge_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                             seed        = seed                               )
        else:
            edge_id     = Edge_Id(Obj_Id())
            edge_source = None

        return Schema__Semantic_Graph__Edge(edge_id        = edge_id                        ,
                                            edge_id_source = edge_source                    ,
                                            from_node      = from_node                      ,
                                            verb           = verb                           ,
                                            to_node        = to_node                        ,
                                            line_number    = line_number or Safe_UInt(0)    )

    @type_safe
    def create_graph__simple_class(self) -> Schema__Semantic_Graph:                      # Graph with module → class → method
        module_node = self.create_node(node_type = Node_Type_Ref('module')                      ,
                                       name      = Safe_Str__Id('my_module')                    ,
                                       seed      = Safe_Str__Id__Seed('test:node:my_module')    )

        class_node = self.create_node(node_type = Node_Type_Ref('class')                        ,
                                      name      = Safe_Str__Id('MyClass')                       ,
                                      seed      = Safe_Str__Id__Seed('test:node:MyClass')       )

        method_node = self.create_node(node_type   = Node_Type_Ref('method')                    ,
                                       name        = Safe_Str__Id('my_method')                  ,
                                       seed        = Safe_Str__Id__Seed('test:node:my_method')  ,
                                       line_number = Safe_UInt(10)                              )

        nodes = Dict__Nodes__By_Id()
        nodes[module_node.node_id] = module_node
        nodes[class_node.node_id]  = class_node
        nodes[method_node.node_id] = method_node

        edges = List__Semantic_Graph__Edges()
        edges.append(self.create_edge(from_node = module_node.node_id                                 ,
                                      verb      = Safe_Str__Ontology__Verb('contains')                ,
                                      to_node   = class_node.node_id                                  ,
                                      seed      = Safe_Str__Id__Seed('test:edge:module_contains_class')))

        edges.append(self.create_edge(from_node = class_node.node_id                                  ,
                                      verb      = Safe_Str__Ontology__Verb('contains')                ,
                                      to_node   = method_node.node_id                                 ,
                                      seed      = Safe_Str__Id__Seed('test:edge:class_contains_method')))

        obj_id__from_seed = Obj_Id.from_seed('test:graph:simple_class')

        return Schema__Semantic_Graph(graph_id     = Graph_Id(obj_id__from_seed)                          ,
                                      ontology_ref = Ontology_Ref('code_structure')                       ,
                                      rule_set_ref = Rule_Set_Ref('code_structure_rules')                 ,
                                      version      = Safe_Str__Version('1.0.0')                           ,
                                      nodes        = nodes                                                ,
                                      edges        = edges                                                )

    @type_safe
    def create_graph__empty(self) -> Schema__Semantic_Graph:                             # Empty graph for testing
        return Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id.from_seed('test:graph:empty')),
                                      ontology_ref = Ontology_Ref('empty')                       ,
                                      rule_set_ref = Rule_Set_Ref()                                ,
                                      version      = Safe_Str__Version('1.0.0')                    ,
                                      nodes        = Dict__Nodes__By_Id()                          ,
                                      edges        = List__Semantic_Graph__Edges()                 )

    # ═══════════════════════════════════════════════════════════════════════════
    # ID Helpers
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def deterministic_node_id(self, seed: Safe_Str__Id__Seed) -> Node_Id:                # Create deterministic node ID
        return Node_Id(Obj_Id.from_seed(seed))

    @type_safe
    def deterministic_edge_id(self, seed: Safe_Str__Id__Seed) -> Edge_Id:                # Create deterministic edge ID
        return Edge_Id(Obj_Id.from_seed(seed))

    @type_safe
    def deterministic_graph_id(self, seed: Safe_Str__Id__Seed) -> Graph_Id:              # Create deterministic graph ID
        return Graph_Id(Obj_Id.from_seed(seed))


# ═══════════════════════════════════════════════════════════════════════════
# Deterministic Obj_Id Constants (Canonical Test IDs)
#
# note: all values are casted to str so that the assert is easier to make
# ═══════════════════════════════════════════════════════════════════════════


OBJ_ID__FOR__TAXONOMY__CODE_ELEMENTS     = str(Obj_Id.from_seed('test:taxonomy:code_elements'))          # --- Taxonomies ---
OBJ_ID__FOR__TAXONOMY__MINIMAL           = str(Obj_Id.from_seed('test:taxonomy:minimal'      ))


OBJ_ID__FOR__ONTOLOGY__CODE_STRUCTURE    = str(Obj_Id.from_seed('test:ontology:code_structure'))         # --- Ontologies ---
OBJ_ID__FOR__ONTOLOGY__MINIMAL           = str(Obj_Id.from_seed('test:ontology:minimal'       ))


OBJ_ID__FOR__RULE_SET__CODE_STRUCTURE    = str(Obj_Id.from_seed('test:rules:code_structure'))            # --- Rule Sets ---
OBJ_ID__FOR__RULE_SET__EMPTY             = str(Obj_Id.from_seed('test:rules:empty'         ))


OBJ_ID__FOR__GRAPH__SIMPLE_CLASS         = str(Obj_Id.from_seed('test:graph:simple_class'))              # --- Graphs ---
OBJ_ID__FOR__GRAPH__EMPTY                = str(Obj_Id.from_seed('test:graph:empty'       ))


OBJ_ID__FOR__NODE__MY_MODULE             = str(Obj_Id.from_seed('test:node:my_module'))                  # --- Nodes ---
OBJ_ID__FOR__NODE__MY_CLASS              = str(Obj_Id.from_seed('test:node:MyClass'  ))
OBJ_ID__FOR__NODE__MY_METHOD             = str(Obj_Id.from_seed('test:node:my_method'))

OBJ_ID__FOR__EDGE__MODULE_CONTAINS_CLASS = str(Obj_Id.from_seed('test:edge:module_contains_class'))     # --- Edges ---
OBJ_ID__FOR__EDGE__CLASS_CONTAINS_METHOD = str(Obj_Id.from_seed('test:edge:class_contains_method'))
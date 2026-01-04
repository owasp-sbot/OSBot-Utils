# ═══════════════════════════════════════════════════════════════════════════════
# QA__Semantic_Graphs__Test_Data - Reusable test data factories for semantic graphs
#
# Updated for Brief 3.7:
#   - Ontologies use predicates dict + edge_rules list (normalized)
#   - Node types have node_type_id (no embedded relationships)
#   - Edges use predicate_id (not verb)
#   - All cross-references use IDs
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Ref      import Dict__Categories__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id       import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id            import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicates__By_Id       import Dict__Predicates__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Refs           import List__Category_Refs
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Edge_Rules              import List__Edge_Rules
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Cardinality      import List__Rules__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Transitivity     import List__Rules__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges   import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph             import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge       import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node       import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                  import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type               import Enum__Id__Source_Type
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                  import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                 import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                   import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref                  import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                  import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref                 import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                   import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref                  import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source            import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                   import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref                  import Taxonomy_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Edge_Rule     import Schema__Ontology__Edge_Rule
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type     import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Predicate     import Schema__Ontology__Predicate
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                    import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality           import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity          import Schema__Rule__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy                import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category      import Schema__Taxonomy__Category
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb        import Safe_Str__Ontology__Verb
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
    # Node Type Creation (now with IDs)
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_node_type(self                                     ,
                         node_type_ref : Node_Type_Ref            ,
                         description   : Safe_Str__Text     = None,
                         seed          : Safe_Str__Id__Seed = None) -> Schema__Ontology__Node_Type:
        if seed:
            node_type_id        = Node_Type_Id(Obj_Id.from_seed(seed))
            node_type_id_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                                     seed        = seed                               )
        else:
            node_type_id        = Node_Type_Id(Obj_Id())
            node_type_id_source = None

        return Schema__Ontology__Node_Type(node_type_id        = node_type_id       ,
                                           node_type_id_source = node_type_id_source,
                                           node_type_ref       = node_type_ref      ,
                                           description         = description        )

    # ═══════════════════════════════════════════════════════════════════════════
    # Predicate Creation (new)
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_predicate(self                               ,
                         predicate_ref : Predicate_Ref      ,
                         inverse_id    : Predicate_Id  = None,
                         description   : Safe_Str__Text = None,
                         seed          : Safe_Str__Id__Seed = None) -> Schema__Ontology__Predicate:
        if seed:
            predicate_id        = Predicate_Id(Obj_Id.from_seed(seed))
            predicate_id_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                                     seed        = seed                               )
        else:
            predicate_id        = Predicate_Id(Obj_Id())
            predicate_id_source = None

        return Schema__Ontology__Predicate(predicate_id        = predicate_id       ,
                                           predicate_id_source = predicate_id_source,
                                           predicate_ref       = predicate_ref      ,
                                           inverse_id          = inverse_id         ,
                                           description         = description        )

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Rule Creation (new)
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_edge_rule(self                           ,
                         source_type_id : Node_Type_Id  ,
                         predicate_id   : Predicate_Id  ,
                         target_type_id : Node_Type_Id  ) -> Schema__Ontology__Edge_Rule:
        return Schema__Ontology__Edge_Rule(source_type_id = source_type_id,
                                           predicate_id   = predicate_id  ,
                                           target_type_id = target_type_id)

    # ═══════════════════════════════════════════════════════════════════════════
    # Ontology Creation (normalized structure)
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_ontology__code_structure(self) -> Schema__Ontology:                       # Standard code structure ontology
        # Create node types with IDs
        module_type   = self.create_node_type(node_type_ref = Node_Type_Ref('module')  ,
                                              description   = Safe_Str__Text('Python module'),
                                              seed          = Safe_Str__Id__Seed('test:node_type:module'))
        class_type    = self.create_node_type(node_type_ref = Node_Type_Ref('class')   ,
                                              description   = Safe_Str__Text('Python class'),
                                              seed          = Safe_Str__Id__Seed('test:node_type:class'))
        method_type   = self.create_node_type(node_type_ref = Node_Type_Ref('method')  ,
                                              description   = Safe_Str__Text('Class method'),
                                              seed          = Safe_Str__Id__Seed('test:node_type:method'))
        function_type = self.create_node_type(node_type_ref = Node_Type_Ref('function'),
                                              description   = Safe_Str__Text('Standalone function'),
                                              seed          = Safe_Str__Id__Seed('test:node_type:function'))

        node_types = Dict__Node_Types__By_Id()
        node_types[module_type.node_type_id]   = module_type
        node_types[class_type.node_type_id]    = class_type
        node_types[method_type.node_type_id]   = method_type
        node_types[function_type.node_type_id] = function_type

        # Create predicates with IDs (linked pairs)
        contains_id  = Predicate_Id(Obj_Id.from_seed('test:predicate:contains'))
        in_id        = Predicate_Id(Obj_Id.from_seed('test:predicate:in'))
        calls_id     = Predicate_Id(Obj_Id.from_seed('test:predicate:calls'))
        called_by_id = Predicate_Id(Obj_Id.from_seed('test:predicate:called_by'))

        contains_pred  = self.create_predicate(predicate_ref = Predicate_Ref('contains')  ,
                                               inverse_id    = in_id                       ,
                                               description   = Safe_Str__Text('Contains child'),
                                               seed          = Safe_Str__Id__Seed('test:predicate:contains'))
        in_pred        = self.create_predicate(predicate_ref = Predicate_Ref('in')        ,
                                               inverse_id    = contains_id                 ,
                                               description   = Safe_Str__Text('Is contained in'),
                                               seed          = Safe_Str__Id__Seed('test:predicate:in'))
        calls_pred     = self.create_predicate(predicate_ref = Predicate_Ref('calls')     ,
                                               inverse_id    = called_by_id                ,
                                               description   = Safe_Str__Text('Calls'),
                                               seed          = Safe_Str__Id__Seed('test:predicate:calls'))
        called_by_pred = self.create_predicate(predicate_ref = Predicate_Ref('called_by') ,
                                               inverse_id    = calls_id                    ,
                                               description   = Safe_Str__Text('Called by'),
                                               seed          = Safe_Str__Id__Seed('test:predicate:called_by'))

        predicates = Dict__Predicates__By_Id()
        predicates[contains_pred.predicate_id]  = contains_pred
        predicates[in_pred.predicate_id]        = in_pred
        predicates[calls_pred.predicate_id]     = calls_pred
        predicates[called_by_pred.predicate_id] = called_by_pred

        # Create edge rules
        edge_rules = List__Edge_Rules()
        # module contains class/method/function
        edge_rules.append(self.create_edge_rule(module_type.node_type_id, contains_id, class_type.node_type_id))
        edge_rules.append(self.create_edge_rule(module_type.node_type_id, contains_id, method_type.node_type_id))
        edge_rules.append(self.create_edge_rule(module_type.node_type_id, contains_id, function_type.node_type_id))
        # class contains method
        edge_rules.append(self.create_edge_rule(class_type.node_type_id, contains_id, method_type.node_type_id))
        # class/method/function in module
        edge_rules.append(self.create_edge_rule(class_type.node_type_id, in_id, module_type.node_type_id))
        edge_rules.append(self.create_edge_rule(method_type.node_type_id, in_id, module_type.node_type_id))
        edge_rules.append(self.create_edge_rule(method_type.node_type_id, in_id, class_type.node_type_id))
        edge_rules.append(self.create_edge_rule(function_type.node_type_id, in_id, module_type.node_type_id))
        # method/function calls method/function
        edge_rules.append(self.create_edge_rule(method_type.node_type_id, calls_id, method_type.node_type_id))
        edge_rules.append(self.create_edge_rule(method_type.node_type_id, calls_id, function_type.node_type_id))
        edge_rules.append(self.create_edge_rule(function_type.node_type_id, calls_id, method_type.node_type_id))
        edge_rules.append(self.create_edge_rule(function_type.node_type_id, calls_id, function_type.node_type_id))

        obj_id__from_seed = Obj_Id.from_seed('test:ontology:code_structure')
        taxonomy_id       = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy:code_elements'))

        return Schema__Ontology(ontology_id   = Ontology_Id(obj_id__from_seed)                   ,
                                ontology_ref  = Ontology_Ref('code_structure')                   ,
                                description   = Safe_Str__Text('Python code structure ontology') ,
                                taxonomy_id   = taxonomy_id                                      ,
                                node_types    = node_types                                       ,
                                predicates    = predicates                                       ,
                                edge_rules    = edge_rules                                       )

    @type_safe
    def create_ontology__minimal(self) -> Schema__Ontology:                              # Minimal ontology with single node type
        entity_type = self.create_node_type(node_type_ref = Node_Type_Ref('entity')       ,
                                            description   = Safe_Str__Text('Generic entity'),
                                            seed          = Safe_Str__Id__Seed('test:node_type:entity'))

        node_types = Dict__Node_Types__By_Id()
        node_types[entity_type.node_type_id] = entity_type

        return Schema__Ontology(ontology_id   = Ontology_Id(Obj_Id.from_seed('test:ontology:minimal')),
                                ontology_ref  = Ontology_Ref('minimal')                               ,
                                description   = Safe_Str__Text('Minimal test ontology')               ,
                                taxonomy_id   = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy:minimal')),
                                node_types    = node_types                                            ,
                                predicates    = Dict__Predicates__By_Id()                             ,
                                edge_rules    = List__Edge_Rules()                                    )

    # ═══════════════════════════════════════════════════════════════════════════
    # Rule Set Creation
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_rule_set__code_structure(self) -> Schema__Rule_Set:                       # Rules for code structure

        transitivity_rules = List__Rules__Transitivity()
        transitivity_rules.append(Schema__Rule__Transitivity(source_type = Node_Type_Ref('method')         ,
                                                             verb        = Safe_Str__Ontology__Verb('in')  ,
                                                             target_type = Node_Type_Ref('module')         ))

        cardinality_rules = List__Rules__Cardinality()
        cardinality_rules.append(Schema__Rule__Cardinality(source_type = Node_Type_Ref('method')              ,
                                                           verb        = Safe_Str__Ontology__Verb('in')       ,
                                                           target_type = Node_Type_Ref('class')               ,
                                                           min_targets = Safe_UInt(1)                         ,
                                                           max_targets = Safe_UInt(1)                         ,
                                                           description = Safe_Str__Text('Method must be in exactly one class')))
        obj_id__from_seed = Obj_Id.from_seed('test:rules:code_structure')
        ontology_id       = Ontology_Id(Obj_Id.from_seed('test:ontology:code_structure'))

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
    # Graph Creation (ID-based)
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_node(self                               ,
                    node_type_id : Node_Type_Id        ,
                    name         : Safe_Str__Id        ,
                    seed         : Safe_Str__Id__Seed = None) -> Schema__Semantic_Graph__Node:
        if seed:
            node_id     = Node_Id(Obj_Id.from_seed(seed))
            node_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                             seed        = seed                               )
        else:
            node_id     = Node_Id(Obj_Id())
            node_source = None

        return Schema__Semantic_Graph__Node(node_id        = node_id     ,
                                            node_id_source = node_source ,
                                            node_type_id   = node_type_id,
                                            name           = name        )

    @type_safe
    def create_edge(self                                  ,
                    from_node_id : Node_Id                ,
                    predicate_id : Predicate_Id           ,
                    to_node_id   : Node_Id                ,
                    seed         : Safe_Str__Id__Seed = None) -> Schema__Semantic_Graph__Edge:
        if seed:
            edge_id     = Edge_Id(Obj_Id.from_seed(seed))
            edge_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                             seed        = seed                               )
        else:
            edge_id     = Edge_Id(Obj_Id())
            edge_source = None

        return Schema__Semantic_Graph__Edge(edge_id        = edge_id     ,
                                            edge_id_source = edge_source ,
                                            from_node_id   = from_node_id,
                                            to_node_id     = to_node_id  ,
                                            predicate_id   = predicate_id)

    @type_safe
    def create_graph__simple_class(self) -> Schema__Semantic_Graph:                      # Graph with module → class → method
        # Get node type IDs
        module_type_id   = Node_Type_Id(Obj_Id.from_seed('test:node_type:module'))
        class_type_id    = Node_Type_Id(Obj_Id.from_seed('test:node_type:class'))
        method_type_id   = Node_Type_Id(Obj_Id.from_seed('test:node_type:method'))
        contains_pred_id = Predicate_Id(Obj_Id.from_seed('test:predicate:contains'))

        # Create nodes
        module_node = self.create_node(node_type_id = module_type_id                     ,
                                       name         = Safe_Str__Id('my_module')          ,
                                       seed         = Safe_Str__Id__Seed('test:node:my_module'))

        class_node = self.create_node(node_type_id = class_type_id                       ,
                                      name         = Safe_Str__Id('MyClass')             ,
                                      seed         = Safe_Str__Id__Seed('test:node:MyClass'))

        method_node = self.create_node(node_type_id = method_type_id                     ,
                                       name         = Safe_Str__Id('my_method')          ,
                                       seed         = Safe_Str__Id__Seed('test:node:my_method'))

        nodes = Dict__Nodes__By_Id()
        nodes[module_node.node_id] = module_node
        nodes[class_node.node_id]  = class_node
        nodes[method_node.node_id] = method_node

        # Create edges
        edges = List__Semantic_Graph__Edges()
        edges.append(self.create_edge(from_node_id = module_node.node_id                              ,
                                      predicate_id = contains_pred_id                                 ,
                                      to_node_id   = class_node.node_id                               ,
                                      seed         = Safe_Str__Id__Seed('test:edge:module_contains_class')))

        edges.append(self.create_edge(from_node_id = class_node.node_id                               ,
                                      predicate_id = contains_pred_id                                 ,
                                      to_node_id   = method_node.node_id                              ,
                                      seed         = Safe_Str__Id__Seed('test:edge:class_contains_method')))

        obj_id__from_seed = Obj_Id.from_seed('test:graph:simple_class')
        ontology_id       = Ontology_Id(Obj_Id.from_seed('test:ontology:code_structure'))
        rule_set_id       = Rule_Set_Id(Obj_Id.from_seed('test:rules:code_structure'))

        return Schema__Semantic_Graph(graph_id    = Graph_Id(obj_id__from_seed),
                                      ontology_id = ontology_id               ,
                                      rule_set_id = rule_set_id               ,
                                      nodes       = nodes                     ,
                                      edges       = edges                     )

    @type_safe
    def create_graph__empty(self) -> Schema__Semantic_Graph:                             # Empty graph for testing
        return Schema__Semantic_Graph(graph_id    = Graph_Id(Obj_Id.from_seed('test:graph:empty')),
                                      ontology_id = Ontology_Id()                                 ,
                                      rule_set_id = Rule_Set_Id()                                 ,
                                      nodes       = Dict__Nodes__By_Id()                          ,
                                      edges       = List__Semantic_Graph__Edges()                 )

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

    @type_safe
    def deterministic_node_type_id(self, seed: Safe_Str__Id__Seed) -> Node_Type_Id:      # Create deterministic node type ID
        return Node_Type_Id(Obj_Id.from_seed(seed))

    @type_safe
    def deterministic_predicate_id(self, seed: Safe_Str__Id__Seed) -> Predicate_Id:      # Create deterministic predicate ID
        return Predicate_Id(Obj_Id.from_seed(seed))

    # ═══════════════════════════════════════════════════════════════════════════
    # Ontology
    # ═══════════════════════════════════════════════════════════════════════════

    def create_test_ontology(self) -> Schema__Ontology:                                      # Build test ontology with rich relationships
        # Create node type IDs
        ontology_id = Ontology_Id (Obj_Id.from_seed('test:ontology:id'  ))
        module_id   = Node_Type_Id(Obj_Id.from_seed('test:nt:module'    ))
        class_id    = Node_Type_Id(Obj_Id.from_seed('test:nt:class'     ))
        method_id   = Node_Type_Id(Obj_Id.from_seed('test:nt:method'    ))
        function_id = Node_Type_Id(Obj_Id.from_seed('test:nt:function'  ))

        # Create node types
        node_types = Dict__Node_Types__By_Id()
        node_types[module_id]   = Schema__Ontology__Node_Type(node_type_id  = module_id                  ,
                                                               node_type_ref = Node_Type_Ref('module')   ,
                                                               description   = Safe_Str__Text('Python module'))
        node_types[class_id]    = Schema__Ontology__Node_Type(node_type_id  = class_id                   ,
                                                               node_type_ref = Node_Type_Ref('class')    ,
                                                               description   = Safe_Str__Text('Python class'))
        node_types[method_id]   = Schema__Ontology__Node_Type(node_type_id  = method_id                  ,
                                                               node_type_ref = Node_Type_Ref('method')   ,
                                                               description   = Safe_Str__Text('Python method'))
        node_types[function_id] = Schema__Ontology__Node_Type(node_type_id  = function_id                ,
                                                               node_type_ref = Node_Type_Ref('function') ,
                                                               description   = Safe_Str__Text('Python function'))

        # Create predicate IDs
        defines_id      = Predicate_Id(Obj_Id.from_seed('test:pred:defines'      ))
        defined_in_id   = Predicate_Id(Obj_Id.from_seed('test:pred:defined_in'   ))
        imports_id      = Predicate_Id(Obj_Id.from_seed('test:pred:imports'      ))
        imported_by_id  = Predicate_Id(Obj_Id.from_seed('test:pred:imported_by'  ))
        has_id          = Predicate_Id(Obj_Id.from_seed('test:pred:has'          ))
        in_id           = Predicate_Id(Obj_Id.from_seed('test:pred:in'           ))
        inherits_id     = Predicate_Id(Obj_Id.from_seed('test:pred:inherits_from'))
        inherited_by_id = Predicate_Id(Obj_Id.from_seed('test:pred:inherited_by' ))
        calls_id        = Predicate_Id(Obj_Id.from_seed('test:pred:calls'        ))
        called_by_id    = Predicate_Id(Obj_Id.from_seed('test:pred:called_by'    ))

        # Create predicates with inverses
        predicates = Dict__Predicates__By_Id()
        predicates[defines_id]      = Schema__Ontology__Predicate(predicate_id  = defines_id                    ,
                                                                   predicate_ref = Predicate_Ref('defines')     ,
                                                                   inverse_id    = defined_in_id                )
        predicates[defined_in_id]   = Schema__Ontology__Predicate(predicate_id  = defined_in_id                 ,
                                                                   predicate_ref = Predicate_Ref('defined_in')  ,
                                                                   inverse_id    = defines_id                   )
        predicates[imports_id]      = Schema__Ontology__Predicate(predicate_id  = imports_id                    ,
                                                                   predicate_ref = Predicate_Ref('imports')     ,
                                                                   inverse_id    = imported_by_id               )
        predicates[imported_by_id]  = Schema__Ontology__Predicate(predicate_id  = imported_by_id                ,
                                                                   predicate_ref = Predicate_Ref('imported_by') ,
                                                                   inverse_id    = imports_id                   )
        predicates[has_id]          = Schema__Ontology__Predicate(predicate_id  = has_id                        ,
                                                                   predicate_ref = Predicate_Ref('has')         ,
                                                                   inverse_id    = in_id                        )
        predicates[in_id]           = Schema__Ontology__Predicate(predicate_id  = in_id                         ,
                                                                   predicate_ref = Predicate_Ref('in')          ,
                                                                   inverse_id    = has_id                       )
        predicates[inherits_id]     = Schema__Ontology__Predicate(predicate_id  = inherits_id                   ,
                                                                   predicate_ref = Predicate_Ref('inherits_from'),
                                                                   inverse_id    = inherited_by_id              )
        predicates[inherited_by_id] = Schema__Ontology__Predicate(predicate_id  = inherited_by_id               ,
                                                                   predicate_ref = Predicate_Ref('inherited_by'),
                                                                   inverse_id    = inherits_id                  )
        predicates[calls_id]        = Schema__Ontology__Predicate(predicate_id  = calls_id                      ,
                                                                   predicate_ref = Predicate_Ref('calls')       ,
                                                                   inverse_id    = called_by_id                 )
        predicates[called_by_id]    = Schema__Ontology__Predicate(predicate_id  = called_by_id                  ,
                                                                   predicate_ref = Predicate_Ref('called_by')   ,
                                                                   inverse_id    = calls_id                     )

        # Create edge rules
        edge_rules = List__Edge_Rules()
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=module_id, predicate_id=defines_id, target_type_id=class_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=module_id, predicate_id=defines_id, target_type_id=function_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=module_id, predicate_id=imports_id, target_type_id=module_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=class_id,  predicate_id=has_id,     target_type_id=method_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=class_id,  predicate_id=inherits_id,target_type_id=class_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=method_id, predicate_id=calls_id,   target_type_id=method_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=method_id, predicate_id=calls_id,   target_type_id=function_id))

        return Schema__Ontology(ontology_id  = ontology_id                                 ,
                                ontology_ref = Ontology_Ref('test_ontology')               ,
                                description  = Safe_Str__Text('Test ontology')             ,
                                node_types   = node_types                                  ,
                                predicates   = predicates                                  ,
                                edge_rules   = edge_rules                                  )

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


OBJ_ID__FOR__EDGE__MODULE_CONTAINS_CLASS = str(Obj_Id.from_seed('test:edge:module_contains_class'))      # --- Edges ---
OBJ_ID__FOR__EDGE__CLASS_CONTAINS_METHOD = str(Obj_Id.from_seed('test:edge:class_contains_method'))


OBJ_ID__FOR__NODE_TYPE__MODULE           = str(Obj_Id.from_seed('test:node_type:module'))                # --- Node Types ---
OBJ_ID__FOR__NODE_TYPE__CLASS            = str(Obj_Id.from_seed('test:node_type:class'))
OBJ_ID__FOR__NODE_TYPE__METHOD           = str(Obj_Id.from_seed('test:node_type:method'))
OBJ_ID__FOR__NODE_TYPE__FUNCTION         = str(Obj_Id.from_seed('test:node_type:function'))
OBJ_ID__FOR__NODE_TYPE__ENTITY           = str(Obj_Id.from_seed('test:node_type:entity'))


OBJ_ID__FOR__PREDICATE__CONTAINS         = str(Obj_Id.from_seed('test:predicate:contains'))              # --- Predicates ---
OBJ_ID__FOR__PREDICATE__IN               = str(Obj_Id.from_seed('test:predicate:in'))
OBJ_ID__FOR__PREDICATE__CALLS            = str(Obj_Id.from_seed('test:predicate:calls'))
OBJ_ID__FOR__PREDICATE__CALLED_BY        = str(Obj_Id.from_seed('test:predicate:called_by'))
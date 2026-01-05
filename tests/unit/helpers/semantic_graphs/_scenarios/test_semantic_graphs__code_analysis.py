# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic Graphs - Code Analysis Scenario
#
# Demonstrates semantic graphs for Python code analysis:
#   - Taxonomy: code_element → callable, container, data
#   - Ontology: module, class, method, function with relationships
#   - Rules: methods must be in classes, functions in modules
#   - Graph: actual code structure representation
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                   import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Id             import Dict__Categories__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id             import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id                  import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicates__By_Id             import Dict__Predicates__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Names__By_Id         import Dict__Property_Names__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Types__By_Id         import Dict__Property_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Ids                  import List__Category_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Edge_Rules                    import List__Edge_Rules
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Required_Node_Property import List__Rules__Required_Node_Property
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges         import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                         import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                        import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                        import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                       import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                         import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref                        import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                        import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref                       import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id                    import Property_Name_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Ref                   import Property_Name_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Id                    import Property_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Ref                   import Property_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                         import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref                        import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                         import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref                        import Taxonomy_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                      import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Edge_Rule           import Schema__Ontology__Edge_Rule
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type           import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Predicate           import Schema__Ontology__Predicate
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Property_Name       import Schema__Ontology__Property_Name
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Property_Type       import Schema__Ontology__Property_Type
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                          import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Node_Property      import Schema__Rule__Required_Node_Property
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph                   import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge             import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node             import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy                      import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category            import Schema__Taxonomy__Category
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Utils                               import Ontology__Utils
from osbot_utils.helpers.semantic_graphs.taxonomy.Taxonomy__Utils                               import Taxonomy__Utils
from osbot_utils.helpers.semantic_graphs.rule.Rule_Set__Utils                                   import Rule_Set__Utils
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                import Obj_Id


class test_semantic_graphs__code_analysis(TestCase):                                   # Code analysis scenario

    @classmethod
    def setUpClass(cls):                                                               # Build complete code analysis model
        cls.build_taxonomy()
        cls.build_ontology()
        cls.build_rule_set()
        cls.build_graph()

    # ═══════════════════════════════════════════════════════════════════════════
    # Model Construction
    # ═══════════════════════════════════════════════════════════════════════════

    @classmethod
    def build_taxonomy(cls):                                                           # Create code element taxonomy
        # Category IDs
        cls.cat_root_id      = Category_Id(Obj_Id.from_seed('code:cat:root'))
        cls.cat_callable_id  = Category_Id(Obj_Id.from_seed('code:cat:callable'))
        cls.cat_container_id = Category_Id(Obj_Id.from_seed('code:cat:container'))
        cls.cat_data_id      = Category_Id(Obj_Id.from_seed('code:cat:data'))

        # Build hierarchy
        cat_root = Schema__Taxonomy__Category(
            category_id  = cls.cat_root_id                                              ,
            category_ref = Category_Ref('code_element')                                 ,
            parent_id    = None                                                         ,
            child_ids    = List__Category_Ids([cls.cat_callable_id, cls.cat_container_id, cls.cat_data_id])
        )
        cat_callable = Schema__Taxonomy__Category(
            category_id  = cls.cat_callable_id                                          ,
            category_ref = Category_Ref('callable')                                     ,
            parent_id    = cls.cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )
        cat_container = Schema__Taxonomy__Category(
            category_id  = cls.cat_container_id                                         ,
            category_ref = Category_Ref('container')                                    ,
            parent_id    = cls.cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )
        cat_data = Schema__Taxonomy__Category(
            category_id  = cls.cat_data_id                                              ,
            category_ref = Category_Ref('data')                                         ,
            parent_id    = cls.cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )

        categories = Dict__Categories__By_Id()
        categories[cls.cat_root_id]      = cat_root
        categories[cls.cat_callable_id]  = cat_callable
        categories[cls.cat_container_id] = cat_container
        categories[cls.cat_data_id]      = cat_data

        cls.taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('code:taxonomy'))
        cls.taxonomy = Schema__Taxonomy(
            taxonomy_id  = cls.taxonomy_id                                              ,
            taxonomy_ref = Taxonomy_Ref('code_analysis')                                ,
            root_id      = cls.cat_root_id                                              ,
            categories   = categories
        )

    @classmethod
    def build_ontology(cls):                                                           # Create code analysis ontology
        # Node Type IDs
        cls.nt_module_id   = Node_Type_Id(Obj_Id.from_seed('code:nt:module'))
        cls.nt_class_id    = Node_Type_Id(Obj_Id.from_seed('code:nt:class'))
        cls.nt_method_id   = Node_Type_Id(Obj_Id.from_seed('code:nt:method'))
        cls.nt_function_id = Node_Type_Id(Obj_Id.from_seed('code:nt:function'))
        cls.nt_variable_id = Node_Type_Id(Obj_Id.from_seed('code:nt:variable'))

        # Predicate IDs
        cls.pred_contains_id = Predicate_Id(Obj_Id.from_seed('code:pred:contains'))
        cls.pred_in_id       = Predicate_Id(Obj_Id.from_seed('code:pred:in'))
        cls.pred_calls_id    = Predicate_Id(Obj_Id.from_seed('code:pred:calls'))
        cls.pred_inherits_id = Predicate_Id(Obj_Id.from_seed('code:pred:inherits'))

        # Property Type IDs
        cls.pt_string_id = Property_Type_Id(Obj_Id.from_seed('code:pt:string'))
        cls.pt_int_id    = Property_Type_Id(Obj_Id.from_seed('code:pt:int'))

        # Property Name IDs
        cls.pn_line_number_id = Property_Name_Id(Obj_Id.from_seed('code:pn:line_number'))
        cls.pn_file_path_id   = Property_Name_Id(Obj_Id.from_seed('code:pn:file_path'))

        # Node Types (linked to taxonomy categories)
        node_types = Dict__Node_Types__By_Id()
        node_types[cls.nt_module_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_module_id                                            ,
            node_type_ref = Node_Type_Ref('module')                                     ,
            category_id   = cls.cat_container_id
        )
        node_types[cls.nt_class_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_class_id                                             ,
            node_type_ref = Node_Type_Ref('class')                                      ,
            category_id   = cls.cat_container_id
        )
        node_types[cls.nt_method_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_method_id                                            ,
            node_type_ref = Node_Type_Ref('method')                                     ,
            category_id   = cls.cat_callable_id
        )
        node_types[cls.nt_function_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_function_id                                          ,
            node_type_ref = Node_Type_Ref('function')                                   ,
            category_id   = cls.cat_callable_id
        )
        node_types[cls.nt_variable_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_variable_id                                          ,
            node_type_ref = Node_Type_Ref('variable')                                   ,
            category_id   = cls.cat_data_id
        )

        # Predicates (with inverses)
        predicates = Dict__Predicates__By_Id()
        predicates[cls.pred_contains_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_contains_id                                        ,
            predicate_ref = Predicate_Ref('contains')                                   ,
            inverse_id    = cls.pred_in_id
        )
        predicates[cls.pred_in_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_in_id                                              ,
            predicate_ref = Predicate_Ref('in')                                         ,
            inverse_id    = cls.pred_contains_id
        )
        predicates[cls.pred_calls_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_calls_id                                           ,
            predicate_ref = Predicate_Ref('calls')                                      ,
            inverse_id    = None
        )
        predicates[cls.pred_inherits_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_inherits_id                                        ,
            predicate_ref = Predicate_Ref('inherits_from')                              ,
            inverse_id    = None
        )

        # Property Types
        property_types = Dict__Property_Types__By_Id()
        property_types[cls.pt_string_id] = Schema__Ontology__Property_Type(
            property_type_id  = cls.pt_string_id                                        ,
            property_type_ref = Property_Type_Ref('string')
        )
        property_types[cls.pt_int_id] = Schema__Ontology__Property_Type(
            property_type_id  = cls.pt_int_id                                           ,
            property_type_ref = Property_Type_Ref('int')
        )

        # Property Names
        property_names = Dict__Property_Names__By_Id()
        property_names[cls.pn_line_number_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_line_number_id                                   ,
            property_name_ref = Property_Name_Ref('line_number')                        ,
            property_type_id  = cls.pt_int_id
        )
        property_names[cls.pn_file_path_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_file_path_id                                     ,
            property_name_ref = Property_Name_Ref('file_path')                          ,
            property_type_id  = cls.pt_string_id
        )

        # Edge Rules
        edge_rules = List__Edge_Rules()
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_module_id, predicate_id=cls.pred_contains_id, target_type_id=cls.nt_class_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_module_id, predicate_id=cls.pred_contains_id, target_type_id=cls.nt_function_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_class_id,  predicate_id=cls.pred_contains_id, target_type_id=cls.nt_method_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_class_id,  predicate_id=cls.pred_inherits_id, target_type_id=cls.nt_class_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_method_id, predicate_id=cls.pred_calls_id,    target_type_id=cls.nt_method_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_method_id, predicate_id=cls.pred_calls_id,    target_type_id=cls.nt_function_id))

        cls.ontology_id = Ontology_Id(Obj_Id.from_seed('code:ontology'))
        cls.ontology = Schema__Ontology(
            ontology_id    = cls.ontology_id                                            ,
            ontology_ref   = Ontology_Ref('code_analysis')                              ,
            taxonomy_id    = cls.taxonomy_id                                            ,
            node_types     = node_types                                                 ,
            predicates     = predicates                                                 ,
            property_types = property_types                                             ,
            property_names = property_names                                             ,
            edge_rules     = edge_rules
        )

    @classmethod
    def build_rule_set(cls):                                                           # Create validation rules
        required_node_properties = List__Rules__Required_Node_Property()
        required_node_properties.append(Schema__Rule__Required_Node_Property(
            node_type_id     = cls.nt_method_id                                         ,
            property_name_id = cls.pn_line_number_id                                    ,
            required         = True
        ))
        required_node_properties.append(Schema__Rule__Required_Node_Property(
            node_type_id     = cls.nt_module_id                                         ,
            property_name_id = cls.pn_file_path_id                                      ,
            required         = True
        ))

        cls.rule_set_id = Rule_Set_Id(Obj_Id.from_seed('code:rules'))
        cls.rule_set = Schema__Rule_Set(
            rule_set_id              = cls.rule_set_id                                  ,
            rule_set_ref             = Rule_Set_Ref('code_validation')                  ,
            ontology_id              = cls.ontology_id                                  ,
            required_node_properties = required_node_properties
        )

    @classmethod
    def build_graph(cls):                                                              # Create sample code graph
        # Node IDs
        cls.node_module_id  = Node_Id(Obj_Id.from_seed('code:node:module'))
        cls.node_class_id   = Node_Id(Obj_Id.from_seed('code:node:class'))
        cls.node_method1_id = Node_Id(Obj_Id.from_seed('code:node:method1'))
        cls.node_method2_id = Node_Id(Obj_Id.from_seed('code:node:method2'))

        # Nodes
        nodes = Dict__Nodes__By_Id()
        nodes[cls.node_module_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_module_id                                           ,
            node_type_id = cls.nt_module_id                                             ,
            name        = 'my_module.py'
        )
        nodes[cls.node_class_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_class_id                                            ,
            node_type_id = cls.nt_class_id                                              ,
            name        = 'MyClass'
        )
        nodes[cls.node_method1_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_method1_id                                          ,
            node_type_id = cls.nt_method_id                                             ,
            name        = '__init__'
        )
        nodes[cls.node_method2_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_method2_id                                          ,
            node_type_id = cls.nt_method_id                                             ,
            name        = 'process'
        )

        # Edges
        edges = List__Semantic_Graph__Edges()
        edges.append(Schema__Semantic_Graph__Edge(
            from_node_id    = cls.node_module_id                                           ,
            predicate_id = cls.pred_contains_id                                         ,
            to_node_id    = cls.node_class_id
        ))
        edges.append(Schema__Semantic_Graph__Edge(
            from_node_id    = cls.node_class_id                                            ,
            predicate_id = cls.pred_contains_id                                         ,
            to_node_id    = cls.node_method1_id
        ))
        edges.append(Schema__Semantic_Graph__Edge(
            from_node_id    = cls.node_class_id                                            ,
            predicate_id = cls.pred_contains_id                                         ,
            to_node_id    = cls.node_method2_id
        ))
        edges.append(Schema__Semantic_Graph__Edge(
            from_node_id    = cls.node_method2_id                                          ,
            predicate_id = cls.pred_calls_id                                            ,
            to_node_id    = cls.node_method1_id
        ))

        cls.graph_id = Graph_Id(Obj_Id.from_seed('code:graph'))
        cls.graph = Schema__Semantic_Graph(
            graph_id    = cls.graph_id                                                  ,
            ontology_id = cls.ontology_id                                               ,
            nodes       = nodes                                                         ,
            edges       = edges
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # Taxonomy Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__taxonomy__hierarchy(self):                                               # Test taxonomy structure
        utils = Taxonomy__Utils()

        root = utils.get_root_category(self.taxonomy)
        assert root.category_id == self.cat_root_id
        assert str(root.category_ref) == 'code_element'

        children = utils.get_children(self.taxonomy, self.cat_root_id)
        assert len(children) == 3
        assert self.cat_callable_id  in children
        assert self.cat_container_id in children
        assert self.cat_data_id      in children

    def test__taxonomy__navigation(self):                                              # Test parent/child navigation
        utils = Taxonomy__Utils()

        # Get ancestors of callable
        ancestors = utils.get_ancestors(self.taxonomy, self.cat_callable_id)
        assert len(ancestors) == 1
        assert self.cat_root_id in ancestors

        # Check relationships
        assert utils.is_ancestor_of(self.taxonomy, self.cat_root_id, self.cat_callable_id)
        assert utils.is_descendant_of(self.taxonomy, self.cat_callable_id, self.cat_root_id)

    def test__taxonomy__depth(self):                                                   # Test depth calculation
        utils = Taxonomy__Utils()

        assert utils.depth(self.taxonomy, self.cat_root_id)      == 0
        assert utils.depth(self.taxonomy, self.cat_callable_id)  == 1
        assert utils.depth(self.taxonomy, self.cat_container_id) == 1

    # ═══════════════════════════════════════════════════════════════════════════
    # Ontology Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__ontology__node_types(self):                                              # Test node type queries
        utils = Ontology__Utils()

        # Get node type
        method_type = utils.get_node_type(self.ontology, self.nt_method_id)
        assert method_type is not None
        assert str(method_type.node_type_ref) == 'method'
        assert method_type.category_id == self.cat_callable_id

        # All node type IDs
        all_ids = list(self.ontology.node_types.keys())
        assert len(all_ids) == 5

    def test__ontology__predicates(self):                                              # Test predicate queries
        utils = Ontology__Utils()

        # Get predicate
        contains = utils.get_predicate(self.ontology, self.pred_contains_id)
        assert contains is not None
        assert str(contains.predicate_ref) == 'contains'

        # Get inverse
        inverse = utils.get_inverse_predicate(self.ontology, self.pred_contains_id)
        assert inverse.predicate_id == self.pred_in_id


    def test__ontology__edge_rules(self):                                              # Test edge rule validation
        utils = Ontology__Utils()

        # Valid edges
        assert utils.is_valid_edge(self.ontology, self.nt_module_id, self.pred_contains_id, self.nt_class_id)
        assert utils.is_valid_edge(self.ontology, self.nt_class_id,  self.pred_contains_id, self.nt_method_id)
        assert utils.is_valid_edge(self.ontology, self.nt_method_id, self.pred_calls_id,    self.nt_function_id)

        # Invalid edges
        assert not utils.is_valid_edge(self.ontology, self.nt_method_id, self.pred_contains_id, self.nt_class_id)
        assert not utils.is_valid_edge(self.ontology, self.nt_variable_id, self.pred_calls_id, self.nt_method_id)

    def test__ontology__properties(self):                                              # Test property queries
        utils = Ontology__Utils()

        # Get property name
        line_number = utils.get_property_name(self.ontology, self.pn_line_number_id)
        assert line_number is not None
        assert str(line_number.property_name_ref) == 'line_number'
        assert line_number.property_type_id == self.pt_int_id

        # Get property type
        int_type = utils.get_property_type(self.ontology, self.pt_int_id)
        assert int_type is not None
        assert str(int_type.property_type_ref) == 'int'

    # ═══════════════════════════════════════════════════════════════════════════
    # Rule Set Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__rules__required_properties(self):                                        # Test required property rules
        utils = Rule_Set__Utils()

        # Method requires line_number
        assert utils.has_required_node_property_rule(self.rule_set, self.nt_method_id, self.pn_line_number_id)
        assert utils.is_node_property_required(self.rule_set, self.nt_method_id, self.pn_line_number_id)

        # Module requires file_path
        assert utils.has_required_node_property_rule(self.rule_set, self.nt_module_id, self.pn_file_path_id)

        # Class has no required properties
        props = utils.get_required_properties_for_node_type(self.rule_set, self.nt_class_id)
        assert len(props) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Graph Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__graph__structure(self):                                                  # Test graph structure
        assert len(self.graph.nodes) == 4
        assert len(self.graph.edges) == 4

        # Check nodes exist
        assert self.node_module_id  in self.graph.nodes
        assert self.node_class_id   in self.graph.nodes
        assert self.node_method1_id in self.graph.nodes
        assert self.node_method2_id in self.graph.nodes

    def test__graph__node_types(self):                                                 # Test node type assignments
        module_node = self.graph.nodes[self.node_module_id]
        assert module_node.node_type_id == self.nt_module_id
        assert module_node.name == 'my_module.py'

        method_node = self.graph.nodes[self.node_method1_id]
        assert method_node.node_type_id == self.nt_method_id
        assert method_node.name == '__init__'

    def test__graph__edges(self):                                                      # Test edge relationships
        contains_edges = [e for e in self.graph.edges if e.predicate_id == self.pred_contains_id]
        calls_edges    = [e for e in self.graph.edges if e.predicate_id == self.pred_calls_id]

        assert len(contains_edges) == 3  # module→class, class→method1, class→method2
        assert len(calls_edges)    == 1  # method2→method1

    def test__graph__find_edges_from_node(self):                                       # Test finding edges from a node
        class_edges = [e for e in self.graph.edges if e.from_node_id == self.node_class_id]
        assert len(class_edges) == 2  # class contains method1 and method2

        for edge in class_edges:
            assert edge.predicate_id == self.pred_contains_id
            assert edge.to_node_id in [self.node_method1_id, self.node_method2_id]
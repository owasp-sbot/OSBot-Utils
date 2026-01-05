# ═══════════════════════════════════════════════════════════════════════════════
# Test QA__Semantic_Graphs__Test_Data - Tests for semantic graphs test data factory
#
# Updated for Brief 3.8:
#   - Taxonomy uses IDs (parent_id, child_ids, root_id)
#   - Property system (property names, property types)
#   - Node types link to taxonomy via category_id
#   - Projections include properties and taxonomy section
#   - References filtered to only what's used
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                    import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Id              import Dict__Categories__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Edge_Properties                import Dict__Edge_Properties
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Properties                import Dict__Node_Properties
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id              import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id                   import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicates__By_Id              import Dict__Predicates__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Names__By_Id          import Dict__Property_Names__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Types__By_Id          import Dict__Property_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Ids                   import List__Category_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Edge_Rules                     import List__Edge_Rules
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Cardinality             import List__Rules__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Required_Edge_Property  import List__Rules__Required_Edge_Property
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Required_Node_Property  import List__Rules__Required_Node_Property
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Transitivity            import List__Rules__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges          import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph                    import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                          import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                         import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                          import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref                         import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                         import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id                     import Property_Name_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Ref                    import Property_Name_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Id                     import Property_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Ref                    import Property_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                          import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                          import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref                         import Taxonomy_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                       import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type            import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Property_Name        import Schema__Ontology__Property_Name
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Property_Type        import Schema__Ontology__Property_Type
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__References         import Schema__Projected__References
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Semantic_Graph     import Schema__Projected__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Taxonomy           import Schema__Projected__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                           import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Edge_Property       import Schema__Rule__Required_Edge_Property
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Node_Property       import Schema__Rule__Required_Node_Property
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy                       import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category             import Schema__Taxonomy__Category
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data                  import QA__Semantic_Graphs__Test_Data
from osbot_utils.testing.__                                                                      import __, __SKIP__
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                     import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                               import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed            import Safe_Str__Id__Seed


class test_QA__Semantic_Graphs__Test_Data(TestCase):                                             # Test QA test data factory

    @classmethod
    def setUpClass(cls):                                                                         # Shared test_data instance
        cls.test_data = QA__Semantic_Graphs__Test_Data()

    def test__init__(self):                                                                      # Test basic initialization
        with QA__Semantic_Graphs__Test_Data() as _:
            assert type(_) is QA__Semantic_Graphs__Test_Data

    # ═══════════════════════════════════════════════════════════════════════════
    # Taxonomy Tests (ID-based per Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_taxonomy(self):                                                             # Test taxonomy creation
        with self.test_data as _:
            taxonomy = _.create_taxonomy()

            assert type(taxonomy)             is Schema__Taxonomy
            assert type(taxonomy.taxonomy_id) is Taxonomy_Id
            assert str(taxonomy.taxonomy_ref) == 'code_analysis'
            assert taxonomy.version           == '1.0.0'
            assert type(taxonomy.root_id)     is Category_Id                                     # Uses root_id not root_category
            assert type(taxonomy.categories)  is Dict__Categories__By_Id                         # By ID not By Ref
            assert len(taxonomy.categories)   == 4

    def test__create_taxonomy__categories_are_id_based(self):                                    # Test categories use IDs
        with self.test_data as _:
            taxonomy = _.create_taxonomy()
            root_id  = taxonomy.root_id
            root     = taxonomy.categories[root_id]

            assert type(root)             is Schema__Taxonomy__Category
            assert type(root.category_id) is Category_Id
            assert type(root.parent_id)   is type(None)                                          # Root has no parent
            assert type(root.child_ids)   is List__Category_Ids                                  # Uses child_ids not child_refs
            assert len(root.child_ids)    == 3                                                   # callable, container, data

    def test__create_taxonomy__no_description_field(self):                                       # Brief 3.8: description removed
        with self.test_data as _:
            taxonomy = _.create_taxonomy()
            root     = taxonomy.categories[taxonomy.root_id]

            assert not hasattr(root, 'description')                                              # No description field
            assert not hasattr(root, 'name')                                                     # No name field (derivable from ref)

    def test__create_taxonomy__hierarchy_navigation(self):                                       # Test ID-based hierarchy
        with self.test_data as _:
            taxonomy    = _.create_taxonomy()
            root        = taxonomy.categories[taxonomy.root_id]
            callable_id = _.get_category_id__callable()
            callable    = taxonomy.categories[callable_id]

            assert callable.parent_id       == taxonomy.root_id                                  # Parent is root
            assert callable_id              in root.child_ids                                    # Root has callable as child
            assert str(callable.category_ref) == 'callable'

    def test__create_taxonomy__deterministic_ids(self):                                          # Test reproducible IDs
        with self.test_data as _:
            taxonomy_1 = _.create_taxonomy()
            taxonomy_2 = _.create_taxonomy()

            assert taxonomy_1.taxonomy_id == taxonomy_2.taxonomy_id                              # Same seed → same ID
            assert taxonomy_1.root_id     == taxonomy_2.root_id

    def test__create_taxonomy_registry(self):                                                    # Test registry creation
        with self.test_data as _:
            registry = _.create_taxonomy_registry()
            taxonomy = registry.get_by_ref(Taxonomy_Ref('code_analysis'))

            assert taxonomy                   is not None
            assert type(taxonomy.taxonomy_id) is Taxonomy_Id

            taxonomy_by_id = registry.get_by_id(taxonomy.taxonomy_id)                            # ID-based lookup works
            assert taxonomy_by_id == taxonomy

    # ═══════════════════════════════════════════════════════════════════════════
    # Property Type Tests (new in Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_property_types(self):                                                       # Test property type creation
        with self.test_data as _:
            property_types = _.create_property_types()

            assert type(property_types) is Dict__Property_Types__By_Id
            assert len(property_types)  == 3                                                     # integer, boolean, string

    def test__create_property_types__structure(self):                                            # Test property type structure
        with self.test_data as _:
            property_types = _.create_property_types()
            integer_id     = _.get_property_type_id__integer()
            integer_type   = property_types[integer_id]

            assert type(integer_type)                   is Schema__Ontology__Property_Type
            assert type(integer_type.property_type_id)  is Property_Type_Id
            assert type(integer_type.property_type_ref) is Property_Type_Ref
            assert str(integer_type.property_type_ref)  == 'integer'

    def test__create_property_types__all_refs(self):                                             # Test all property type refs
        with self.test_data as _:
            property_types = _.create_property_types()
            refs           = [str(pt.property_type_ref) for pt in property_types.values()]

            assert 'integer' in refs
            assert 'boolean' in refs
            assert 'string'  in refs

    # ═══════════════════════════════════════════════════════════════════════════
    # Property Name Tests (new in Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_property_names(self):                                                       # Test property name creation
        with self.test_data as _:
            property_types = _.create_property_types()
            property_names = _.create_property_names(property_types)

            assert type(property_names) is Dict__Property_Names__By_Id
            assert len(property_names)  == 4                                                     # line_number, is_async, docstring, call_count

    def test__create_property_names__structure(self):                                            # Test property name structure
        with self.test_data as _:
            property_types  = _.create_property_types()
            property_names  = _.create_property_names(property_types)
            line_number_id  = _.get_property_name_id__line_number()
            line_number     = property_names[line_number_id]

            assert type(line_number)                    is Schema__Ontology__Property_Name
            assert type(line_number.property_name_id)   is Property_Name_Id
            assert type(line_number.property_name_ref)  is Property_Name_Ref
            assert str(line_number.property_name_ref)   == 'line_number'
            assert type(line_number.property_type_id)   is Property_Type_Id                      # FK to integer type

    def test__create_property_names__type_links(self):                                           # Test property → type links
        with self.test_data as _:
            property_types = _.create_property_types()
            property_names = _.create_property_names(property_types)
            integer_id     = _.get_property_type_id__integer()

            line_number_id = _.get_property_name_id__line_number()
            line_number    = property_names[line_number_id]

            assert line_number.property_type_id == integer_id                                    # line_number is integer

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Type Tests (with category_id per Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_node_types(self):                                                           # Test node type creation
        with self.test_data as _:
            node_types = _.create_node_types()

            assert type(node_types) is Dict__Node_Types__By_Id
            assert len(node_types)  == 5                                                         # class, method, function, module, variable

    def test__create_node_types__category_id_link(self):                                         # Test node type → category link
        with self.test_data as _:
            node_types   = _.create_node_types()
            method_id    = _.get_node_type_id__method()
            method       = node_types[method_id]
            callable_id  = _.get_category_id__callable()

            assert type(method)             is Schema__Ontology__Node_Type
            assert type(method.category_id) is Category_Id                                       # Has category_id field
            assert method.category_id       == callable_id                                       # method is in callable category

    def test__create_node_types__all_have_categories(self):                                      # Test all node types have categories
        with self.test_data as _:
            node_types = _.create_node_types()

            for nt in node_types.values():
                assert nt.category_id is not None                                                # All have category links

    # ═══════════════════════════════════════════════════════════════════════════
    # Ontology Tests (with properties per Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_ontology(self):                                                             # Test ontology creation
        with self.test_data as _:
            ontology = _.create_ontology()

            assert type(ontology)                is Schema__Ontology
            assert type(ontology.ontology_id)    is Ontology_Id
            assert type(ontology.taxonomy_id)    is Taxonomy_Id
            assert type(ontology.node_types)     is Dict__Node_Types__By_Id
            assert type(ontology.predicates)     is Dict__Predicates__By_Id
            assert type(ontology.property_names) is Dict__Property_Names__By_Id                  # New in 3.8
            assert type(ontology.property_types) is Dict__Property_Types__By_Id                  # New in 3.8
            assert type(ontology.edge_rules)     is List__Edge_Rules

    def test__create_ontology__has_properties(self):                                             # Test ontology includes properties
        with self.test_data as _:
            ontology = _.create_ontology()

            assert len(ontology.property_types) == 3                                             # integer, boolean, string
            assert len(ontology.property_names) == 4                                             # line_number, is_async, docstring, call_count

    def test__create_ontology__predicates_have_inverses(self):                                   # Test predicate inverse links
        with self.test_data as _:
            ontology    = _.create_ontology()
            contains_id = _.get_predicate_id__contains()

            contains = ontology.predicates[contains_id]
            assert contains.inverse_id is not None

            inverse = ontology.predicates[contains.inverse_id]
            assert inverse.inverse_id == contains_id                                             # Bidirectional link

    def test__create_ontology_registry(self):                                                    # Test registry creation
        with self.test_data as _:
            registry = _.create_ontology_registry()
            ontology = registry.get_by_ref(Ontology_Ref('code_analysis'))

            assert ontology is not None

            ontology_by_id = registry.get_by_id(ontology.ontology_id)                            # ID-based lookup works
            assert ontology_by_id == ontology

    # ═══════════════════════════════════════════════════════════════════════════
    # Rule Set Tests (with property rules per Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_rule_set(self):                                                             # Test rule set creation
        with self.test_data as _:
            rule_set = _.create_rule_set()

            assert type(rule_set)                        is Schema__Rule_Set
            assert type(rule_set.rule_set_id)            is Rule_Set_Id
            assert type(rule_set.transitivity_rules)     is List__Rules__Transitivity
            assert type(rule_set.cardinality_rules)      is List__Rules__Cardinality
            assert type(rule_set.required_node_properties) is List__Rules__Required_Node_Property  # New in 3.8
            assert type(rule_set.required_edge_properties) is List__Rules__Required_Edge_Property  # New in 3.8

    def test__create_rule_set__required_node_properties(self):                                   # Test required node property rules
        with self.test_data as _:
            rule_set       = _.create_rule_set()
            method_id      = _.get_node_type_id__method()
            line_number_id = _.get_property_name_id__line_number()

            assert len(rule_set.required_node_properties) >= 1

            method_rules = [r for r in rule_set.required_node_properties
                           if r.node_type_id == method_id]
            assert len(method_rules) >= 1                                                        # Method requires line_number

            rule = method_rules[0]
            assert type(rule)              is Schema__Rule__Required_Node_Property
            assert rule.property_name_id   == line_number_id

    def test__create_rule_set__required_edge_properties(self):                                   # Test required edge property rules
        with self.test_data as _:
            rule_set      = _.create_rule_set()
            calls_id      = _.get_predicate_id__calls()
            call_count_id = _.get_property_name_id__call_count()

            assert len(rule_set.required_edge_properties) >= 1

            calls_rules = [r for r in rule_set.required_edge_properties
                          if r.predicate_id == calls_id]
            assert len(calls_rules) >= 1                                                         # Calls requires call_count

            rule = calls_rules[0]
            assert type(rule)              is Schema__Rule__Required_Edge_Property
            assert rule.property_name_id   == call_count_id

    # ═══════════════════════════════════════════════════════════════════════════
    # Graph Tests (with properties per Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_graph__empty(self):                                                 # Test empty graph creation
        with self.test_data as _:
            graph = _.create_graph__empty()

            assert type(graph)              is Schema__Semantic_Graph
            assert type(graph.graph_id)     is Graph_Id
            assert type(graph.nodes)        is Dict__Nodes__By_Id
            assert type(graph.edges)        is List__Semantic_Graph__Edges
            assert len(graph.nodes)         == 0
            assert len(graph.edges)         == 0
            assert str(graph.ontology_id)   == '046d8716'

    def test__create_graph__empty__deterministic_id(self):                               # Test empty graph has deterministic ID
        with self.test_data as _:
            graph_1 = _.create_graph__empty()
            graph_2 = _.create_graph__empty()

            assert graph_1.graph_id == graph_2.graph_id                                  # Same default seed → same ID

    def test__create_graph__empty__custom_seed(self):                                    # Test empty graph with custom seed
        with self.test_data as _:
            seed    = Safe_Str__Id__Seed('custom-empty-graph')
            graph   = _.create_graph__empty(seed=seed)

            assert graph.graph_id_source is not None
            assert str(graph.graph_id_source.seed) == 'custom-empty-graph'

    def test__create_graph_with_properties(self):                                                # Test graph with property data
        with self.test_data as _:
            builder = _.create_graph_with_properties()
            graph   = builder.build()

            assert type(graph)              is Schema__Semantic_Graph
            assert type(graph.graph_id)     is Graph_Id
            assert type(graph.ontology_id)  is Ontology_Id
            assert type(graph.nodes)        is Dict__Nodes__By_Id
            assert type(graph.edges)        is List__Semantic_Graph__Edges
            assert len(graph.nodes)         == 4                                                 # module, class, method, function
            assert len(graph.edges)         == 4                                                 # contains x3, calls x1

    def test__create_graph_with_properties__nodes_have_properties(self):                         # Test nodes have properties
        with self.test_data as _:
            builder        = _.create_graph_with_properties()
            graph          = builder.build()
            line_number_id = _.get_property_name_id__line_number()

            nodes_with_props = [n for n in graph.nodes.values() if n.properties is not None]
            assert len(nodes_with_props) >= 1                                                    # At least one node has properties

            has_line_number = False
            for node in graph.nodes.values():
                if node.properties and line_number_id in node.properties:
                    has_line_number = True
                    assert type(node.properties)                 is Dict__Node_Properties
                    assert type(node.properties[line_number_id]) is Safe_Str__Text
                    break

            assert has_line_number                                                               # At least one has line_number

    def test__create_graph_with_properties__edges_have_properties(self):                         # Test edges have properties
        with self.test_data as _:
            builder       = _.create_graph_with_properties()
            graph         = builder.build()
            call_count_id = _.get_property_name_id__call_count()

            edges_with_props = [e for e in graph.edges if e.properties is not None]
            assert len(edges_with_props) >= 1                                                    # At least one edge has properties

            has_call_count = False
            for edge in graph.edges:
                if edge.properties and call_count_id in edge.properties:
                    has_call_count = True
                    assert type(edge.properties)                is Dict__Edge_Properties
                    assert type(edge.properties[call_count_id]) is Safe_Str__Text
                    break

            assert has_call_count                                                                # At least one has call_count

    # ═══════════════════════════════════════════════════════════════════════════
    # Complete Fixture Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_complete_fixture(self):                                                     # Test complete fixture
        with self.test_data as _:
            fixture = _.create_complete_fixture()

            assert 'taxonomy_registry' in fixture
            assert 'ontology_registry' in fixture
            assert 'ontology'          in fixture
            assert 'taxonomy'          in fixture
            assert 'rule_set'          in fixture
            assert 'graph'             in fixture
            assert 'projection'        in fixture
            assert 'projector'         in fixture

    def test__create_complete_fixture__projection_has_properties(self):                          # Test projection includes properties
        with self.test_data as _:
            fixture    = _.create_complete_fixture()
            projection = fixture['projection']

            assert type(projection) is Schema__Projected__Semantic_Graph

            nodes_with_props = [n for n in projection.projection.nodes
                               if n.properties is not None]
            assert len(nodes_with_props) >= 1                                                    # Properties projected

    def test__create_complete_fixture__projection_has_taxonomy(self):                            # Test projection includes taxonomy
        with self.test_data as _:
            fixture    = _.create_complete_fixture()
            projection = fixture['projection']

            assert type(projection.taxonomy) is Schema__Projected__Taxonomy
            assert projection.taxonomy.node_type_categories is not None                          # Node type → category mapping
            assert projection.taxonomy.category_parents     is not None                          # Category hierarchy

    def test__create_complete_fixture__references_filtered(self):                                # Test references are filtered
        with self.test_data as _:
            fixture    = _.create_complete_fixture()
            projection = fixture['projection']
            ontology   = fixture['ontology']

            assert type(projection.references) is Schema__Projected__References

            used_node_types = len(projection.references.node_types)
            all_node_types  = len(ontology.node_types)
            assert used_node_types <= all_node_types                                             # Filtered to what's used

    def test__create_complete_fixture__projection_properties_use_refs(self):                     # Test projection uses refs not IDs
        with self.test_data as _:
            fixture    = _.create_complete_fixture()
            projection = fixture['projection']

            for node in projection.projection.nodes:
                if node.properties:
                    for key in node.properties.keys():
                        assert type(key) is Property_Name_Ref                                    # Uses refs not IDs

    # ═══════════════════════════════════════════════════════════════════════════
    # Accessor Method Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_category_id__callable(self):                                                   # Test callable category ID accessor
        with self.test_data as _:
            callable_id = _.get_category_id__callable()

            assert type(callable_id) is Category_Id

            taxonomy = _.create_taxonomy()
            assert callable_id in taxonomy.categories                                            # ID exists in taxonomy

    def test__get_node_type_id__method(self):                                                    # Test method node type ID accessor
        with self.test_data as _:
            method_id = _.get_node_type_id__method()

            assert type(method_id) is Node_Type_Id

            ontology = _.create_ontology()
            assert method_id in ontology.node_types                                              # ID exists in ontology

    def test__get_predicate_id__calls(self):                                                     # Test calls predicate ID accessor
        with self.test_data as _:
            calls_id = _.get_predicate_id__calls()

            assert type(calls_id) is Predicate_Id

            ontology = _.create_ontology()
            assert calls_id in ontology.predicates                                               # ID exists in ontology

    def test__get_property_name_id__line_number(self):                                           # Test line_number property ID accessor
        with self.test_data as _:
            line_number_id = _.get_property_name_id__line_number()

            assert type(line_number_id) is Property_Name_Id

            ontology = _.create_ontology()
            assert line_number_id in ontology.property_names                                     # ID exists in ontology

    def test__get_property_type_id__integer(self):                                               # Test integer property type ID accessor
        with self.test_data as _:
            integer_id = _.get_property_type_id__integer()

            assert type(integer_id) is Property_Type_Id

            ontology = _.create_ontology()
            assert integer_id in ontology.property_types                                         # ID exists in ontology

    # ═══════════════════════════════════════════════════════════════════════════
    # Deterministic ID Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__deterministic_ids__taxonomy(self):                                                 # Test taxonomy IDs are reproducible
        with self.test_data as _:
            taxonomy_1 = _.create_taxonomy()
            taxonomy_2 = _.create_taxonomy()

            assert taxonomy_1.taxonomy_id == taxonomy_2.taxonomy_id
            assert taxonomy_1.root_id     == taxonomy_2.root_id

            for cat_id in taxonomy_1.categories.keys():
                assert cat_id in taxonomy_2.categories

    def test__deterministic_ids__ontology(self):                                                 # Test ontology IDs are reproducible
        with self.test_data as _:
            ontology_1 = _.create_ontology()
            ontology_2 = _.create_ontology()

            assert ontology_1.ontology_id == ontology_2.ontology_id

            for nt_id in ontology_1.node_types.keys():
                assert nt_id in ontology_2.node_types

            for pn_id in ontology_1.property_names.keys():
                assert pn_id in ontology_2.property_names

    def test__deterministic_ids__graph(self):                                                    # Test graph IDs are reproducible
        with self.test_data as _:
            graph_1 = _.create_graph_with_properties().build()
            graph_2 = _.create_graph_with_properties().build()

            assert graph_1.graph_id == graph_2.graph_id

            for node_id in graph_1.nodes.keys():
                assert node_id in graph_2.nodes

    # ═══════════════════════════════════════════════════════════════════════════
    # Helper Method Tests (create_node, create_edge, create_graph__empty)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_node(self):                                                         # Test node creation helper
        with self.test_data as _:
            class_type_id = _.get_node_type_id__class()
            node          = _.create_node(node_type_id = class_type_id          ,
                                          name         = Safe_Str__Id('MyClass'))

            assert type(node)              is Schema__Semantic_Graph__Node
            assert type(node.node_id)      is Node_Id
            assert node.node_type_id       == class_type_id
            assert str(node.name)          == 'MyClass'
            assert node.node_id_source     is None                                       # Random ID has no source

    def test__create_node__with_seed(self):                                              # Test node with deterministic ID
        with self.test_data as _:
            class_type_id = _.get_node_type_id__class()
            seed          = Safe_Str__Id__Seed('test:node:MyClass')
            node          = _.create_node(node_type_id = class_type_id          ,
                                          name         = Safe_Str__Id('MyClass'),
                                          seed         = seed                   )

            assert node.node_id_source is not None
            assert str(node.node_id_source.seed) == 'test:node:MyClass'

            node_2 = _.create_node(node_type_id = class_type_id          ,                # Same seed → same ID
                                   name         = Safe_Str__Id('MyClass'),
                                   seed         = seed                   )
            assert node.node_id == node_2.node_id

    def test__create_node__with_properties(self):                                        # Test node with properties
        with self.test_data as _:
            class_type_id  = _.get_node_type_id__class()
            line_number_id = _.get_property_name_id__line_number()

            properties = Dict__Node_Properties()
            properties[line_number_id] = Safe_Str__Text('42')

            node = _.create_node(node_type_id = class_type_id          ,
                                 name         = Safe_Str__Id('MyClass'),
                                 properties   = properties             )

            assert node.properties is not None
            assert line_number_id in node.properties
            assert str(node.properties[line_number_id]) == '42'

    def test__create_edge(self):                                                         # Test edge creation helper
        with self.test_data as _:
            class_type_id  = _.get_node_type_id__class()
            method_type_id = _.get_node_type_id__method()
            contains_id    = _.get_predicate_id__contains()

            node_1 = _.create_node(class_type_id , Safe_Str__Id('MyClass'))
            node_2 = _.create_node(method_type_id, Safe_Str__Id('my_method'))

            edge = _.create_edge(from_node_id = node_1.node_id,
                                 predicate_id = contains_id   ,
                                 to_node_id   = node_2.node_id)

            assert type(edge)          is Schema__Semantic_Graph__Edge
            assert type(edge.edge_id)  is Edge_Id
            assert edge.from_node_id   == node_1.node_id
            assert edge.predicate_id   == contains_id
            assert edge.to_node_id     == node_2.node_id
            assert edge.edge_id_source is None                                           # Random ID has no source

    def test__create_edge__with_seed(self):                                              # Test edge with deterministic ID
        with self.test_data as _:
            contains_id = _.get_predicate_id__contains()
            node_1      = _.create_node(_.get_node_type_id__class() , Safe_Str__Id('A'))
            node_2      = _.create_node(_.get_node_type_id__method(), Safe_Str__Id('b'))
            seed        = Safe_Str__Id__Seed('test:edge:A_contains_b')

            edge = _.create_edge(from_node_id = node_1.node_id,
                                 predicate_id = contains_id   ,
                                 to_node_id   = node_2.node_id,
                                 seed         = seed          )

            assert edge.edge_id_source is not None
            assert str(edge.edge_id_source.seed) == 'test:edge:A_contains_b'

            edge_2 = _.create_edge(from_node_id = node_1.node_id,                         # Same seed → same ID
                                   predicate_id = contains_id   ,
                                   to_node_id   = node_2.node_id,
                                   seed         = seed          )
            assert edge.edge_id == edge_2.edge_id

    def test__create_edge__with_properties(self):                                        # Test edge with properties
        with self.test_data as _:
            calls_id      = _.get_predicate_id__calls()
            call_count_id = _.get_property_name_id__call_count()

            node_1 = _.create_node(_.get_node_type_id__method(), Safe_Str__Id('foo'))
            node_2 = _.create_node(_.get_node_type_id__method(), Safe_Str__Id('bar'))

            properties = Dict__Edge_Properties()
            properties[call_count_id] = Safe_Str__Text('5')

            edge = _.create_edge(from_node_id = node_1.node_id,
                                 predicate_id = calls_id      ,
                                 to_node_id   = node_2.node_id,
                                 properties   = properties    )

            assert edge.properties is not None
            assert call_count_id in edge.properties
            assert str(edge.properties[call_count_id]) == '5'

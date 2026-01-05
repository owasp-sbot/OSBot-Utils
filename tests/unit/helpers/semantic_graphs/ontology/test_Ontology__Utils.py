# ═══════════════════════════════════════════════════════════════════════════════
# Test Ontology__Utils - Tests for ontology utility operations
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
#
# Updated for Brief 3.8:
#   - Uses node_type_id instead of node_type ref keys
#   - Uses predicates dict instead of embedded relationships
#   - Uses edge_rules list instead of relationship targets
#   - Ontology includes property_names and property_types
#   - Node types have category_id
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                               import TestCase
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Utils                           import Ontology__Utils
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id         import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicates__By_Id         import Dict__Predicates__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Names__By_Id     import Dict__Property_Names__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Types__By_Id     import Dict__Property_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Edge_Rules                import List__Edge_Rules
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Node_Type_Ids             import List__Node_Type_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Predicate_Ids             import List__Predicate_Ids
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                     import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                    import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                   import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                    import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref                   import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id                import Property_Name_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Ref               import Property_Name_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Id                import Property_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                  import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data             import QA__Semantic_Graphs__Test_Data
from osbot_utils.testing.__                                                                 import __
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id


class test_Ontology__Utils(TestCase):                                                       # Test ontology utilities

    @classmethod
    def setUpClass(cls):                                                                    # Shared test objects (performance)
        cls.test_data = QA__Semantic_Graphs__Test_Data()
        cls.utils     = Ontology__Utils()
        cls.ontology  = cls.test_data.create_ontology()                                     # Brief 3.8 API

        # Cache IDs using Brief 3.8 accessors
        cls.class_id    = cls.test_data.get_node_type_id__class()
        cls.method_id   = cls.test_data.get_node_type_id__method()
        cls.function_id = cls.test_data.get_node_type_id__function()

        cls.contains_id      = cls.test_data.get_predicate_id__contains()
        cls.contained_in_id  = cls.test_data.get_predicate_id__contained_by()
        cls.calls_id         = cls.test_data.get_predicate_id__calls()
        cls.called_by_id     = cls.test_data.get_predicate_id__called_by()

        # Property IDs
        cls.line_number_id = cls.test_data.get_property_name_id__line_number()
        cls.integer_type_id = cls.test_data.get_property_type_id__integer()

    def test__init__(self):                                                                 # Test initialization
        with Ontology__Utils() as _:
            assert type(_) is Ontology__Utils

    # ═══════════════════════════════════════════════════════════════════════════
    # Ontology Structure Tests (Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__ontology__has_expected_structure(self):                                       # Verify Brief 3.8 ontology
        with self.ontology as _:
            assert type(_)                is Schema__Ontology
            assert type(_.node_types)     is Dict__Node_Types__By_Id
            assert type(_.predicates)     is Dict__Predicates__By_Id
            assert type(_.property_names) is Dict__Property_Names__By_Id                    # Brief 3.8
            assert type(_.property_types) is Dict__Property_Types__By_Id                    # Brief 3.8
            assert type(_.edge_rules)     is List__Edge_Rules

            assert len(_.node_types)     == 5                                               # class, method, function, module, variable
            assert len(_.predicates)     == 6                                               # contains/contained_by, calls/called_by, uses/used_by
            assert len(_.property_names) == 4                                               # line_number, is_async, docstring, call_count
            assert len(_.property_types) == 3                                               # integer, boolean, string

    def test__ontology__node_types_have_category_id(self):                                  # Brief 3.8: taxonomy link
        for nt in self.ontology.node_types.values():
            assert type(nt.category_id) is Category_Id                                      # All have category links

    # ═══════════════════════════════════════════════════════════════════════════
    # Valid Edge Detection (ID-based)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__valid_edge__returns_true_for_valid(self):                                     # Test valid edge detection
        assert self.utils.is_valid_edge(self.ontology, self.class_id,  self.contains_id, self.method_id)   is True
        assert self.utils.is_valid_edge(self.ontology, self.method_id, self.calls_id,    self.function_id) is True

    def test__valid_edge__returns_false_for_invalid(self):                                  # Test invalid edge detection
        unknown_type = Node_Type_Id(Obj_Id())
        assert self.utils.is_valid_edge(self.ontology, unknown_type, self.contains_id, self.class_id) is False

        unknown_pred = Predicate_Id(Obj_Id())
        assert self.utils.is_valid_edge(self.ontology, self.class_id, unknown_pred, self.method_id) is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Valid Edge Detection (Ref-based convenience)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__valid_edge_by_ref__returns_true_for_valid(self):                              # Test valid edge by ref
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('class'),  Predicate_Ref('contains'), Node_Type_Ref('method'))   is True
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('method'), Predicate_Ref('calls'),    Node_Type_Ref('function')) is True

    def test__valid_edge_by_ref__returns_false_for_invalid(self):                           # Test invalid edge by ref
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('invalid'), Predicate_Ref('contains'), Node_Type_Ref('method')) is False
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('class'),   Predicate_Ref('invalid'),  Node_Type_Ref('method')) is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Valid Targets Query
    # ═══════════════════════════════════════════════════════════════════════════

    def test__valid_targets_for(self):                                                      # Test valid target lookup
        targets = self.utils.valid_targets_for(self.ontology, self.class_id, self.contains_id)

        assert type(targets) is List__Node_Type_Ids
        assert self.method_id in targets                                                    # class contains method

    def test__valid_targets_for__no_targets(self):                                          # Test no valid targets
        unknown_pred = Predicate_Id(Obj_Id())
        targets = self.utils.valid_targets_for(self.ontology, self.class_id, unknown_pred)

        assert len(targets) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Valid Predicates Query
    # ═══════════════════════════════════════════════════════════════════════════

    def test__valid_predicates_for(self):                                                   # Test valid predicate lookup
        predicates = self.utils.valid_predicates_for(self.ontology, self.method_id)

        assert type(predicates) is List__Predicate_Ids
        assert self.calls_id in predicates                                                  # method calls

    def test__valid_predicates_for__no_predicates(self):                                    # Test no valid predicates
        unknown_type = Node_Type_Id(Obj_Id())
        predicates = self.utils.valid_predicates_for(self.ontology, unknown_type)

        assert len(predicates) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Inverse Predicate Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_inverse_predicate(self):                                                  # Test inverse predicate lookup
        contains_inverse = self.utils.get_inverse_predicate(self.ontology, self.contains_id)
        assert contains_inverse is not None
        assert contains_inverse.predicate_id == self.contained_in_id

        calls_inverse = self.utils.get_inverse_predicate(self.ontology, self.calls_id)
        assert calls_inverse is not None
        assert calls_inverse.predicate_id == self.called_by_id

    def test__get_inverse_predicate__returns_none_for_invalid(self):                        # Test invalid lookups
        unknown_pred = Predicate_Id(Obj_Id())
        assert self.utils.get_inverse_predicate(self.ontology, unknown_pred) is None

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Type Queries
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_node_type(self):                                                          # Test node type lookup by ID
        node_type = self.utils.get_node_type(self.ontology, self.class_id)

        assert node_type is not None
        assert node_type.node_type_ref == Node_Type_Ref('class')

    def test__get_node_type_by_ref(self):                                                   # Test node type lookup by ref
        node_type = self.utils.get_node_type_by_ref(self.ontology, Node_Type_Ref('method'))

        assert node_type is not None
        assert node_type.node_type_id == self.method_id

    def test__has_node_type(self):                                                          # Test node type existence by ID
        assert self.utils.has_node_type(self.ontology, self.class_id) is True
        assert self.utils.has_node_type(self.ontology, Node_Type_Id(Obj_Id())) is False

    def test__has_node_type_ref(self):                                                      # Test node type existence by ref
        assert self.utils.has_node_type_ref(self.ontology, Node_Type_Ref('class')) is True
        assert self.utils.has_node_type_ref(self.ontology, Node_Type_Ref('unknown')) is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Predicate Queries
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_predicate(self):                                                          # Test predicate lookup by ID
        predicate = self.utils.get_predicate(self.ontology, self.contains_id)

        assert predicate is not None
        assert predicate.predicate_ref == Predicate_Ref('contains')

    def test__get_predicate_by_ref(self):                                                   # Test predicate lookup by ref
        predicate = self.utils.get_predicate_by_ref(self.ontology, Predicate_Ref('calls'))

        assert predicate is not None
        assert predicate.predicate_id == self.calls_id

    def test__has_predicate(self):                                                          # Test predicate existence by ID
        assert self.utils.has_predicate(self.ontology, self.calls_id) is True
        assert self.utils.has_predicate(self.ontology, Predicate_Id(Obj_Id())) is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Property Name Queries (Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_property_name(self):                                                      # Test property name lookup by ID
        prop_name = self.utils.get_property_name(self.ontology, self.line_number_id)

        assert prop_name is not None
        assert prop_name.property_name_ref == Property_Name_Ref('line_number')

    def test__get_property_name_by_ref(self):                                               # Test property name lookup by ref
        prop_name = self.utils.get_property_name_by_ref(self.ontology, Property_Name_Ref('line_number'))

        assert prop_name is not None
        assert prop_name.property_name_id == self.line_number_id

    def test__has_property_name(self):                                                      # Test property name existence
        assert self.utils.has_property_name(self.ontology, self.line_number_id) is True
        assert self.utils.has_property_name(self.ontology, Property_Name_Id(Obj_Id())) is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Property Type Queries (Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_property_type(self):                                                      # Test property type lookup by ID
        prop_type = self.utils.get_property_type(self.ontology, self.integer_type_id)

        assert prop_type is not None
        assert str(prop_type.property_type_ref) == 'integer'

    def test__has_property_type(self):                                                      # Test property type existence
        assert self.utils.has_property_type(self.ontology, self.integer_type_id) is True
        assert self.utils.has_property_type(self.ontology, Property_Type_Id(Obj_Id())) is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Property Name → Type Link (Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__property_name_links_to_type(self):                                            # Test property_name has type_id
        prop_name = self.utils.get_property_name(self.ontology, self.line_number_id)

        assert prop_name.property_type_id is not None
        assert prop_name.property_type_id == self.integer_type_id                           # line_number is integer

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration with QA Test Data
    # ═══════════════════════════════════════════════════════════════════════════

    def test__qa_ontology__valid_edges(self):                                               # Test QA ontology edges
        ontology = self.test_data.create_ontology()

        assert self.utils.is_valid_edge_by_ref(ontology, Node_Type_Ref('class'),  Predicate_Ref('contains'), Node_Type_Ref('method'))   is True
        assert self.utils.is_valid_edge_by_ref(ontology, Node_Type_Ref('method'), Predicate_Ref('calls'),    Node_Type_Ref('function')) is True

    def test__qa_ontology__inverse_predicates(self):                                        # Test QA ontology inverse predicates
        ontology = self.test_data.create_ontology()

        contains_pred = self.utils.get_predicate_by_ref(ontology, Predicate_Ref('contains'))
        inverse_pred  = self.utils.get_inverse_predicate(ontology, contains_pred.predicate_id)
        assert inverse_pred is not None

        calls_pred   = self.utils.get_predicate_by_ref(ontology, Predicate_Ref('calls'))
        inverse_pred = self.utils.get_inverse_predicate(ontology, calls_pred.predicate_id)
        assert inverse_pred is not None
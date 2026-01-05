# ═══════════════════════════════════════════════════════════════════════════════
# Test Rule_Set__Utils - Tests for rule set utility operations
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
#
# Updated for Brief 3.8:
#   - ontology_ref → ontology_id
#   - Rule sets use required_node_properties and required_edge_properties
#   - Property validation rules with node_type_id and property_name_id
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                   import TestCase
from osbot_utils.helpers.semantic_graphs.rule.Rule_Set__Utils                                   import Rule_Set__Utils
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                        import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                       import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                         import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                        import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id                    import Property_Name_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                         import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref                        import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                          import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Node_Property      import Schema__Rule__Required_Node_Property
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Edge_Property      import Schema__Rule__Required_Edge_Property
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data                 import QA__Semantic_Graphs__Test_Data
from osbot_utils.testing.__                                                                     import __, __SKIP__
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                import Obj_Id


class test_Rule_Set__Utils(TestCase):                                                           # Test rule set utilities

    @classmethod
    def setUpClass(cls):                                                                        # Shared test objects (performance)
        cls.test_data = QA__Semantic_Graphs__Test_Data()
        cls.utils     = Rule_Set__Utils()
        cls.rule_set  = cls.create_test_rule_set()                                              # Rich rule set for testing

        # Cache IDs for tests
        cls.class_id       = cls.test_data.get_node_type_id__class()
        cls.method_id      = cls.test_data.get_node_type_id__method()
        cls.function_id    = cls.test_data.get_node_type_id__function()
        cls.calls_id       = cls.test_data.get_predicate_id__calls()
        cls.line_number_id = cls.test_data.get_property_name_id__line_number()
        cls.call_count_id  = cls.test_data.get_property_name_id__call_count()

    @classmethod
    def create_test_rule_set(cls) -> Schema__Rule_Set:                                          # Build test rule set
        test_data = QA__Semantic_Graphs__Test_Data()

        method_id      = test_data.get_node_type_id__method()
        function_id    = test_data.get_node_type_id__function()
        calls_id       = test_data.get_predicate_id__calls()
        line_number_id = test_data.get_property_name_id__line_number()
        call_count_id  = test_data.get_property_name_id__call_count()

        # Brief 3.8: required_node_properties (node_type_id → property_name_id)
        node_prop_method = Schema__Rule__Required_Node_Property(node_type_id     = method_id     ,
                                                                property_name_id = line_number_id,
                                                                required         = True          )

        node_prop_function = Schema__Rule__Required_Node_Property(node_type_id     = function_id   ,
                                                                  property_name_id = line_number_id,
                                                                  required         = True          )

        # Brief 3.8: required_edge_properties (predicate_id → property_name_id)
        # This one is optional (required=False) to test both cases
        edge_prop_calls = Schema__Rule__Required_Edge_Property(predicate_id     = calls_id     ,
                                                               property_name_id = call_count_id,
                                                               required         = False        )

        return Schema__Rule_Set(rule_set_id              = Rule_Set_Id(Obj_Id())               ,
                                rule_set_ref             = Rule_Set_Ref('python_rules')        ,
                                ontology_id              = Ontology_Id(Obj_Id())               ,
                                version                  = '1.0.0'                             ,
                                required_node_properties = [node_prop_method, node_prop_function],
                                required_edge_properties = [edge_prop_calls]                   )

    def test__create_test_rule_set(self):                                                       # Verify test rule set structure
        with self.rule_set as _:
            assert type(_) == Schema__Rule_Set
            assert str(_.rule_set_ref)              == 'python_rules'
            assert len(_.required_node_properties)  == 2
            assert len(_.required_edge_properties)  == 1

    def test__init__(self):                                                                     # Test initialization
        with Rule_Set__Utils() as _:
            assert type(_) is Rule_Set__Utils

    # ═══════════════════════════════════════════════════════════════════════════
    # Required Node Property Checks (Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_required_node_property__returns_matching_rule(self):                          # Test node property lookup
        method_rule = self.utils.get_required_node_property(self.rule_set, self.method_id, self.line_number_id)

        assert method_rule is not None
        assert method_rule.required is True

        function_rule = self.utils.get_required_node_property(self.rule_set, self.function_id, self.line_number_id)

        assert function_rule is not None
        assert function_rule.required is True

    def test__get_required_node_property__returns_none_for_no_match(self):                      # Test missing rule
        unknown_type = Node_Type_Id(Obj_Id())
        unknown_prop = Property_Name_Id(Obj_Id())

        assert self.utils.get_required_node_property(self.rule_set, unknown_type, self.line_number_id) is None
        assert self.utils.get_required_node_property(self.rule_set, self.method_id, unknown_prop)      is None

    def test__is_node_property_required(self):                                                  # Test requirement check
        assert self.utils.is_node_property_required(self.rule_set, self.method_id, self.line_number_id)   is True
        assert self.utils.is_node_property_required(self.rule_set, self.function_id, self.line_number_id) is True

        unknown_prop = Property_Name_Id(Obj_Id())
        assert self.utils.is_node_property_required(self.rule_set, self.method_id, unknown_prop)          is False

    def test__get_required_properties_for_node_type(self):                                      # Test listing properties for type
        method_props = self.utils.get_required_properties_for_node_type(self.rule_set, self.method_id)

        assert len(method_props) >= 1
        assert self.line_number_id in method_props                                              # Returns list of property IDs

    # ═══════════════════════════════════════════════════════════════════════════
    # Required Edge Property Checks (Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_required_edge_property__returns_matching_rule(self):                          # Test edge property lookup
        calls_rule = self.utils.get_required_edge_property(self.rule_set, self.calls_id, self.call_count_id)

        assert calls_rule is not None
        assert calls_rule.required is False                                                     # Optional property (set in create_test_rule_set)

    def test__get_required_edge_property__returns_none_for_no_match(self):                      # Test missing rule
        unknown_pred = Predicate_Id(Obj_Id())
        unknown_prop = Property_Name_Id(Obj_Id())

        assert self.utils.get_required_edge_property(self.rule_set, unknown_pred, self.call_count_id) is None
        assert self.utils.get_required_edge_property(self.rule_set, self.calls_id, unknown_prop)      is None

    def test__is_edge_property_required(self):                                                  # Test requirement check
        # call_count on calls is optional (required=False)
        assert self.utils.is_edge_property_required(self.rule_set, self.calls_id, self.call_count_id) is False

        unknown_prop = Property_Name_Id(Obj_Id())
        assert self.utils.is_edge_property_required(self.rule_set, self.calls_id, unknown_prop)       is False

    def test__get_required_properties_for_predicate(self):                                      # Test listing properties for predicate
        calls_props = self.utils.get_required_properties_for_predicate(self.rule_set, self.calls_id)

        assert len(calls_props) >= 1
        assert self.call_count_id in calls_props                                                # Returns list of property IDs

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration with QA Test Data
    # ═══════════════════════════════════════════════════════════════════════════

    def test__qa_rule_set__has_node_property_rules(self):                                       # Test QA rule set node properties
        rule_set = self.test_data.create_rule_set()

        assert len(rule_set.required_node_properties) >= 1

        # Check that we can look up the rule for method → line_number
        method_id      = self.test_data.get_node_type_id__method()
        line_number_id = self.test_data.get_property_name_id__line_number()

        rule = self.utils.get_required_node_property(rule_set, method_id, line_number_id)
        assert rule is not None

    def test__qa_rule_set__has_edge_property_rules(self):                                       # Test QA rule set edge properties
        rule_set = self.test_data.create_rule_set()

        assert len(rule_set.required_edge_properties) >= 1

        # Check that we can look up the rule for calls → call_count
        calls_id      = self.test_data.get_predicate_id__calls()
        call_count_id = self.test_data.get_property_name_id__call_count()

        rule = self.utils.get_required_edge_property(rule_set, calls_id, call_count_id)
        assert rule is not None

    def test__qa_rule_set__ontology_id_is_set(self):                                            # Brief 3.8: ontology_id
        rule_set = self.test_data.create_rule_set()

        assert type(rule_set.ontology_id) is Ontology_Id                                        # ID not ref

    def test__qa_rule_set__empty_has_no_rules(self):                                            # Test empty rule set
        rule_set = self.test_data.create_rule_set__empty()

        unknown_type = Node_Type_Id(Obj_Id())
        unknown_prop = Property_Name_Id(Obj_Id())

        assert self.utils.get_required_node_property(rule_set, unknown_type, unknown_prop) is None
        assert self.utils.get_required_edge_property(rule_set, Predicate_Id(Obj_Id()), unknown_prop) is None
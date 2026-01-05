# ═══════════════════════════════════════════════════════════════════════════════
# Test Ontology__Utils - Tests for ontology utility operations
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
#
# Updated for Brief 3.7:
#   - Uses node_type_id instead of node_type ref keys
#   - Uses predicates dict instead of embedded relationships
#   - Uses edge_rules list instead of relationship targets
#   - is_valid_edge now takes IDs, is_valid_edge_by_ref takes refs
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                               import TestCase
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Utils                           import Ontology__Utils
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Node_Type_Ids             import List__Node_Type_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Predicate_Ids             import List__Predicate_Ids
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                    import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                   import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                    import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref                   import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                  import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data             import QA__Semantic_Graphs__Test_Data
from osbot_utils.testing.__                                                                 import __
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id


class test_Ontology__Utils(TestCase):                                                       # Test ontology utilities

    @classmethod
    def setUpClass(cls):                                                                    # Shared test objects (performance)
        cls.test_data       = QA__Semantic_Graphs__Test_Data()
        cls.utils           = Ontology__Utils()
        cls.ontology        = cls.test_data.create_test_ontology()                                          # More complex ontology for testing

        # Cache IDs for test assertions
        cls.module_id       = Node_Type_Id(Obj_Id.from_seed('test:nt:module'))
        cls.class_id        = Node_Type_Id(Obj_Id.from_seed('test:nt:class'))
        cls.method_id       = Node_Type_Id(Obj_Id.from_seed('test:nt:method'))
        cls.function_id     = Node_Type_Id(Obj_Id.from_seed('test:nt:function'))

        cls.defines_id      = Predicate_Id(Obj_Id.from_seed('test:pred:defines'))
        cls.defined_in_id   = Predicate_Id(Obj_Id.from_seed('test:pred:defined_in'))
        cls.imports_id      = Predicate_Id(Obj_Id.from_seed('test:pred:imports'))
        cls.imported_by_id  = Predicate_Id(Obj_Id.from_seed('test:pred:imported_by'))
        cls.has_id          = Predicate_Id(Obj_Id.from_seed('test:pred:has'))
        cls.in_id           = Predicate_Id(Obj_Id.from_seed('test:pred:in'))
        cls.inherits_id     = Predicate_Id(Obj_Id.from_seed('test:pred:inherits_from'))
        cls.inherited_by_id = Predicate_Id(Obj_Id.from_seed('test:pred:inherited_by'))
        cls.calls_id        = Predicate_Id(Obj_Id.from_seed('test:pred:calls'))
        cls.called_by_id    = Predicate_Id(Obj_Id.from_seed('test:pred:called_by'))

    def test__create_test_ontology(self):                                                   # Verify test ontology structure
        with self.ontology as _:
            assert type(_)           is Schema__Ontology
            assert len(_.node_types) == 4
            assert len(_.predicates) == 10
            assert len(_.edge_rules) == 7
            assert _.ontology_id     == '1899785f'
            assert _.obj()           == __(ontology_id_source=None,
                                           description='Test ontology',
                                           taxonomy_id=None,
                                           ontology_id='1899785f',
                                           ontology_ref='test_ontology',
                                           node_types=__(_95ee023e=__(node_type_id_source=None,
                                                                      description='Python module',
                                                                      node_type_id='95ee023e',
                                                                      node_type_ref='module'),
                                                         _0d6826fc=__(node_type_id_source=None,
                                                                      description='Python class',
                                                                      node_type_id='0d6826fc',
                                                                      node_type_ref='class'),
                                                         _04e5c9c0=__(node_type_id_source=None,
                                                                      description='Python method',
                                                                      node_type_id='04e5c9c0',
                                                                      node_type_ref='method'),
                                                         _99d98d2f=__(node_type_id_source=None,
                                                                      description='Python function',
                                                                      node_type_id='99d98d2f',
                                                                      node_type_ref='function')),
                                           predicates=__(ce6d03cc=__(predicate_id_source=None,
                                                                     inverse_id='b0e00137',
                                                                     description=None,
                                                                     predicate_id='ce6d03cc',
                                                                     predicate_ref='defines'),
                                                         b0e00137=__(predicate_id_source=None,
                                                                     inverse_id='ce6d03cc',
                                                                     description=None,
                                                                     predicate_id='b0e00137',
                                                                     predicate_ref='defined_in'),
                                                         _8f870f0a=__(predicate_id_source=None,
                                                                      inverse_id='c909ed61',
                                                                      description=None,
                                                                      predicate_id='8f870f0a',
                                                                      predicate_ref='imports'),
                                                         c909ed61=__(predicate_id_source=None,
                                                                     inverse_id='8f870f0a',
                                                                     description=None,
                                                                     predicate_id='c909ed61',
                                                                     predicate_ref='imported_by'),
                                                         _44396997=__(predicate_id_source=None,
                                                                      inverse_id='24646240',
                                                                      description=None,
                                                                      predicate_id='44396997',
                                                                      predicate_ref='has'),
                                                         _24646240=__(predicate_id_source=None,
                                                                      inverse_id='44396997',
                                                                      description=None,
                                                                      predicate_id='24646240',
                                                                      predicate_ref='in'),
                                                         _78713b3d=__(predicate_id_source=None,
                                                                      inverse_id='47da9761',
                                                                      description=None,
                                                                      predicate_id='78713b3d',
                                                                      predicate_ref='inherits_from'),
                                                         _47da9761=__(predicate_id_source=None,
                                                                      inverse_id='78713b3d',
                                                                      description=None,
                                                                      predicate_id='47da9761',
                                                                      predicate_ref='inherited_by'),
                                                         cbea65df=__(predicate_id_source=None,
                                                                     inverse_id='64cc8d0a',
                                                                     description=None,
                                                                     predicate_id='cbea65df',
                                                                     predicate_ref='calls'),
                                                         _64cc8d0a=__(predicate_id_source=None,
                                                                      inverse_id='cbea65df',
                                                                      description=None,
                                                                      predicate_id='64cc8d0a',
                                                                      predicate_ref='called_by')),
                                           edge_rules=[__(source_type_id='95ee023e',
                                                          predicate_id='ce6d03cc',
                                                          target_type_id='0d6826fc'),
                                                       __(source_type_id='95ee023e',
                                                          predicate_id='ce6d03cc',
                                                          target_type_id='99d98d2f'),
                                                       __(source_type_id='95ee023e',
                                                          predicate_id='8f870f0a',
                                                          target_type_id='95ee023e'),
                                                       __(source_type_id='0d6826fc',
                                                          predicate_id='44396997',
                                                          target_type_id='04e5c9c0'),
                                                       __(source_type_id='0d6826fc',
                                                          predicate_id='78713b3d',
                                                          target_type_id='0d6826fc'),
                                                       __(source_type_id='04e5c9c0',
                                                          predicate_id='cbea65df',
                                                          target_type_id='04e5c9c0'),
                                                       __(source_type_id='04e5c9c0',
                                                          predicate_id='cbea65df',
                                                          target_type_id='99d98d2f')])

    def test__init__(self):                                                                 # Test initialization
        with Ontology__Utils() as _:
            assert type(_) is Ontology__Utils

    # ═══════════════════════════════════════════════════════════════════════════
    # Valid Edge Detection (ID-based)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__valid_edge__returns_true_for_valid(self):                                     # Test valid edge detection
        assert self.utils.is_valid_edge(self.ontology, self.module_id, self.defines_id, self.class_id)    is True
        assert self.utils.is_valid_edge(self.ontology, self.module_id, self.defines_id, self.function_id) is True
        assert self.utils.is_valid_edge(self.ontology, self.module_id, self.imports_id, self.module_id)   is True
        assert self.utils.is_valid_edge(self.ontology, self.class_id,  self.has_id,     self.method_id)   is True
        assert self.utils.is_valid_edge(self.ontology, self.class_id,  self.inherits_id,self.class_id)    is True
        assert self.utils.is_valid_edge(self.ontology, self.method_id, self.calls_id,   self.method_id)   is True
        assert self.utils.is_valid_edge(self.ontology, self.method_id, self.calls_id,   self.function_id) is True

    def test__valid_edge__returns_false_for_invalid(self):                                  # Test invalid edge detection
        assert self.utils.is_valid_edge(self.ontology, self.module_id,  self.defines_id, self.method_id)   is False
        assert self.utils.is_valid_edge(self.ontology, self.class_id,   self.defines_id, self.method_id)   is False
        assert self.utils.is_valid_edge(self.ontology, self.function_id,self.has_id,     self.class_id)    is False
        # Invalid IDs
        unknown_type = Node_Type_Id(Obj_Id())
        assert self.utils.is_valid_edge(self.ontology, unknown_type, self.has_id, self.class_id) is False
        unknown_pred = Predicate_Id(Obj_Id())
        assert self.utils.is_valid_edge(self.ontology, self.module_id, unknown_pred, self.class_id) is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Valid Edge Detection (Ref-based convenience)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__valid_edge_by_ref__returns_true_for_valid(self):                              # Test valid edge by ref
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('module'), Predicate_Ref('defines'), Node_Type_Ref('class'))    is True
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('module'), Predicate_Ref('defines'), Node_Type_Ref('function')) is True
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('module'), Predicate_Ref('imports'), Node_Type_Ref('module'))   is True
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('class'),  Predicate_Ref('has'),     Node_Type_Ref('method'))   is True
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('class'),  Predicate_Ref('inherits_from'), Node_Type_Ref('class')) is True
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('method'), Predicate_Ref('calls'),   Node_Type_Ref('method'))   is True
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('method'), Predicate_Ref('calls'),   Node_Type_Ref('function')) is True

    def test__valid_edge_by_ref__returns_false_for_invalid(self):                           # Test invalid edge by ref
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('module'),  Predicate_Ref('defines'), Node_Type_Ref('method'))  is False
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('class'),   Predicate_Ref('defines'), Node_Type_Ref('method'))  is False
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('function'),Predicate_Ref('has'),     Node_Type_Ref('class'))   is False
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('invalid'), Predicate_Ref('has'),     Node_Type_Ref('class'))   is False
        assert self.utils.is_valid_edge_by_ref(self.ontology, Node_Type_Ref('module'),  Predicate_Ref('invalid'), Node_Type_Ref('class'))   is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Valid Targets Query
    # ═══════════════════════════════════════════════════════════════════════════

    def test__valid_targets_for(self):                                                      # Test valid target lookup
        targets = self.utils.valid_targets_for(self.ontology, self.module_id, self.defines_id)

        assert type(targets) is List__Node_Type_Ids
        assert len(targets)  == 2
        assert self.class_id    in targets
        assert self.function_id in targets

    def test__valid_targets_for__single_target(self):                                       # Test single valid target
        targets = self.utils.valid_targets_for(self.ontology, self.class_id, self.has_id)

        assert len(targets) == 1
        assert self.method_id in targets

    def test__valid_targets_for__no_targets(self):                                          # Test no valid targets
        targets = self.utils.valid_targets_for(self.ontology, self.function_id, self.defines_id)

        assert len(targets) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Valid Predicates Query
    # ═══════════════════════════════════════════════════════════════════════════

    def test__valid_predicates_for(self):                                                   # Test valid predicate lookup
        predicates = self.utils.valid_predicates_for(self.ontology, self.module_id)

        assert type(predicates) is List__Predicate_Ids
        assert len(predicates)  == 2
        assert self.defines_id in predicates
        assert self.imports_id in predicates

    def test__valid_predicates_for__no_predicates(self):                                    # Test no valid predicates
        predicates = self.utils.valid_predicates_for(self.ontology, self.function_id)

        assert len(predicates) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Inverse Predicate Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_inverse_predicate(self):                                                  # Test inverse predicate lookup
        defines_inverse = self.utils.get_inverse_predicate(self.ontology, self.defines_id)
        assert defines_inverse is not None
        assert defines_inverse.predicate_ref == Predicate_Ref('defined_in')

        imports_inverse = self.utils.get_inverse_predicate(self.ontology, self.imports_id)
        assert imports_inverse is not None
        assert imports_inverse.predicate_ref == Predicate_Ref('imported_by')

        has_inverse = self.utils.get_inverse_predicate(self.ontology, self.has_id)
        assert has_inverse is not None
        assert has_inverse.predicate_ref == Predicate_Ref('in')

        inherits_inverse = self.utils.get_inverse_predicate(self.ontology, self.inherits_id)
        assert inherits_inverse is not None
        assert inherits_inverse.predicate_ref == Predicate_Ref('inherited_by')

        calls_inverse = self.utils.get_inverse_predicate(self.ontology, self.calls_id)
        assert calls_inverse is not None
        assert calls_inverse.predicate_ref == Predicate_Ref('called_by')

    def test__get_inverse_predicate__returns_none_for_invalid(self):                        # Test invalid lookups
        unknown_pred = Predicate_Id(Obj_Id())
        assert self.utils.get_inverse_predicate(self.ontology, unknown_pred) is None

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Type Queries
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_node_type(self):                                                          # Test node type lookup by ID
        node_type = self.utils.get_node_type(self.ontology, self.module_id)

        assert node_type is not None
        assert node_type.node_type_ref == Node_Type_Ref('module')

    def test__get_node_type_by_ref(self):                                                   # Test node type lookup by ref
        node_type = self.utils.get_node_type_by_ref(self.ontology, Node_Type_Ref('class'))

        assert node_type is not None
        assert node_type.node_type_id == self.class_id

    def test__has_node_type(self):                                                          # Test node type existence by ID
        assert self.utils.has_node_type(self.ontology, self.module_id) is True
        assert self.utils.has_node_type(self.ontology, Node_Type_Id(Obj_Id())) is False

    def test__has_node_type_ref(self):                                                      # Test node type existence by ref
        assert self.utils.has_node_type_ref(self.ontology, Node_Type_Ref('module')) is True
        assert self.utils.has_node_type_ref(self.ontology, Node_Type_Ref('unknown')) is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Predicate Queries
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_predicate(self):                                                          # Test predicate lookup by ID
        predicate = self.utils.get_predicate(self.ontology, self.defines_id)

        assert predicate is not None
        assert predicate.predicate_ref == Predicate_Ref('defines')

    def test__get_predicate_by_ref(self):                                                   # Test predicate lookup by ref
        predicate = self.utils.get_predicate_by_ref(self.ontology, Predicate_Ref('has'))

        assert predicate is not None
        assert predicate.predicate_id == self.has_id

    def test__has_predicate(self):                                                          # Test predicate existence by ID
        assert self.utils.has_predicate(self.ontology, self.calls_id) is True
        assert self.utils.has_predicate(self.ontology, Predicate_Id(Obj_Id())) is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration with QA Test Data
    # ═══════════════════════════════════════════════════════════════════════════

    def test__qa_ontology__valid_edges(self):                                               # Test QA ontology edges
        ontology = self.test_data.create_ontology__code_structure()

        # Module contains things
        assert self.utils.is_valid_edge_by_ref(ontology, Node_Type_Ref('module'), Predicate_Ref('contains'), Node_Type_Ref('class'))    is True
        assert self.utils.is_valid_edge_by_ref(ontology, Node_Type_Ref('module'), Predicate_Ref('contains'), Node_Type_Ref('method'))   is True
        assert self.utils.is_valid_edge_by_ref(ontology, Node_Type_Ref('module'), Predicate_Ref('contains'), Node_Type_Ref('function')) is True

        # Class contains method
        assert self.utils.is_valid_edge_by_ref(ontology, Node_Type_Ref('class'), Predicate_Ref('contains'), Node_Type_Ref('method'))    is True

        # Method/function call
        assert self.utils.is_valid_edge_by_ref(ontology, Node_Type_Ref('method'), Predicate_Ref('calls'), Node_Type_Ref('method'))      is True
        assert self.utils.is_valid_edge_by_ref(ontology, Node_Type_Ref('method'), Predicate_Ref('calls'), Node_Type_Ref('function'))    is True

    def test__qa_ontology__inverse_predicates(self):                                        # Test QA ontology inverse predicates
        ontology = self.test_data.create_ontology__code_structure()

        # Get contains predicate and check inverse
        contains_pred = self.utils.get_predicate_by_ref(ontology, Predicate_Ref('contains'))
        inverse_pred  = self.utils.get_inverse_predicate(ontology, contains_pred.predicate_id)
        assert inverse_pred is not None
        assert inverse_pred.predicate_ref == Predicate_Ref('in')

        # Get calls predicate and check inverse
        calls_pred   = self.utils.get_predicate_by_ref(ontology, Predicate_Ref('calls'))
        inverse_pred = self.utils.get_inverse_predicate(ontology, calls_pred.predicate_id)
        assert inverse_pred is not None
        assert inverse_pred.predicate_ref == Predicate_Ref('called_by')
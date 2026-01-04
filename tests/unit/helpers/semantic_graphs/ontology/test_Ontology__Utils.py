# ═══════════════════════════════════════════════════════════════════════════════
# Test Ontology__Utils - Tests for ontology utility operations
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                               import TestCase
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Utils                           import Ontology__Utils
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Valid_Edges               import List__Valid_Edges
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                   import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                     import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref                    import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                  import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type       import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Relationship    import Schema__Ontology__Relationship
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb          import Safe_Str__Ontology__Verb
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data             import QA__Semantic_Graphs__Test_Data
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id


class test_Ontology__Utils(TestCase):                                                       # Test ontology utilities

    @classmethod
    def setUpClass(cls):                                                                    # Shared test objects (performance)
        cls.qa       = QA__Semantic_Graphs__Test_Data()
        cls.utils    = Ontology__Utils()
        cls.ontology = cls.create_test_ontology()                                           # More complex ontology for testing

    @classmethod
    def create_test_ontology(cls) -> Schema__Ontology:                                      # Build test ontology with rich relationships
        module_defines   = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('defined_in')  ,
                                                          targets = [Node_Type_Ref('class')                 ,
                                                                     Node_Type_Ref('function')]             )
        module_imports   = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('imported_by') ,
                                                          targets = [Node_Type_Ref('module')]               )
        module_node_type = Schema__Ontology__Node_Type(description   = 'Python module'                      ,
                                                       relationships = {'defines': module_defines           ,
                                                                        'imports': module_imports           })

        class_has        = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('in')          ,
                                                          targets = [Node_Type_Ref('method')]               )
        class_inherits   = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('inherited_by'),
                                                          targets = [Node_Type_Ref('class')]                )
        class_node_type  = Schema__Ontology__Node_Type(description   = 'Python class'                       ,
                                                       relationships = {'has'          : class_has          ,
                                                                        'inherits_from': class_inherits     })

        method_calls     = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('called_by')   ,
                                                          targets = [Node_Type_Ref('method')                ,
                                                                     Node_Type_Ref('function')]             )
        method_node_type = Schema__Ontology__Node_Type(description   = 'Python method'                      ,
                                                       relationships = {'calls': method_calls               })

        function_node_type = Schema__Ontology__Node_Type(description   = 'Python function'                  ,
                                                         relationships = {}                                 )

        return Schema__Ontology(ontology_id  = Ontology_Id(Obj_Id())                                        ,
                                ontology_ref = Ontology_Ref('test_ontology')                                ,
                                version      = '1.0.0'                                                      ,
                                description  = 'Test ontology'                                              ,
                                node_types   = {'module'  : module_node_type                                ,
                                                'class'   : class_node_type                                 ,
                                                'method'  : method_node_type                                ,
                                                'function': function_node_type                              })

    def test__create_test_ontology(self):                                                   # Verify test ontology structure
        with self.ontology as _:
            assert type(_) is Schema__Ontology
            assert _.obj() == __(version      = '1.0.0'                                                     ,
                                 ontology_id  = __SKIP__                                                    ,
                                 ontology_ref = 'test_ontology'                                             ,
                                 description  = 'Test ontology'                                             ,
                                 taxonomy_ref = ''                                                          ,
                                 node_types   = __(module   = __(description   = 'Python module'            ,
                                                                 relationships = __(defines = __(inverse = 'defined_in'             ,
                                                                                                 targets = ['class', 'function'])   ,
                                                                                    imports = __(inverse = 'imported_by'            ,
                                                                                                 targets = ['module'])              ),
                                                                 taxonomy_ref  = ''                                                 ),
                                                   _class   = __(description   = 'Python class'             ,
                                                                 relationships = __(has           = __(inverse = 'in'               ,
                                                                                                       targets = ['method'])        ,
                                                                                    inherits_from = __(inverse = 'inherited_by'     ,
                                                                                                       targets = ['class'])         ),
                                                                 taxonomy_ref  = ''                                                 ),
                                                   method   = __(description   = 'Python method'            ,
                                                                 relationships = __(calls = __(inverse = 'called_by'                ,
                                                                                               targets = ['method', 'function'])    ),
                                                                 taxonomy_ref  = ''                                                 ),
                                                   function = __(description   = 'Python function'          ,
                                                                 relationships = __()                       ,
                                                                 taxonomy_ref  = ''                                                 )))

    def test__init__(self):                                                                 # Test initialization
        with Ontology__Utils() as _:
            assert type(_) is Ontology__Utils

    # ═══════════════════════════════════════════════════════════════════════════
    # Valid Edge Detection
    # ═══════════════════════════════════════════════════════════════════════════

    def test__valid_edge__returns_true_for_valid(self):                                     # Test valid edge detection
        assert self.utils.is_valid_edge(self.ontology, 'module', 'defines', 'class')       is True
        assert self.utils.is_valid_edge(self.ontology, 'module', 'defines', 'function')    is True
        assert self.utils.is_valid_edge(self.ontology, 'module', 'imports', 'module')      is True
        assert self.utils.is_valid_edge(self.ontology, 'class', 'has', 'method')           is True
        assert self.utils.is_valid_edge(self.ontology, 'class', 'inherits_from', 'class')  is True
        assert self.utils.is_valid_edge(self.ontology, 'method', 'calls', 'method')        is True
        assert self.utils.is_valid_edge(self.ontology, 'method', 'calls', 'function')      is True

    def test__valid_edge__returns_false_for_invalid(self):                                  # Test invalid edge detection
        assert self.utils.is_valid_edge(self.ontology, 'module', 'defines', 'method')      is False
        assert self.utils.is_valid_edge(self.ontology, 'class', 'defines', 'method')       is False
        assert self.utils.is_valid_edge(self.ontology, 'function', 'has', 'class')         is False
        assert self.utils.is_valid_edge(self.ontology, 'invalid', 'has', 'class')          is False
        assert self.utils.is_valid_edge(self.ontology, 'module', 'invalid_verb', 'class')  is False

    # ═══════════════════════════════════════════════════════════════════════════
    # All Valid Edges
    # ═══════════════════════════════════════════════════════════════════════════

    def test__all_valid_edges(self):                                                        # Test listing all valid edges
        edges = self.utils.all_valid_edges(self.ontology)

        assert type(edges) is List__Valid_Edges
        assert edges.obj() == [__(source_type='module', verb='defines'      , target_type='class')   ,
                               __(source_type='module', verb='defines'      , target_type='function'),
                               __(source_type='module', verb='imports'      , target_type='module')  ,
                               __(source_type='class' , verb='has'          , target_type='method')  ,
                               __(source_type='class' , verb='inherits_from', target_type='class')   ,
                               __(source_type='method', verb='calls'        , target_type='method')  ,
                               __(source_type='method', verb='calls'        , target_type='function')]
        assert len(edges) == 7

    # ═══════════════════════════════════════════════════════════════════════════
    # Inverse Verb Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_inverse_verb(self):                                                       # Test inverse verb lookup
        assert self.utils.get_inverse_verb(self.ontology, 'module', 'defines')      == 'defined_in'
        assert self.utils.get_inverse_verb(self.ontology, 'module', 'imports')      == 'imported_by'
        assert self.utils.get_inverse_verb(self.ontology, 'class', 'has')           == 'in'
        assert self.utils.get_inverse_verb(self.ontology, 'class', 'inherits_from') == 'inherited_by'
        assert self.utils.get_inverse_verb(self.ontology, 'method', 'calls')        == 'called_by'

    def test__get_inverse_verb__returns_none_for_invalid(self):                             # Test invalid lookups
        assert self.utils.get_inverse_verb(self.ontology, 'invalid', 'has')     is None
        assert self.utils.get_inverse_verb(self.ontology, 'module', 'invalid')  is None
        assert self.utils.get_inverse_verb(self.ontology, 'function', 'calls')  is None


    # ═══════════════════════════════════════════════════════════════════════════
    # Integration with QA Test Data
    # ═══════════════════════════════════════════════════════════════════════════

    def test__qa_ontology__valid_edges(self):                                               # Test QA ontology edges
        ontology = self.qa.create_ontology__code_structure()

        # Module contains things
        assert self.utils.is_valid_edge(ontology, 'module', 'contains', 'class')    is True
        assert self.utils.is_valid_edge(ontology, 'module', 'contains', 'method')   is True
        assert self.utils.is_valid_edge(ontology, 'module', 'contains', 'function') is True

        # Class contains method
        assert self.utils.is_valid_edge(ontology, 'class', 'contains', 'method')    is True

        # Method/function call
        assert self.utils.is_valid_edge(ontology, 'method', 'calls', 'method')      is True
        assert self.utils.is_valid_edge(ontology, 'method', 'calls', 'function')    is True

    def test__qa_ontology__inverse_verbs(self):                                             # Test QA ontology inverses
        ontology = self.qa.create_ontology__code_structure()

        assert self.utils.get_inverse_verb(ontology, 'module', 'contains') == 'in'
        assert self.utils.get_inverse_verb(ontology, 'method', 'calls')    == 'called_by'
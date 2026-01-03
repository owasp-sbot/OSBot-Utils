# ═══════════════════════════════════════════════════════════════════════════════
# Test Ontology__Utils - Tests for ontology utility operations
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                               import TestCase
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Utils                           import Ontology__Utils
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                    import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                     import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                  import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type       import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Relationship    import Schema__Ontology__Relationship
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb          import Safe_Str__Ontology__Verb
from osbot_utils.testing.__ import __

# todo:
#     :
#       - move create_test_ontology to a helper QA__Semantic_Graph__Test_Data utils class
#       - add util to create visualisation of these schema in mermaid since these note only these are nice graphs,
#               that will help with creating, editing and visualising these ontologies

class test_Ontology__Utils(TestCase):                                                # Test ontology utilities

    @classmethod
    def setUpClass(cls):                                                             # Create shared test ontology
        cls.utils    = Ontology__Utils()
        cls.ontology = cls.create_test_ontology()

    @classmethod
    def create_test_ontology(cls) -> Schema__Ontology:                                                # Build test ontology
        module_defines    = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('defined_in')   ,
                                                           targets = [Node_Type_Id('class')                   ,
                                                                      Node_Type_Id('function')]              )
        module_imports    = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('imported_by')  ,
                                                           targets = [Node_Type_Id('module')]                 )
        module_node_type  = Schema__Ontology__Node_Type(description   = 'Python module'     ,
                                                        relationships = {'defines': module_defines ,
                                                                         'imports': module_imports })

        class_has         = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('in')           ,
                                                           targets = [Node_Type_Id('method')]                 )
        class_inherits    = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('inherited_by') ,
                                                           targets = [Node_Type_Id('class')]                  )
        class_node_type   = Schema__Ontology__Node_Type(description   = 'Python class'       ,
                                                        relationships = {'has'          : class_has     ,
                                                                         'inherits_from': class_inherits })

        method_calls      = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('called_by')    ,
                                                           targets = [Node_Type_Id('method')                  ,
                                                                      Node_Type_Id('function')]              )
        method_node_type  = Schema__Ontology__Node_Type(description   = 'Python method'      ,
                                                        relationships = {'calls': method_calls })

        function_node_type = Schema__Ontology__Node_Type(description   = 'Python function'   ,
                                                         relationships = {})

        return Schema__Ontology(ontology_id = Ontology_Id('test_ontology')    ,
                                version     = '1.0.0'                          ,
                                description = 'Test ontology'                 ,
                                node_types  = {'module'  : module_node_type   ,
                                               'class'   : class_node_type    ,
                                               'method'  : method_node_type   ,
                                               'function': function_node_type })


    def test__create_test_ontology(self):
        with self.ontology as _:
            assert type(_) is Schema__Ontology
            assert _.obj() == __(version     = '1.0.0'                     ,
                                 ontology_id = 'test_ontology'             ,
                                 description = 'Test ontology'             ,
                                 taxonomy_ref= ''                          ,
                                 node_types  = __(module  = __(description   = 'Python module'     ,
                                                               relationships = __(defines = __(inverse = 'defined_in' ,
                                                                                               targets = ['class', 'function'])  ,
                                                                                  imports = __(inverse = 'imported_by',
                                                                                               targets = ['module'])             ),
                                                               taxonomy_ref  = ''                                 ),
                                                  _class  = __(description   = 'Python class'      ,
                                                               relationships = __(has           = __(inverse = 'in'           ,
                                                                                                     targets = ['method'])    ,
                                                                                  inherits_from = __(inverse = 'inherited_by' ,
                                                                                                     targets = ['class'])     ),
                                                               taxonomy_ref  = ''                                 ),
                                                   method  = __(description   = 'Python method'     ,
                                                               relationships = __(calls = __(inverse = 'called_by' ,
                                                                                             targets = ['method', 'function']) ),
                                                               taxonomy_ref  = ''                                 ),
                                                   function= __(description   = 'Python function'   ,
                                                               relationships = __()                 ,
                                                               taxonomy_ref  = ''                                 )))


    def test__init__(self):                                                          # Test initialization
        with Ontology__Utils() as _:
            assert type(_) is Ontology__Utils

    def test__valid_edge__returns_true_for_valid(self):                              # Test valid edge detection
        assert self.utils.valid_edge(self.ontology, 'module', 'defines', 'class')    is True
        assert self.utils.valid_edge(self.ontology, 'module', 'defines', 'function') is True
        assert self.utils.valid_edge(self.ontology, 'module', 'imports', 'module')   is True
        assert self.utils.valid_edge(self.ontology, 'class', 'has', 'method')        is True
        assert self.utils.valid_edge(self.ontology, 'class', 'inherits_from', 'class') is True
        assert self.utils.valid_edge(self.ontology, 'method', 'calls', 'method')     is True
        assert self.utils.valid_edge(self.ontology, 'method', 'calls', 'function')   is True

    def test__valid_edge__returns_false_for_invalid(self):                           # Test invalid edge detection
        assert self.utils.valid_edge(self.ontology, 'module', 'defines', 'method')   is False
        assert self.utils.valid_edge(self.ontology, 'class', 'defines', 'method')    is False
        assert self.utils.valid_edge(self.ontology, 'function', 'has', 'class')      is False
        assert self.utils.valid_edge(self.ontology, 'invalid', 'has', 'class')       is False
        assert self.utils.valid_edge(self.ontology, 'module', 'invalid_verb', 'class') is False

    def test__all_valid_edges(self):                                                 # Test edge enumeration
        edges    = self.utils.all_valid_edges(self.ontology)
        expected = [('module', 'defines', 'class')   ,
                    ('module', 'defines', 'function'),
                    ('module', 'imports', 'module')  ,
                    ('class', 'has', 'method')       ,
                    ('class', 'inherits_from', 'class'),
                    ('method', 'calls', 'method')    ,
                    ('method', 'calls', 'function')  ]

        for edge in expected:
            assert edge in edges, f"Expected edge {edge} not found"

        assert len(edges) == 7

    def test__get_inverse_verb(self):                                                # Test inverse verb lookup
        assert self.utils.get_inverse_verb(self.ontology, 'module', 'defines')      == 'defined_in'
        assert self.utils.get_inverse_verb(self.ontology, 'module', 'imports')      == 'imported_by'
        assert self.utils.get_inverse_verb(self.ontology, 'class', 'has')           == 'in'
        assert self.utils.get_inverse_verb(self.ontology, 'class', 'inherits_from') == 'inherited_by'
        assert self.utils.get_inverse_verb(self.ontology, 'method', 'calls')        == 'called_by'

    def test__get_inverse_verb__returns_none_for_invalid(self):                      # Test invalid lookups
        assert self.utils.get_inverse_verb(self.ontology, 'invalid', 'has')    is None
        assert self.utils.get_inverse_verb(self.ontology, 'module', 'invalid') is None
        assert self.utils.get_inverse_verb(self.ontology, 'function', 'calls') is None

    def test__verbs_for_node_type(self):                                             # Test verb listing per type
        module_verbs = self.utils.verbs_for_node_type(self.ontology, 'module')
        assert 'defines' in module_verbs
        assert 'imports' in module_verbs

        class_verbs = self.utils.verbs_for_node_type(self.ontology, 'class')
        assert 'has'          in class_verbs
        assert 'inherits_from' in class_verbs

        assert self.utils.verbs_for_node_type(self.ontology, 'function') == []
        assert self.utils.verbs_for_node_type(self.ontology, 'invalid')  == []

    def test__targets_for_verb(self):                                                # Test target listing
        module_defines_targets = self.utils.targets_for_verb(self.ontology, 'module', 'defines')
        assert 'class'    in module_defines_targets
        assert 'function' in module_defines_targets
        assert 'method'   not in module_defines_targets

        class_has_targets = self.utils.targets_for_verb(self.ontology, 'class', 'has')
        assert 'method' in class_has_targets
        assert len(class_has_targets) == 1

        assert self.utils.targets_for_verb(self.ontology, 'invalid', 'has')    == []
        assert self.utils.targets_for_verb(self.ontology, 'module', 'invalid') == []

    def test__edge_forward_name(self):                                               # Test forward edge name
        assert self.utils.edge_forward_name('module', 'defines', 'class')     == 'module_defines_class'
        assert self.utils.edge_forward_name('module', 'defines', 'function')  == 'module_defines_function'
        assert self.utils.edge_forward_name('class', 'has', 'method')         == 'class_has_method'
        assert self.utils.edge_forward_name('class', 'inherits_from', 'class') == 'class_inherits_from_class'

    def test__edge_inverse_name(self):                                               # Test inverse edge name
        assert self.utils.edge_inverse_name(self.ontology, 'module', 'defines', 'class')    == 'class_defined_in_module'
        assert self.utils.edge_inverse_name(self.ontology, 'class', 'has', 'method')        == 'method_in_class'
        assert self.utils.edge_inverse_name(self.ontology, 'class', 'inherits_from', 'class') == 'class_inherited_by_class'

    def test__node_type_ids(self):                                                   # Test node type listing
        type_ids = self.utils.node_type_ids(self.ontology)

        assert 'module'   in type_ids
        assert 'class'    in type_ids
        assert 'method'   in type_ids
        assert 'function' in type_ids
        assert len(type_ids) == 4
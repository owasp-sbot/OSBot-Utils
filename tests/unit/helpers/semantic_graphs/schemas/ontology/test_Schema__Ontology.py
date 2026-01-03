from unittest                                                                               import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                    import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                     import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                  import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type       import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Relationship    import Schema__Ontology__Relationship
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb          import Safe_Str__Ontology__Verb


class test_Schema__Ontology(TestCase):                                               # Test main ontology schema

    @classmethod
    def setUpClass(cls):                                                             # Create test ontology once
        cls.ontology = cls.create_test_ontology()

    @classmethod
    def create_test_ontology(cls) -> Schema__Ontology:                               # Build minimal test ontology
        module_defines = Schema__Ontology__Relationship(                             # module -> class, function
            inverse = Safe_Str__Ontology__Verb('defined_in')                         ,
            targets = [Node_Type_Id('class'), Node_Type_Id('function')]              ,
        )
        module_imports = Schema__Ontology__Relationship(                             # module -> module
            inverse = Safe_Str__Ontology__Verb('imported_by')                        ,
            targets = [Node_Type_Id('module')]                                       ,
        )
        module_node_type = Schema__Ontology__Node_Type(
            description   = 'Python module'                                          ,
            relationships = {'defines': module_defines, 'imports': module_imports}   ,
        )

        class_has = Schema__Ontology__Relationship(                                  # class -> method
            inverse = Safe_Str__Ontology__Verb('in')                                 ,
            targets = [Node_Type_Id('method')]                                       ,
        )
        class_inherits = Schema__Ontology__Relationship(                             # class -> class
            inverse = Safe_Str__Ontology__Verb('inherited_by')                       ,
            targets = [Node_Type_Id('class')]                                        ,
        )
        class_node_type = Schema__Ontology__Node_Type(
            description   = 'Python class'                                           ,
            relationships = {'has': class_has, 'inherits_from': class_inherits}      ,
        )

        method_calls = Schema__Ontology__Relationship(                               # method -> method, function
            inverse = Safe_Str__Ontology__Verb('called_by')                          ,
            targets = [Node_Type_Id('method'), Node_Type_Id('function')]             ,
        )
        method_node_type = Schema__Ontology__Node_Type(
            description   = 'Python method'                                          ,
            relationships = {'calls': method_calls}                                  ,
        )

        function_node_type = Schema__Ontology__Node_Type(                            # function (no relationships)
            description   = 'Python function'                                        ,
            relationships = {}                                                       ,
        )

        return Schema__Ontology(
            ontology_id = Ontology_Id('test_ontology')                                ,
            version     = '1.0.0'                                                    ,
            description = 'Test ontology for unit tests'                             ,
            node_types  = {
                'module'  : module_node_type                                         ,
                'class'   : class_node_type                                          ,
                'method'  : method_node_type                                         ,
                'function': function_node_type                                       ,
            }                                                                        ,
        )

    def test__init__(self):                                                          # Test basic initialization
        with Schema__Ontology(ontology_id=Ontology_Id('empty')) as _:
            assert type(_.ontology_id)  is Ontology_Id
            assert str(_.ontology_id)   == 'empty'
            assert str(_.version)       == '1.0.0'                                   # Default version
            assert str(_.description)   == ''
            assert _.node_types         == {}

    def test__ontology_structure(self):                                              # Test full ontology structure
        with self.ontology as _:
            assert str(_.ontology_id)   == 'test_ontology'
            assert str(_.version)       == '1.0.0'
            assert len(_.node_types)    == 4

    def test__valid_edge__returns_true_for_valid_edges(self):                        # Test valid edge detection
        with self.ontology as _:
            assert _.valid_edge('module', 'defines', 'class')        is True
            assert _.valid_edge('module', 'defines', 'function')     is True
            assert _.valid_edge('module', 'imports', 'module')       is True
            assert _.valid_edge('class', 'has', 'method')            is True
            assert _.valid_edge('class', 'inherits_from', 'class')   is True
            assert _.valid_edge('method', 'calls', 'method')         is True
            assert _.valid_edge('method', 'calls', 'function')       is True

    def test__valid_edge__returns_false_for_invalid_edges(self):                     # Test invalid edge detection
        with self.ontology as _:
            assert _.valid_edge('module', 'defines', 'method')       is False        # method not in targets
            assert _.valid_edge('class', 'defines', 'method')        is False        # class has 'has', not 'defines'
            assert _.valid_edge('function', 'has', 'class')          is False        # function has no relationships
            assert _.valid_edge('invalid', 'has', 'class')           is False        # invalid source type
            assert _.valid_edge('module', 'invalid_verb', 'class')   is False        # invalid verb

    def test__get_inverse_verb(self):                                                # Test inverse verb lookup
        with self.ontology as _:
            assert _.get_inverse_verb('module', 'defines')       == 'defined_in'
            assert _.get_inverse_verb('module', 'imports')       == 'imported_by'
            assert _.get_inverse_verb('class', 'has')            == 'in'
            assert _.get_inverse_verb('class', 'inherits_from')  == 'inherited_by'
            assert _.get_inverse_verb('method', 'calls')         == 'called_by'

    def test__get_inverse_verb__returns_none_for_invalid(self):                      # Test invalid lookups
        with self.ontology as _:
            assert _.get_inverse_verb('invalid', 'has')          is None
            assert _.get_inverse_verb('module', 'invalid')       is None
            assert _.get_inverse_verb('function', 'calls')       is None             # function has no relationships

    def test__edge_forward_name(self):                                               # Test forward edge name computation
        with self.ontology as _:
            assert _.edge_forward_name('module', 'defines', 'class')    == 'module_defines_class'
            assert _.edge_forward_name('module', 'defines', 'function') == 'module_defines_function'
            assert _.edge_forward_name('class', 'has', 'method')        == 'class_has_method'
            assert _.edge_forward_name('class', 'inherits_from', 'class') == 'class_inherits_from_class'

    def test__edge_inverse_name(self):                                               # Test inverse edge name computation
        with self.ontology as _:
            assert _.edge_inverse_name('module', 'defines', 'class')    == 'class_defined_in_module'
            assert _.edge_inverse_name('class', 'has', 'method')        == 'method_in_class'
            assert _.edge_inverse_name('class', 'inherits_from', 'class') == 'class_inherited_by_class'

    def test__all_valid_edges(self):                                                 # Test edge enumeration
        with self.ontology as _:
            edges = _.all_valid_edges()

            expected = [                                                             # All expected valid edges
                ('module', 'defines', 'class')                                       ,
                ('module', 'defines', 'function')                                    ,
                ('module', 'imports', 'module')                                      ,
                ('class', 'has', 'method')                                           ,
                ('class', 'inherits_from', 'class')                                  ,
                ('method', 'calls', 'method')                                        ,
                ('method', 'calls', 'function')                                      ,
            ]

            for edge in expected:
                assert edge in edges, f"Expected edge {edge} not found"

            assert len(edges) == 7                                                   # Exactly 7 valid edges

    def test__node_type_ids(self):                                                   # Test node type listing
        with self.ontology as _:
            type_ids = _.node_type_ids()
            assert 'module'   in type_ids
            assert 'class'    in type_ids
            assert 'method'   in type_ids
            assert 'function' in type_ids
            assert len(type_ids) == 4

    def test__verbs_for_node_type(self):                                             # Test verb listing per type
        with self.ontology as _:
            module_verbs = _.verbs_for_node_type('module')
            assert 'defines' in module_verbs
            assert 'imports' in module_verbs

            class_verbs = _.verbs_for_node_type('class')
            assert 'has'          in class_verbs
            assert 'inherits_from' in class_verbs

            assert _.verbs_for_node_type('function') == []                           # No verbs
            assert _.verbs_for_node_type('invalid')  == []                           # Invalid type

    def test__targets_for_verb(self):                                                # Test target listing
        with self.ontology as _:
            module_defines_targets = _.targets_for_verb('module', 'defines')
            assert 'class'    in module_defines_targets
            assert 'function' in module_defines_targets
            assert 'method'   not in module_defines_targets

            class_has_targets = _.targets_for_verb('class', 'has')
            assert 'method' in class_has_targets
            assert len(class_has_targets) == 1

            assert _.targets_for_verb('invalid', 'has')    == []                     # Invalid source
            assert _.targets_for_verb('module', 'invalid') == []                     # Invalid verb

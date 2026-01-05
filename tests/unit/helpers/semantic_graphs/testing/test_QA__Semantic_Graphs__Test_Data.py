# ═══════════════════════════════════════════════════════════════════════════════
# Test QA__Semantic_Graphs__Test_Data - Tests for semantic graphs test data factory
#
# Updated for Brief 3.7:
#   - Node types use node_type_id (not embedded relationships)
#   - Predicates are first-class entities
#   - Edge rules define valid connections
#   - All cross-references use IDs
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Ref         import Dict__Categories__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id          import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id               import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicates__By_Id          import Dict__Predicates__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Refs              import List__Category_Refs
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Edge_Rules                 import List__Edge_Rules
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Cardinality         import List__Rules__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Transitivity        import List__Rules__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges      import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type                  import Enum__Id__Source_Type
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph                import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge          import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node          import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                     import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                     import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                    import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                      import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                     import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref                    import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                      import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                      import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                   import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Edge_Rule        import Schema__Ontology__Edge_Rule
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type        import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Predicate        import Schema__Ontology__Predicate
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                       import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality              import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity             import Schema__Rule__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy                   import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category         import Schema__Taxonomy__Category
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data              import QA__Semantic_Graphs__Test_Data
from osbot_utils.testing.__                                                                  import __, __SKIP__
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                            import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                           import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                            import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                             import Obj_Id
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Registry                         import Ontology__Registry
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Type_Ids__By_Ref      import Dict__Node_Type_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicate_Ids__By_Ref      import Dict__Predicate_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Projected__Edges           import List__Projected__Edges
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Projected__Nodes           import List__Projected__Nodes
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Data           import Schema__Projected__Data
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Edge           import Schema__Projected__Edge
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Node           import Schema__Projected__Node
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__References     import Schema__Projected__References
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Semantic_Graph import Schema__Projected__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Sources        import Schema__Projected__Sources
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data              import EXPECTED__PROJECTED__SIMPLE_CLASS__NODES
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data              import EXPECTED__PROJECTED__SIMPLE_CLASS__EDGES
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data              import EXPECTED__PROJECTED__SIMPLE_CLASS__REFERENCES__NODES
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data              import EXPECTED__PROJECTED__SIMPLE_CLASS__REFERENCES__EDGES
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now             import Timestamp_Now
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id              import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed        import Safe_Str__Id__Seed

class test_QA__Semantic_Graphs__Test_Data(TestCase):                                       # Test QA test data factory

    @classmethod
    def setUpClass(cls):                                                                   # Shared test_data instance
        cls.test_data = QA__Semantic_Graphs__Test_Data()

    def test__init__(self):                                                                # Test basic initialization
        with QA__Semantic_Graphs__Test_Data() as _:
            assert type(_) is QA__Semantic_Graphs__Test_Data

    # ═══════════════════════════════════════════════════════════════════════════
    # Taxonomy Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_category(self):                                                       # Test category creation
        with self.test_data as _:
            category = _.create_category(category_ref = Category_Ref('test_cat')         ,
                                         description  = 'Test description'               )

            assert type(category)              is Schema__Taxonomy__Category
            assert str(category.category_ref)  == 'test_cat'
            assert str(category.name)          == 'test_cat'                               # Defaults to ref
            assert str(category.description)   == 'Test description'
            assert str(category.parent_ref)    == ''
            assert type(category.child_refs)   is List__Category_Refs
            assert len(category.child_refs)    == 0
            assert category.obj()              == __(category_ref = 'test_cat'         ,
                                                     name         = 'test_cat'         ,
                                                     description  = 'Test description' ,
                                                     parent_ref   = ''                 ,
                                                     child_refs   = []                )


    def test__create_category__with_children(self):                                        # Test category with children
        child_refs = List__Category_Refs([Category_Ref('child1'), Category_Ref('child2')])
        with self.test_data as _:
            category = _.create_category(category_ref = Category_Ref('parent')      ,
                                         parent_ref   = Category_Ref('grandparent') ,
                                         child_refs   = child_refs                  )

            assert 'child1' in [str(c) for c in category.child_refs]
            assert 'child2' in [str(c) for c in category.child_refs]
            assert str(category.parent_ref)  == 'grandparent'
            assert len(category.child_refs)  == 2
            assert category.obj()            == __(category_ref = 'parent'            ,
                                                   name         = 'parent'            ,
                                                   description  = ''                  ,
                                                   parent_ref   = 'grandparent'       ,
                                                   child_refs   = ['child1', 'child2'])


    def test__create_taxonomy__code_elements(self):                                        # Test code elements taxonomy
        with self.test_data as _:
            taxonomy = _.create_taxonomy__code_elements()

            assert type(taxonomy)              is Schema__Taxonomy
            assert type(taxonomy.taxonomy_id)  is Taxonomy_Id
            assert str(taxonomy.taxonomy_ref)  == 'code_elements'
            assert taxonomy.version            == '1.0.0'
            assert taxonomy.root_category      == 'code_element'
            assert type(taxonomy.categories)   is Dict__Categories__By_Ref
            assert len(taxonomy.categories)    == 4
            assert taxonomy.taxonomy_id        == str(Obj_Id.from_seed('test:taxonomy:code_elements'))

            category_refs = [str(k) for k in taxonomy.categories.keys()]               # Check all categories exist
            assert 'code_element' in category_refs
            assert 'container'    in category_refs
            assert 'code_unit'    in category_refs
            assert 'callable'     in category_refs
            assert taxonomy.obj() == __(taxonomy_id_source = None                            ,
                                        version            = '1.0.0'                         ,
                                        taxonomy_id        = '5fb24b5a'                      ,
                                        taxonomy_ref       = 'code_elements'                 ,
                                        description        = 'Code elements taxonomy'        ,
                                        root_category      = 'code_element'                  ,
                                        categories         = __(code_element = __(category_ref = 'code_element'       ,
                                                                                  name         = 'code_element'       ,
                                                                                  description  = 'Root category'      ,
                                                                                  parent_ref   = ''                   ,
                                                                                  child_refs   = ['container', 'code_unit']),
                                                                container    = __(category_ref = 'container'          ,
                                                                                  name         = 'container'          ,
                                                                                  description  = 'Container elements' ,
                                                                                  parent_ref   = 'code_element'       ,
                                                                                  child_refs   = []                  ),
                                                                code_unit    = __(category_ref = 'code_unit'          ,
                                                                                  name         = 'code_unit'          ,
                                                                                  description  = 'Executable code'    ,
                                                                                  parent_ref   = 'code_element'       ,
                                                                                  child_refs   = ['callable']        ),
                                                                callable     = __(category_ref = 'callable'           ,
                                                                                  name         = 'callable'           ,
                                                                                  description  = 'Callable code'      ,
                                                                                  parent_ref   = 'code_unit'          ,
                                                                                  child_refs   = []                  )))


    def test__create_taxonomy__code_elements__hierarchy(self):                             # Test taxonomy hierarchy
        with self.test_data as _:
            taxonomy = _.create_taxonomy__code_elements()

            root = taxonomy.categories[Category_Ref('code_element')]
            assert len(root.child_refs) == 2

            code_unit = taxonomy.categories[Category_Ref('code_unit')]
            assert str(code_unit.parent_ref)      == 'code_element'
            assert len(code_unit.child_refs)      == 1
            assert str(code_unit.child_refs[0])   == 'callable'


    def test__create_taxonomy__minimal(self):                                              # Test minimal taxonomy
        with self.test_data as _:
            taxonomy = _.create_taxonomy__minimal()

            assert type(taxonomy)                is Schema__Taxonomy
            assert str(taxonomy.taxonomy_ref)    == 'minimal'
            assert len(taxonomy.categories)      == 1
            assert str(taxonomy.root_category)   == 'root'
            assert taxonomy.obj()                == __(taxonomy_id_source = None                         ,
                                                       version            = '1.0.0'                      ,
                                                       taxonomy_id        = '880a1c12'                   ,
                                                       taxonomy_ref       = 'minimal'                    ,
                                                       description        = 'Minimal test taxonomy'      ,
                                                       root_category      = 'root'                       ,
                                                       categories         = __(root = __(category_ref = 'root'         ,
                                                                                          name         = 'root'         ,
                                                                                          description  = 'Root category',
                                                                                          parent_ref   = ''             ,
                                                                                          child_refs   = []            )))


    def test__create_taxonomy__deterministic_id(self):                                     # Test deterministic taxonomy ID
        with self.test_data as _:
            taxonomy_1 = _.create_taxonomy__code_elements()
            taxonomy_2 = _.create_taxonomy__code_elements()

            assert taxonomy_1.taxonomy_id == taxonomy_2.taxonomy_id                        # Same seed → same ID
            assert taxonomy_1.obj()       == taxonomy_2.obj()
            assert taxonomy_1.json()      == taxonomy_2.json()

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Type Tests (now with IDs)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_node_type(self):                                                      # Test node type creation
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed

        with self.test_data as _:
            node_type = _.create_node_type(node_type_ref = Node_Type_Ref('test_type')    ,
                                           description   = 'Test node type'              ,
                                           seed          = Safe_Str__Id__Seed('test:node_type:test'))

            assert type(node_type)                   is Schema__Ontology__Node_Type
            assert type(node_type.node_type_id)      is Node_Type_Id
            assert str(node_type.node_type_ref)      == 'test_type'
            assert str(node_type.description)        == 'Test node type'
            assert node_type.node_type_id_source     is not None
            assert node_type.node_type_id            == str(Obj_Id.from_seed('test:node_type:test'))
            assert node_type.obj()                   == __(node_type_id_source = __(source_type = 'deterministic'       ,
                                                                                    seed        = 'test:node_type:test'),
                                                           node_type_id        = str(Obj_Id.from_seed('test:node_type:test')),
                                                           node_type_ref       = 'test_type'                            ,
                                                           description         = 'Test node type'                       )

    def test__create_node_type__random_id(self):                                           # Test node type with random ID
        with self.test_data as _:
            node_type = _.create_node_type(node_type_ref = Node_Type_Ref('random_type'),
                                           description   = 'Random type'              )

            assert type(node_type.node_type_id)  is Node_Type_Id
            assert node_type.node_type_id_source is None                                   # No source for random ID
            assert len(str(node_type.node_type_id)) == 8                                   # Valid Obj_Id

    # ═══════════════════════════════════════════════════════════════════════════
    # Predicate Tests (new)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_predicate(self):                                                      # Test predicate creation
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed

        with self.test_data as _:
            predicate = _.create_predicate(predicate_ref = Predicate_Ref('test_rel')     ,
                                           description   = 'Test relationship'           ,
                                           seed          = Safe_Str__Id__Seed('test:predicate:test'))

            assert type(predicate)                   is Schema__Ontology__Predicate
            assert type(predicate.predicate_id)      is Predicate_Id
            assert str(predicate.predicate_ref)      == 'test_rel'
            assert str(predicate.description)        == 'Test relationship'
            assert predicate.inverse_id              is None
            assert predicate.predicate_id            == str(Obj_Id.from_seed('test:predicate:test'))
            assert predicate.obj()                   == __(predicate_id_source = __(source_type = 'deterministic'         ,
                                                                                     seed        = 'test:predicate:test') ,
                                                           predicate_id        = str(Obj_Id.from_seed('test:predicate:test')),
                                                           predicate_ref       = 'test_rel'                               ,
                                                           inverse_id          = None                                     ,
                                                           description         = 'Test relationship'                      )

    def test__create_predicate__with_inverse(self):                                        # Test predicate with inverse
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed

        inverse_id = Predicate_Id(Obj_Id.from_seed('test:predicate:inverse'))
        with self.test_data as _:
            predicate = _.create_predicate(predicate_ref = Predicate_Ref('contains')          ,
                                           inverse_id    = inverse_id                         ,
                                           seed          = Safe_Str__Id__Seed('test:predicate:contains'))

            assert predicate.inverse_id == inverse_id

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Rule Tests (new)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_edge_rule(self):                                                      # Test edge rule creation
        source_id    = Node_Type_Id(Obj_Id.from_seed('test:node_type:class'))
        predicate_id = Predicate_Id(Obj_Id.from_seed('test:predicate:contains'))
        target_id    = Node_Type_Id(Obj_Id.from_seed('test:node_type:method'))

        with self.test_data as _:
            rule = _.create_edge_rule(source_type_id = source_id   ,
                                      predicate_id   = predicate_id,
                                      target_type_id = target_id   )

            assert type(rule)           is Schema__Ontology__Edge_Rule
            assert rule.source_type_id  == source_id
            assert rule.predicate_id    == predicate_id
            assert rule.target_type_id  == target_id
            assert rule.obj()           == __(source_type_id = str(source_id)   ,
                                              predicate_id   = str(predicate_id),
                                              target_type_id = str(target_id)   )

    # ═══════════════════════════════════════════════════════════════════════════
    # Ontology Tests (normalized structure)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_ontology__code_structure(self):                                       # Test code structure ontology
        with self.test_data as _:
            ontology = _.create_ontology__code_structure()

            assert type(ontology)              is Schema__Ontology
            assert type(ontology.ontology_id)  is Ontology_Id
            assert ontology.ontology_ref       == 'code_structure'
            assert type(ontology.taxonomy_id)  is Taxonomy_Id                              # Now uses taxonomy_id not ref
            assert type(ontology.node_types)   is Dict__Node_Types__By_Id                  # Now by ID
            assert type(ontology.predicates)   is Dict__Predicates__By_Id                  # New: predicates
            assert type(ontology.edge_rules)   is List__Edge_Rules                         # New: edge_rules
            assert len(ontology.node_types)    == 4
            assert len(ontology.predicates)    == 4                                        # contains, in, calls, called_by
            assert len(ontology.edge_rules)    == 12                                       # All valid edge combinations

            assert ontology.ontology_id        == str(Obj_Id.from_seed('test:ontology:code_structure'))
            assert ontology.taxonomy_id        == str(Obj_Id.from_seed('test:taxonomy:code_elements'))

            # Verify node types by checking refs
            node_type_refs = [nt.node_type_ref for nt in ontology.node_types.values()]
            assert Node_Type_Ref('module')   in node_type_refs
            assert Node_Type_Ref('class')    in node_type_refs
            assert Node_Type_Ref('method')   in node_type_refs
            assert Node_Type_Ref('function') in node_type_refs

            # Verify predicates by checking refs
            predicate_refs = [p.predicate_ref for p in ontology.predicates.values()]
            assert Predicate_Ref('contains')  in predicate_refs
            assert Predicate_Ref('in')        in predicate_refs
            assert Predicate_Ref('calls')     in predicate_refs
            assert Predicate_Ref('called_by') in predicate_refs

    def test__create_ontology__code_structure__predicates(self):                           # Test ontology predicates
        with self.test_data as _:
            ontology = _.create_ontology__code_structure()

            # Find contains predicate
            contains_pred = None
            in_pred       = None
            for pred in ontology.predicates.values():
                if pred.predicate_ref == Predicate_Ref('contains'):
                    contains_pred = pred
                elif pred.predicate_ref == Predicate_Ref('in'):
                    in_pred = pred

            assert contains_pred is not None
            assert in_pred       is not None
            assert contains_pred.inverse_id == in_pred.predicate_id                        # Linked inverses
            assert in_pred.inverse_id       == contains_pred.predicate_id

    def test__create_ontology__code_structure__edge_rules(self):                           # Test ontology edge rules
        with self.test_data as _:
            ontology = _.create_ontology__code_structure()

            # Get IDs for verification
            module_id   = Node_Type_Id(Obj_Id.from_seed('test:node_type:module'))
            class_id    = Node_Type_Id(Obj_Id.from_seed('test:node_type:class'))
            method_id   = Node_Type_Id(Obj_Id.from_seed('test:node_type:method'))
            contains_id = Predicate_Id(Obj_Id.from_seed('test:predicate:contains'))

            # Check module contains class is a valid rule
            has_module_contains_class = False
            for rule in ontology.edge_rules:
                if (rule.source_type_id == module_id and
                    rule.predicate_id   == contains_id and
                    rule.target_type_id == class_id):
                    has_module_contains_class = True
                    break

            assert has_module_contains_class

    def test__create_ontology__minimal(self):                                              # Test minimal ontology
        with self.test_data as _:
            ontology = _.create_ontology__minimal()

            assert type(ontology)             is Schema__Ontology
            assert str(ontology.ontology_ref) == 'minimal'
            assert len(ontology.node_types)   == 1
            assert len(ontology.predicates)   == 0
            assert len(ontology.edge_rules)   == 0

            # Check entity node type exists (by looking at refs)
            entity_found = False
            for nt in ontology.node_types.values():
                if nt.node_type_ref == Node_Type_Ref('entity'):
                    entity_found = True
                    break
            assert entity_found

            # Use __SKIP__ for the dynamic key
            entity_id = str(Obj_Id.from_seed('test:node_type:entity'))
            assert ontology.obj()             == __(ontology_id_source = None                                 ,
                                                    ontology_id        = '33b3df6f'                           ,
                                                    ontology_ref       = 'minimal'                            ,
                                                    description        = 'Minimal test ontology'              ,
                                                    taxonomy_id        = '880a1c12'                           ,
                                                    node_types         = __SKIP__                             ,  # Key is dynamic ID
                                                    predicates         = __()                                 ,
                                                    edge_rules         = []                                   )

            # Verify the node type separately
            for nt in ontology.node_types.values():
                assert nt.node_type_ref == Node_Type_Ref('entity')
                assert nt.obj() == __(node_type_id_source = __(source_type = 'deterministic'            ,
                                                                seed        = 'test:node_type:entity') ,
                                      node_type_id        = entity_id                                   ,
                                      node_type_ref       = 'entity'                                    ,
                                      description         = 'Generic entity'                           )


    def test__create_ontology__deterministic_id(self):                                     # Test deterministic ontology ID
        with self.test_data as _:
            ontology_1 = _.create_ontology__code_structure()
            ontology_2 = _.create_ontology__code_structure()

            assert ontology_1.ontology_id == ontology_2.ontology_id                        # Same seed → same ID
            assert ontology_1.json()      == ontology_2.json()
            assert ontology_1.obj()       == ontology_2.obj()

    # ═══════════════════════════════════════════════════════════════════════════
    # Rule Set Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_rule_set__code_structure(self):                                       # Test code structure rules
        with self.test_data as _:
            rule_set = _.create_rule_set__code_structure()

            assert type(rule_set)                   is Schema__Rule_Set
            assert type(rule_set.rule_set_id)       is Rule_Set_Id
            assert rule_set.rule_set_ref            == 'code_structure_rules'
            assert rule_set.ontology_ref            == 'code_structure'
            assert type(rule_set.transitivity_rules) is List__Rules__Transitivity
            assert type(rule_set.cardinality_rules)  is List__Rules__Cardinality
            assert len(rule_set.transitivity_rules)  == 1
            assert len(rule_set.cardinality_rules)   == 1

            assert rule_set.rule_set_id              == str(Obj_Id.from_seed('test:rules:code_structure'))


    def test__create_rule_set__code_structure__transitivity(self):                         # Test transitivity rule
        with self.test_data as _:
            rule_set = _.create_rule_set__code_structure()
            trans_rule = rule_set.transitivity_rules[0]

            assert type(trans_rule)            is Schema__Rule__Transitivity
            assert str(trans_rule.source_type) == 'method'
            assert str(trans_rule.verb)        == 'in'
            assert str(trans_rule.target_type) == 'module'

    def test__create_rule_set__code_structure__cardinality(self):                          # Test cardinality rule
        with self.test_data as _:
            rule_set = _.create_rule_set__code_structure()
            card_rule = rule_set.cardinality_rules[0]

            assert type(card_rule)            is Schema__Rule__Cardinality
            assert str(card_rule.source_type) == 'method'
            assert str(card_rule.verb)        == 'in'
            assert str(card_rule.target_type) == 'class'
            assert int(card_rule.min_targets) == 1
            assert int(card_rule.max_targets) == 1

    def test__create_rule_set__empty(self):                                                # Test empty rule set
        with self.test_data as _:
            rule_set = _.create_rule_set__empty()

            assert type(rule_set)                    is Schema__Rule_Set
            assert str(rule_set.rule_set_ref)        == 'empty_rules'
            assert len(rule_set.transitivity_rules)  == 0
            assert len(rule_set.cardinality_rules)   == 0
            assert rule_set.obj()                    == __(rule_set_id_source  = None                            ,
                                                           version              = '1.0.0'                         ,
                                                           rule_set_id          = '1084ba3a'                      ,
                                                           rule_set_ref         = 'empty_rules'                   ,
                                                           ontology_ref         = 'minimal'                       ,
                                                           description          = 'Empty rule set for testing'    ,
                                                           transitivity_rules   = []                              ,
                                                           cardinality_rules    = []                              )


    def test__create_rule_set__deterministic_id(self):                                     # Test deterministic rule set ID
        with self.test_data as _:
            rule_set_1 = _.create_rule_set__code_structure()
            rule_set_2 = _.create_rule_set__code_structure()

            assert rule_set_1.rule_set_id == rule_set_2.rule_set_id                        # Same seed → same ID
            assert rule_set_1.json()      == rule_set_2.json()
            assert rule_set_1.obj()       == rule_set_2.obj()

    # ═══════════════════════════════════════════════════════════════════════════
    # Graph Tests (ID-based)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_node(self):                                                           # Test node creation
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id

        node_type_id = Node_Type_Id(Obj_Id.from_seed('test:node_type:class'))
        with self.test_data as _:
            seed = 'test:node:TestClass'
            node = _.create_node(node_type_id = node_type_id                 ,
                                 name         = Safe_Str__Id('TestClass')    ,
                                 seed         = Safe_Str__Id__Seed(seed)     )

            assert type(node)                      is Schema__Semantic_Graph__Node
            assert type(node.node_id)              is Node_Id
            assert node.node_type_id               == node_type_id                         # Uses node_type_id
            assert node.name                       == 'TestClass'
            assert node.node_id                    == str(Obj_Id.from_seed(seed))
            assert node.node_id_source             is not None
            assert node.node_id_source.source_type == Enum__Id__Source_Type.DETERMINISTIC
            assert node.node_id_source.seed        == seed

            assert node.obj()                      == __(node_id_source = __(source_type = 'deterministic'       ,
                                                                             seed        = 'test:node:TestClass'),
                                                         node_id        = '30a65568'                             ,
                                                         node_type_id   = str(node_type_id)                      ,
                                                         name           = 'TestClass'                            )

    def test__create_node__random_id(self):                                                # Test node with random ID
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id

        node_type_id = Node_Type_Id(Obj_Id.from_seed('test:node_type:method'))
        with self.test_data as _:
            node = _.create_node(node_type_id = node_type_id              ,
                                 name         = Safe_Str__Id('test_method'))

            assert node.node_id_source is None                                             # No source for random ID
            assert node.obj()          == __(node_id_source = None                  ,
                                             node_id        = __SKIP__              ,
                                             node_type_id   = str(node_type_id)     ,
                                             name           = 'test_method'         )

    def test__create_edge(self):                                                           # Test edge creation
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed

        node__seed_1 = 'node1'
        node__seed_2 = 'node2'
        edge__seed_1 = 'test:edge:1_contains_2'

        node_id_1    = Node_Id(Obj_Id.from_seed(node__seed_1))
        node_id_2    = Node_Id(Obj_Id.from_seed(node__seed_2))
        predicate_id = Predicate_Id(Obj_Id.from_seed('test:predicate:contains'))

        with self.test_data as _:
            edge = _.create_edge(from_node_id = node_id_1                            ,
                                 predicate_id = predicate_id                         ,
                                 to_node_id   = node_id_2                            ,
                                 seed         = Safe_Str__Id__Seed(edge__seed_1)     )

            assert type(edge)                      is Schema__Semantic_Graph__Edge
            assert type(edge.edge_id)              is Edge_Id
            assert edge.from_node_id               == node_id_1                            # Uses from_node_id
            assert edge.predicate_id               == predicate_id                         # Uses predicate_id
            assert edge.to_node_id                 == node_id_2                            # Uses to_node_id
            assert edge.edge_id_source             is not None
            assert edge.edge_id_source.source_type == Enum__Id__Source_Type.DETERMINISTIC
            assert edge.edge_id                    == str(Obj_Id.from_seed(edge__seed_1))
            assert edge.obj()                      == __(edge_id_source = __(source_type = 'deterministic'        ,
                                                                              seed        = 'test:edge:1_contains_2'),
                                                         edge_id        = 'e12d8dd1'                               ,
                                                         from_node_id   = 'ca12f31b'                               ,
                                                         to_node_id     = '15b18a72'                               ,
                                                         predicate_id   = str(predicate_id)                        )

    def test__create_graph__simple_class(self):                                            # Test simple class graph
        with self.test_data as _:
            graph = _.create_graph__simple_class()

            assert type(graph)               is Schema__Semantic_Graph
            assert type(graph.graph_id)      is Graph_Id
            assert type(graph.ontology_id)   is Ontology_Id                                # Uses ontology_id
            assert type(graph.rule_set_id)   is Rule_Set_Id                                # Uses rule_set_id
            assert type(graph.nodes)         is Dict__Nodes__By_Id
            assert type(graph.edges)         is List__Semantic_Graph__Edges
            assert len(graph.nodes)          == 3
            assert len(graph.edges)          == 2
            assert graph.graph_id            == str(Obj_Id.from_seed('test:graph:simple_class'))
            assert graph.ontology_id         == str(Obj_Id.from_seed('test:ontology:code_structure'))
            assert graph.rule_set_id         == str(Obj_Id.from_seed('test:rules:code_structure'))
            assert graph.obj()               == __(graph_id_source = None                                ,
                                                   rule_set_id      = 'd01d41cc'                          ,
                                                   graph_id         = 'c13f47de'                          ,
                                                   ontology_id      = 'c6c846c6'                          ,
                                                   nodes            = __(ff5bcf64  = __(node_id_source = __(source_type    = 'deterministic'        ,
                                                                                                            seed           = 'test:node:my_module') ,
                                                                                         node_id        = 'ff5bcf64'                                ,
                                                                                         node_type_id   = 'd84ade10'                                ,
                                                                                         name           = 'my_module'                               ),
                                                                          _02a4d1fa = __(node_id_source = __(source_type    = 'deterministic'        ,
                                                                                                            seed           = 'test:node:MyClass')    ,
                                                                                         node_id        = '02a4d1fa'                                ,
                                                                                         node_type_id   = '2a530b24'                                ,
                                                                                         name           = 'MyClass'                                 ),
                                                                          _53b63bbe = __(node_id_source = __(source_type    = 'deterministic'        ,
                                                                                                            seed           = 'test:node:my_method')  ,
                                                                                         node_id        = '53b63bbe'                                ,
                                                                                         node_type_id   = '99a23b6f'                                ,
                                                                                         name           = 'my_method'                               )),
                                                   edges            = [__(edge_id_source = __(source_type    = 'deterministic'                      ,
                                                                                             seed           = 'test:edge:module_contains_class')   ,
                                                                          edge_id        = 'fa07486e'                                              ,
                                                                          from_node_id   = 'ff5bcf64'                                              ,
                                                                          to_node_id     = '02a4d1fa'                                              ,
                                                                          predicate_id   = 'b8dbb70e'                                             ),
                                                                       __(edge_id_source = __(source_type    = 'deterministic'                      ,
                                                                                             seed           = 'test:edge:class_contains_method')   ,
                                                                          edge_id        = '95e10d20'                                              ,
                                                                          from_node_id   = '02a4d1fa'                                              ,
                                                                          to_node_id     = '53b63bbe'                                              ,
                                                                          predicate_id   = 'b8dbb70e'                                             )])



    def test__create_graph__simple_class__nodes(self):                                     # Test graph nodes
        with self.test_data as _:
            graph = _.create_graph__simple_class()

            node_names = [str(n.name) for n in graph.nodes.values()]
            assert 'my_module'  in node_names
            assert 'MyClass'    in node_names
            assert 'my_method'  in node_names

            # Check node_type_ids match expected values
            module_type_id   = Node_Type_Id(Obj_Id.from_seed('test:node_type:module'))
            class_type_id    = Node_Type_Id(Obj_Id.from_seed('test:node_type:class'))
            method_type_id   = Node_Type_Id(Obj_Id.from_seed('test:node_type:method'))

            node_type_ids = [n.node_type_id for n in graph.nodes.values()]
            assert module_type_id in node_type_ids
            assert class_type_id  in node_type_ids
            assert method_type_id in node_type_ids

    def test__create_graph__simple_class__edges(self):                                     # Test graph edges
        with self.test_data as _:
            graph = _.create_graph__simple_class()

            assert len(graph.edges) == 2
            contains_id = Predicate_Id(Obj_Id.from_seed('test:predicate:contains'))
            predicates = [e.predicate_id for e in graph.edges]
            assert predicates == [contains_id, contains_id]                                # module→class, class→method

    def test__create_graph__empty(self):                                                   # Test empty graph
        with self.test_data as _:
            graph = _.create_graph__empty()

            assert type(graph)              is Schema__Semantic_Graph
            assert str(graph.ontology_id)   == ''                                          # Empty ontology_id
            assert str(graph.rule_set_id)   == ''                                          # Empty rule_set_id
            assert len(graph.nodes)         == 0
            assert len(graph.edges)         == 0
            assert graph.obj()              == __(graph_id_source = None             ,
                                                  graph_id        = 'b3f23601'       ,
                                                  ontology_id     = ''               ,
                                                  rule_set_id     = ''               ,
                                                  nodes           = __()             ,
                                                  edges           = []              )


    def test__create_graph__deterministic_id(self):                                        # Test deterministic graph ID
        with self.test_data as _:
            graph_1 = _.create_graph__simple_class()
            graph_2 = _.create_graph__simple_class()

            assert graph_1.graph_id == graph_2.graph_id                                    # Same seed → same ID
            assert graph_1.json()   == graph_2.json()
            assert graph_1.obj ()   == graph_2.obj ()

    # ═══════════════════════════════════════════════════════════════════════════
    # ID Helper Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__deterministic_node_id(self):                                                 # Test deterministic node ID helper
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed

        with self.test_data as _:
            node_id_1 = _.deterministic_node_id(Safe_Str__Id__Seed('test:same:seed'))
            node_id_2 = _.deterministic_node_id(Safe_Str__Id__Seed('test:same:seed'))
            node_id_3 = _.deterministic_node_id(Safe_Str__Id__Seed('test:different:seed'))

            assert type(node_id_1) is Node_Id
            assert node_id_1       == node_id_2                                            # Same seed → same ID
            assert node_id_1       != node_id_3                                            # Different seed → different ID

    def test__deterministic_edge_id(self):                                                 # Test deterministic edge ID helper
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed

        with self.test_data as _:
            edge_id_1 = _.deterministic_edge_id(Safe_Str__Id__Seed('test:edge:seed'))
            edge_id_2 = _.deterministic_edge_id(Safe_Str__Id__Seed('test:edge:seed'))

            assert type(edge_id_1) is Edge_Id
            assert edge_id_1       == edge_id_2                                            # Same seed → same ID

    def test__deterministic_graph_id(self):                                                # Test deterministic graph ID helper
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed

        with self.test_data as _:
            graph_id_1 = _.deterministic_graph_id(Safe_Str__Id__Seed('test:graph:seed'))
            graph_id_2 = _.deterministic_graph_id(Safe_Str__Id__Seed('test:graph:seed'))

            assert type(graph_id_1) is Graph_Id
            assert graph_id_1       == graph_id_2                                          # Same seed → same ID

    def test__deterministic_node_type_id(self):                                            # Test deterministic node type ID helper
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed

        with self.test_data as _:
            nt_id_1 = _.deterministic_node_type_id(Safe_Str__Id__Seed('test:nt:seed'))
            nt_id_2 = _.deterministic_node_type_id(Safe_Str__Id__Seed('test:nt:seed'))

            assert type(nt_id_1) is Node_Type_Id
            assert nt_id_1       == nt_id_2                                                # Same seed → same ID

    def test__deterministic_predicate_id(self):                                            # Test deterministic predicate ID helper
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed

        with self.test_data as _:
            pred_id_1 = _.deterministic_predicate_id(Safe_Str__Id__Seed('test:pred:seed'))
            pred_id_2 = _.deterministic_predicate_id(Safe_Str__Id__Seed('test:pred:seed'))

            assert type(pred_id_1) is Predicate_Id
            assert pred_id_1       == pred_id_2                                            # Same seed → same ID

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__all_test_data__is_consistent(self):                                          # Test data consistency
        with self.test_data as _:
            taxonomy = _.create_taxonomy__code_elements()
            ontology = _.create_ontology__code_structure()
            rule_set = _.create_rule_set__code_structure()
            graph    = _.create_graph__simple_class()

            assert ontology.taxonomy_id  == taxonomy.taxonomy_id               # Ontology refs taxonomy by ID
            assert rule_set.ontology_ref == ontology.ontology_ref              # Rules ref ontology (still by ref)
            assert graph.ontology_id     == ontology.ontology_id               # Graph refs ontology by ID

    def test__graph_nodes__have_valid_types(self):                                         # Graph node types in ontology
        with self.test_data as _:
            ontology = _.create_ontology__code_structure()
            graph    = _.create_graph__simple_class     ()

            ontology_type_ids = set(ontology.node_types.keys())
            graph_type_ids    = set(n.node_type_id for n in graph.nodes.values())

            assert graph_type_ids.issubset(ontology_type_ids)                              # All graph types in ontology

    def test__graph_edges__have_valid_predicates(self):                                    # Graph predicates in ontology
        with self.test_data as _:
            ontology = _.create_ontology__code_structure()
            graph    = _.create_graph__simple_class     ()

            ontology_pred_ids = set(ontology.predicates.keys())
            graph_pred_ids    = set(e.predicate_id for e in graph.edges)

            assert graph_pred_ids.issubset(ontology_pred_ids)                              # All graph predicates in ontology

    # ═══════════════════════════════════════════════════════════════════════════
    # Projected Schema Factory Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_projected_node(self):                                                   # Test projected node creation
        with self.test_data as _:
            node = _.create_projected_node(ref  = Node_Type_Ref('class'),
                                           name = Safe_Str__Id('MyClass'))

            assert type(node)      is Schema__Projected__Node
            assert str(node.ref)   == 'class'
            assert str(node.name)  == 'MyClass'
            assert node.obj()      == __(ref  = 'class'  ,
                                         name = 'MyClass')

    def test__create_projected_edge(self):                                                   # Test projected edge creation
        with self.test_data as _:
            edge = _.create_projected_edge(from_name = Safe_Str__Id('MyClass')    ,
                                           to_name   = Safe_Str__Id('my_method')  ,
                                           ref       = Predicate_Ref('contains')  )

            assert type(edge)          is Schema__Projected__Edge
            assert str(edge.from_name) == 'MyClass'
            assert str(edge.to_name)   == 'my_method'
            assert str(edge.ref)       == 'contains'
            assert edge.obj()          == __(from_name = 'MyClass'  ,
                                             to_name   = 'my_method',
                                             ref       = 'contains' )

    def test__create_projected_data(self):                                                   # Test projected data creation
        with self.test_data as _:
            nodes = List__Projected__Nodes()
            nodes.append(_.create_projected_node(ref  = Node_Type_Ref('class'),
                                                 name = Safe_Str__Id('MyClass')))

            edges = List__Projected__Edges()
            edges.append(_.create_projected_edge(from_name = Safe_Str__Id('MyClass')  ,
                                                 to_name   = Safe_Str__Id('my_method'),
                                                 ref       = Predicate_Ref('contains')))

            data = _.create_projected_data(nodes = nodes,
                                           edges = edges)

            assert type(data)        is Schema__Projected__Data
            assert type(data.nodes)  is List__Projected__Nodes
            assert type(data.edges)  is List__Projected__Edges
            assert len(data.nodes)   == 1
            assert len(data.edges)   == 1
            assert data.obj()        == __(nodes = [__(ref  = 'class'  ,
                                                       name = 'MyClass')],
                                           edges = [__(from_name = 'MyClass'  ,
                                                       to_name   = 'my_method',
                                                       ref       = 'contains' )])

    def test__create_projected_references(self):                                             # Test projected references creation
        with self.test_data as _:
            nodes_dict = Dict__Node_Type_Ids__By_Ref()
            nodes_dict[Node_Type_Ref('class')] = Node_Type_Id('abc12345')

            edges_dict = Dict__Predicate_Ids__By_Ref()
            edges_dict[Predicate_Ref('contains')] = Predicate_Id('def45678')

            refs = _.create_projected_references(nodes = nodes_dict,
                                                 edges = edges_dict)

            assert type(refs)        is Schema__Projected__References
            assert type(refs.nodes)  is Dict__Node_Type_Ids__By_Ref
            assert type(refs.edges)  is Dict__Predicate_Ids__By_Ref
            assert refs.nodes.get(Node_Type_Ref('class'))    == 'abc12345'
            assert refs.edges.get(Predicate_Ref('contains')) == 'def45678'

    def test__create_projected_sources(self):                                                # Test projected sources creation
        with self.test_data as _:
            sources = _.create_projected_sources(source_graph_id = Graph_Id('abc12345')                    ,
                                                 ontology_seed   = Safe_Str__Id__Seed('test:ontology:seed'))

            assert type(sources)                is Schema__Projected__Sources
            assert str(sources.source_graph_id) == 'abc12345'
            assert str(sources.ontology_seed)   == 'test:ontology:seed'
            assert type(sources.generated_at)   is Timestamp_Now

    def test__create_projected_sources__without_seed(self):                                  # Test sources without ontology seed
        with self.test_data as _:
            sources = _.create_projected_sources(source_graph_id = Graph_Id('abc12345'))

            assert str(sources.source_graph_id) == 'abc12345'
            assert sources.ontology_seed        is None

    def test__create_projected_semantic_graph(self):                                         # Test full projected graph creation
        with self.test_data as _:
            nodes = List__Projected__Nodes()
            nodes.append(_.create_projected_node(ref = Node_Type_Ref('class'), name = Safe_Str__Id('MyClass')))

            edges = List__Projected__Edges()

            projection = _.create_projected_data(nodes = nodes, edges = edges)

            nodes_dict = Dict__Node_Type_Ids__By_Ref()
            edges_dict = Dict__Predicate_Ids__By_Ref()
            references = _.create_projected_references(nodes = nodes_dict, edges = edges_dict)

            sources = _.create_projected_sources(source_graph_id = Graph_Id('abc12345'))

            projected_graph = _.create_projected_semantic_graph(projection = projection,
                                                                references = references,
                                                                sources    = sources   )

            assert type(projected_graph)            is Schema__Projected__Semantic_Graph
            assert type(projected_graph.projection) is Schema__Projected__Data
            assert type(projected_graph.references) is Schema__Projected__References
            assert type(projected_graph.sources)    is Schema__Projected__Sources
            assert len(projected_graph.projection.nodes) == 1
            assert len(projected_graph.projection.edges) == 0

            assert projected_graph.obj()                  == __(projection=__(nodes=[__(ref='class',
                                                                                        name='MyClass')],
                                                                              edges=[]),
                                                                references=__(nodes=__(), edges=__()),
                                                                sources=__(ontology_seed=None,
                                                                           source_graph_id='abc12345',
                                                                           generated_at=__SKIP__))

    # ═══════════════════════════════════════════════════════════════════════════
    # Projection Integration Setup Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_projection_test_setup(self):                                            # Test projection setup helper
        with self.test_data as _:
            registry, graph = _.create_projection_test_setup()

            assert type(registry)           is Ontology__Registry
            assert type(graph)              is Schema__Semantic_Graph
            assert len(graph.nodes)         == 3                                             # module, class, method
            assert len(graph.edges)         == 2                                             # two contains edges

            ontology = registry.get_by_id(graph.ontology_id)                                 # Registry has the ontology
            assert ontology                 is not None
            assert str(ontology.ontology_ref) == 'code_structure'

    def test__create_projection_test_setup__ontology_has_required_types(self):               # Setup has types for graph
        with self.test_data as _:
            registry, graph = _.create_projection_test_setup()
            ontology        = registry.get_by_id(graph.ontology_id)

            graph_type_ids    = set(n.node_type_id for n in graph.nodes.values())            # All graph node types exist in ontology
            ontology_type_ids = set(ontology.node_types.keys())
            assert graph_type_ids.issubset(ontology_type_ids)

            graph_pred_ids    = set(e.predicate_id for e in graph.edges)                     # All graph predicates exist in ontology
            ontology_pred_ids = set(ontology.predicates.keys())
            assert graph_pred_ids.issubset(ontology_pred_ids)

    def test__create_projected__simple_class__expected(self):                                # Test expected projection output
        with self.test_data as _:
            expected = _.create_projected__simple_class__expected()

            assert type(expected)       is Schema__Projected__Data
            assert len(expected.nodes)  == 3
            assert len(expected.edges)  == 2

            node_names = [str(n.name) for n in expected.nodes]                               # Check expected nodes
            assert 'my_module' in node_names
            assert 'MyClass'   in node_names
            assert 'my_method' in node_names

            edge_refs = [str(e.ref) for e in expected.edges]                                 # Check expected edges
            assert edge_refs == ['contains', 'contains']

    # ═══════════════════════════════════════════════════════════════════════════
    # Expected Output Constants Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__expected_projected_nodes_constant(self):                                       # Test nodes constant structure
        assert type(EXPECTED__PROJECTED__SIMPLE_CLASS__NODES) is list
        assert len(EXPECTED__PROJECTED__SIMPLE_CLASS__NODES)  == 3

        refs = [n['ref'] for n in EXPECTED__PROJECTED__SIMPLE_CLASS__NODES]
        assert 'module' in refs
        assert 'class'  in refs
        assert 'method' in refs

        names = [n['name'] for n in EXPECTED__PROJECTED__SIMPLE_CLASS__NODES]
        assert 'my_module' in names
        assert 'MyClass'   in names
        assert 'my_method' in names

    def test__expected_projected_edges_constant(self):                                       # Test edges constant structure
        assert type(EXPECTED__PROJECTED__SIMPLE_CLASS__EDGES) is list
        assert len(EXPECTED__PROJECTED__SIMPLE_CLASS__EDGES)  == 2

        for edge in EXPECTED__PROJECTED__SIMPLE_CLASS__EDGES:
            assert 'from_name' in edge
            assert 'to_name'   in edge
            assert 'ref'       in edge
            assert edge['ref'] == 'contains'

    def test__expected_projected_references_nodes_constant(self):                            # Test node refs constant
        assert type(EXPECTED__PROJECTED__SIMPLE_CLASS__REFERENCES__NODES) is dict
        assert 'module'   in EXPECTED__PROJECTED__SIMPLE_CLASS__REFERENCES__NODES
        assert 'class'    in EXPECTED__PROJECTED__SIMPLE_CLASS__REFERENCES__NODES
        assert 'method'   in EXPECTED__PROJECTED__SIMPLE_CLASS__REFERENCES__NODES
        assert 'function' in EXPECTED__PROJECTED__SIMPLE_CLASS__REFERENCES__NODES

    def test__expected_projected_references_edges_constant(self):                            # Test edge refs constant
        assert type(EXPECTED__PROJECTED__SIMPLE_CLASS__REFERENCES__EDGES) is dict
        assert 'contains'  in EXPECTED__PROJECTED__SIMPLE_CLASS__REFERENCES__EDGES
        assert 'in'        in EXPECTED__PROJECTED__SIMPLE_CLASS__REFERENCES__EDGES
        assert 'calls'     in EXPECTED__PROJECTED__SIMPLE_CLASS__REFERENCES__EDGES
        assert 'called_by' in EXPECTED__PROJECTED__SIMPLE_CLASS__REFERENCES__EDGES

    def test__expected_constants__match_factory_output(self):                                # Constants match factory methods
        with self.test_data as _:
            expected_data = _.create_projected__simple_class__expected()

            factory_nodes = [n.obj() for n in expected_data.nodes]                           # Compare nodes
            for expected_node in EXPECTED__PROJECTED__SIMPLE_CLASS__NODES:
                assert __(ref  = expected_node['ref' ],
                          name = expected_node['name']) in factory_nodes

            factory_edges = [e.obj() for e in expected_data.edges]                           # Compare edges
            for expected_edge in EXPECTED__PROJECTED__SIMPLE_CLASS__EDGES:
                assert __(from_name = expected_edge['from_name'],
                          to_name   = expected_edge['to_name'  ],
                          ref       = expected_edge['ref'      ]) in factory_edges


def find_fast_mode_marker():
    frame       = inspect.currentframe()
    previous_frames = list
    for _ in range(MAX_DEPTH):
        frame = frame.f_back
        if frame is None:
            return None

        # Check for original marker
        marker = frame.f_locals.get(TYPE_SAFE__FAST_MODE__VAR_NAME)
        if isinstance(marker, Type_Safe__Fast_Mode__Marker):

            for previous_frame in previous_frames:
                previous_frame[TYPE_SAFE__FAST_MODE__VAR_NAME] = marker     # Cache for ALL future walks
            return marker
        previous_frames.append(frame)                                       # keep track of all frames so far

    return None
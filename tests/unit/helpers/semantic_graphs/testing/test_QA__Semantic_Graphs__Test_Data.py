# ═══════════════════════════════════════════════════════════════════════════════
# Test QA__Semantic_Graphs__Test_Data - Tests for semantic graphs test data factory
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                              import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Ref       import Dict__Categories__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Ref       import Dict__Node_Types__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id             import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Refs            import List__Category_Refs
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Cardinality       import List__Rules__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Transitivity      import List__Rules__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges    import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type                import Enum__Id__Source_Type
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph              import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge        import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node        import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                   import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                  import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                    import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                    import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                    import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                 import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type      import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Relationship   import Schema__Ontology__Relationship
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                     import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality            import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity           import Schema__Rule__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy                 import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category       import Schema__Taxonomy__Category
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data            import QA__Semantic_Graphs__Test_Data
from osbot_utils.testing.__                                                                import __, __SKIP__
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                          import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                         import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                          import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                           import Obj_Id


class test_QA__Semantic_Graphs__Test_Data(TestCase):                                       # Test QA test data factory

    @classmethod
    def setUpClass(cls):                                                                   # Shared QA instance
        cls.qa = QA__Semantic_Graphs__Test_Data()

    def test__init__(self):                                                                # Test basic initialization
        with QA__Semantic_Graphs__Test_Data() as _:
            assert type(_) is QA__Semantic_Graphs__Test_Data

    # ═══════════════════════════════════════════════════════════════════════════
    # Taxonomy Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_category(self):                                                       # Test category creation
        with self.qa as _:
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
        with self.qa as _:
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
        with self.qa as _:
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
                                        description         = 'Code elements taxonomy'        ,
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
        with self.qa as _:
            taxonomy = _.create_taxonomy__code_elements()

            root = taxonomy.categories[Category_Ref('code_element')]
            assert len(root.child_refs) == 2

            code_unit = taxonomy.categories[Category_Ref('code_unit')]
            assert str(code_unit.parent_ref)      == 'code_element'
            assert len(code_unit.child_refs)      == 1
            assert str(code_unit.child_refs[0])   == 'callable'
            assert taxonomy.obj()                 == __(taxonomy_id_source = None                              ,
                                                        version            = '1.0.0'                           ,
                                                        taxonomy_id        = '5fb24b5a'                        ,
                                                        taxonomy_ref       = 'code_elements'                   ,
                                                        description        = 'Code elements taxonomy'          ,
                                                        root_category      = 'code_element'                    ,
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


    def test__create_taxonomy__minimal(self):                                              # Test minimal taxonomy
        with self.qa as _:
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
        with self.qa as _:
            taxonomy_1 = _.create_taxonomy__code_elements()
            taxonomy_2 = _.create_taxonomy__code_elements()

            assert taxonomy_1.taxonomy_id == taxonomy_2.taxonomy_id                        # Same seed → same ID
            assert taxonomy_1.obj()       == taxonomy_2.obj()
            assert taxonomy_1.json()      == taxonomy_2.json()

    # ═══════════════════════════════════════════════════════════════════════════
    # Ontology Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_relationship(self):                                                   # Test relationship creation
        from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Node_Type_Refs import List__Node_Type_Refs
        from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb import Safe_Str__Ontology__Verb

        targets = List__Node_Type_Refs([Node_Type_Ref('class'), Node_Type_Ref('method')])
        with self.qa as _:
            rel = _.create_relationship(inverse = Safe_Str__Ontology__Verb('contained_by'),
                                        targets = targets                                 )

            assert type(rel)         is Schema__Ontology__Relationship
            assert str(rel.inverse)  == 'contained_by'
            assert len(rel.targets)  == 2
            assert rel.obj()         == __(inverse = 'contained_by'     ,
                                           targets = ['class', 'method'])

    def test__create_node_type(self):                                                      # Test node type creation
        with self.qa as _:
            node_type = _.create_node_type(description  = 'Test node'                    ,
                                           taxonomy_ref = Category_Ref('container')      )

            assert type(node_type)              is Schema__Ontology__Node_Type
            assert str(node_type.description)   == 'Test node'
            assert str(node_type.taxonomy_ref)  == 'container'
            assert len(node_type.relationships) == 0
            assert node_type.obj()              == __(description   = 'Test node' ,
                                                      relationships = __()        ,
                                                      taxonomy_ref  = 'container' )

    def test__create_ontology__code_structure(self):                                       # Test code structure ontology
        with self.qa as _:
            ontology = _.create_ontology__code_structure()

            assert type(ontology)              is Schema__Ontology
            assert type(ontology.ontology_id)  is Ontology_Id
            assert ontology.ontology_ref       == 'code_structure'
            assert ontology.taxonomy_ref       == 'code_elements'
            assert type(ontology.node_types)   is Dict__Node_Types__By_Ref
            assert len(ontology.node_types)    == 4

            assert ontology.ontology_id        == str(Obj_Id.from_seed('test:ontology:code_structure'))
            node_type_refs = [str(k) for k in ontology.node_types.keys()]
            assert 'module'       in node_type_refs
            assert 'class'        in node_type_refs
            assert 'method'       in node_type_refs
            assert 'function'     in node_type_refs
            assert ontology.obj() == __(ontology_id_source = None                              ,
                                        version            = '1.0.0'                           ,
                                        ontology_id        = 'c6c846c6'                        ,
                                        ontology_ref       = 'code_structure'                  ,
                                        description        = 'Python code structure ontology'  ,
                                        taxonomy_ref       = 'code_elements'                   ,
                                        node_types         = __(module   = __(description   = 'Python module'         ,
                                                                              relationships = __(contains = __(inverse = 'in'        ,
                                                                                                               targets = ['class',
                                                                                                                          'method',
                                                                                                                          'function']) ),
                                                                              taxonomy_ref  = 'container'                  ),
                                                                _class   = __(description   = 'Python class'          ,
                                                                              relationships = __(contains = __(inverse = 'in'        ,
                                                                                                               targets = ['method']) ,
                                                                                                 _in      = __(inverse = 'contains'  ,
                                                                                                               targets = ['class', 'module']) ),
                                                                              taxonomy_ref  = 'container'                  ),
                                                                method   = __(description   = 'Class method'          ,
                                                                              relationships = __(_in   = __(inverse = 'contains'     ,
                                                                                                            targets = ['class', 'module']) ,
                                                                                                 calls = __(inverse = 'called_by'     ,
                                                                                                            targets = ['method', 'function']) ),
                                                                              taxonomy_ref  = 'callable'                  ),
                                                                function = __(description   = 'Standalone function'    ,
                                                                              relationships = __(_in   = __(inverse = 'contains'     ,
                                                                                                            targets = ['class', 'module']) ,
                                                                                                 calls = __(inverse = 'called_by'     ,
                                                                                                            targets = ['method', 'function']) ),
                                                                              taxonomy_ref  = 'callable'                  )))


    def test__create_ontology__code_structure__relationships(self):                        # Test ontology relationships
        with self.qa as _:
            ontology = _.create_ontology__code_structure()

            module_type = ontology.node_types[Node_Type_Ref('module')]
            assert 'contains' in [str(v) for v in module_type.relationships.keys()]

            method_type = ontology.node_types[Node_Type_Ref('method')]
            rel_verbs = [str(v) for v in method_type.relationships.keys()]
            assert 'in'           in rel_verbs
            assert 'calls'        in rel_verbs


    def test__create_ontology__minimal(self):                                              # Test minimal ontology
        with self.qa as _:
            ontology = _.create_ontology__minimal()

            assert type(ontology)             is Schema__Ontology
            assert str(ontology.ontology_ref) == 'minimal'
            assert len(ontology.node_types)   == 1
            assert Node_Type_Ref('entity')    in ontology.node_types
            assert ontology.obj()             == __(ontology_id_source = None                         ,
                                                    version            = '1.0.0'                      ,
                                                    ontology_id        = '33b3df6f'                   ,
                                                    ontology_ref       = 'minimal'                    ,
                                                    description        = 'Minimal test ontology'      ,
                                                    taxonomy_ref       = 'minimal'                    ,
                                                    node_types         = __(entity = __(description   = 'Generic entity' ,
                                                                                        relationships = __()             ,
                                                                                        taxonomy_ref  = 'root'           )))


    def test__create_ontology__deterministic_id(self):                                     # Test deterministic ontology ID
        with self.qa as _:
            ontology_1 = _.create_ontology__code_structure()
            ontology_2 = _.create_ontology__code_structure()

            assert ontology_1.ontology_id == ontology_2.ontology_id                        # Same seed → same ID
            assert ontology_1.json()      == ontology_2.json()
            assert ontology_1.obj()       == ontology_2.obj()

    # ═══════════════════════════════════════════════════════════════════════════
    # Rule Set Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_rule_set__code_structure(self):                                       # Test code structure rules
        with self.qa as _:
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

            assert rule_set.obj()                    == __(rule_set_id_source = None                                          ,
                                                           version             = '1.0.0'                                      ,
                                                           rule_set_id         = 'd01d41cc'                                   ,
                                                           rule_set_ref        = 'code_structure_rules'                       ,
                                                           ontology_ref        = 'code_structure'                             ,
                                                           description          = 'Code structure validation rules'            ,
                                                           transitivity_rules  = [__(source_type = 'method'                   ,
                                                                                     verb        = 'in'                       ,
                                                                                     target_type = 'module'                  )],
                                                           cardinality_rules   = [__(source_type  = 'method'                  ,
                                                                                     verb         = 'in'                      ,
                                                                                     target_type  = 'class'                   ,
                                                                                     min_targets  = 1                         ,
                                                                                     max_targets  = 1                         ,
                                                                                     description  = 'Method must be in exactly one class')])


    def test__create_rule_set__code_structure__transitivity(self):                         # Test transitivity rule
        with self.qa as _:
            rule_set = _.create_rule_set__code_structure()
            trans_rule = rule_set.transitivity_rules[0]

            assert type(trans_rule)            is Schema__Rule__Transitivity
            assert str(trans_rule.source_type) == 'method'
            assert str(trans_rule.verb)        == 'in'
            assert str(trans_rule.target_type) == 'module'

    def test__create_rule_set__code_structure__cardinality(self):                          # Test cardinality rule
        with self.qa as _:
            rule_set = _.create_rule_set__code_structure()
            card_rule = rule_set.cardinality_rules[0]

            assert type(card_rule)            is Schema__Rule__Cardinality
            assert str(card_rule.source_type) == 'method'
            assert str(card_rule.verb)        == 'in'
            assert str(card_rule.target_type) == 'class'
            assert int(card_rule.min_targets) == 1
            assert int(card_rule.max_targets) == 1

    def test__create_rule_set__empty(self):                                                # Test empty rule set
        with self.qa as _:
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
                                                           description           = 'Empty rule set for testing'    ,
                                                           transitivity_rules   = []                              ,
                                                           cardinality_rules    = []                              )


    def test__create_rule_set__deterministic_id(self):                                     # Test deterministic rule set ID
        with self.qa as _:
            rule_set_1 = _.create_rule_set__code_structure()
            rule_set_2 = _.create_rule_set__code_structure()

            assert rule_set_1.rule_set_id == rule_set_2.rule_set_id                        # Same seed → same ID
            assert rule_set_1.json()      == rule_set_2.json()
            assert rule_set_1.obj()       == rule_set_2.obj()

    # ═══════════════════════════════════════════════════════════════════════════
    # Graph Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_node(self):                                                           # Test node creation
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id

        with self.qa as _:
            seed = 'test:node:TestClass'
            node = _.create_node(node_type = Node_Type_Ref('class')        ,
                                 name      = Safe_Str__Id('TestClass')     ,
                                 seed      = Safe_Str__Id__Seed(seed))

            assert type(node)                      is Schema__Semantic_Graph__Node
            assert type(node.node_id)              is Node_Id
            assert node.node_type                  == 'class'
            assert node.name                       == 'TestClass'
            assert node.node_id                    == str(Obj_Id.from_seed(seed))
            assert node.node_id_source             is not None
            assert node.node_id_source.source_type == Enum__Id__Source_Type.DETERMINISTIC
            assert node.node_id_source.seed        == seed

            assert node.obj()                      == __(node_id_source=__(source_type = 'deterministic'       ,
                                                                           seed        = 'test:node:TestClass'),
                                                         node_id     = '30a65568',
                                                         node_type   = 'class',
                                                         name        = 'TestClass',
                                                         line_number = 0)

    def test__create_node__random_id(self):                                                # Test node with random ID
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id

        with self.qa as _:
            node = _.create_node(node_type = Node_Type_Ref('method')   ,
                                 name      = Safe_Str__Id('test_method'))

            assert type(node.node_id)  is Node_Id
            assert node.node_id_source is None                                             # No source for random ID
            assert node.obj()          == __(node_id_source = None         ,
                                             node_id         = __SKIP__     ,
                                             node_type       = 'method'     ,
                                             name            = 'test_method',
                                             line_number     = 0           )

            assert node.node_id        != 'd73c9318'

    def test__create_edge(self):                                                           # Test edge creation
        from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb import Safe_Str__Ontology__Verb
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed

        node__seed_1 = 'node1'
        node__seed_2 = 'node2'
        edge__seed_1 = 'test:edge:1_contains_2'

        node_id_1 = Node_Id(Obj_Id.from_seed(node__seed_1))
        node_id_2 = Node_Id(Obj_Id.from_seed(node__seed_2))

        with self.qa as _:
            edge = _.create_edge(from_node = node_id_1                                   ,
                                 verb      = Safe_Str__Ontology__Verb('contains')        ,
                                 to_node   = node_id_2                                   ,
                                 seed      = Safe_Str__Id__Seed(edge__seed_1))

            assert type(edge)                      is Schema__Semantic_Graph__Edge
            assert type(edge.edge_id)              is Edge_Id
            assert edge.from_node                  == node_id_1
            assert edge.verb                       == 'contains'
            assert edge.to_node                    == node_id_2
            assert edge.edge_id_source             is not None
            assert edge.edge_id_source.source_type == Enum__Id__Source_Type.DETERMINISTIC
            assert edge.edge_id                    == str(Obj_Id.from_seed(edge__seed_1))
            assert edge.from_node                  == str(Obj_Id.from_seed(node__seed_1))
            assert edge.to_node                    == str(Obj_Id.from_seed(node__seed_2))
            assert edge.obj()                      == __(edge_id_source = __(source_type = 'deterministic'        ,
                                                                             seed        = 'test:edge:1_contains_2'),
                                                          line_number     = 0                                       ,
                                                          edge_id         = 'e12d8dd1'                              ,
                                                          from_node       = 'ca12f31b'                              ,
                                                          verb            = 'contains'                              ,
                                                          to_node         = '15b18a72')                            != __()

    def test__create_graph__simple_class(self):                                            # Test simple class graph
        with self.qa as _:
            graph = _.create_graph__simple_class()

            assert type(graph)               is Schema__Semantic_Graph
            assert type(graph.graph_id)      is Graph_Id
            assert graph.ontology_ref        == 'code_structure'
            assert graph.rule_set_ref        == 'code_structure_rules'
            assert type(graph.nodes)         is Dict__Nodes__By_Id
            assert type(graph.edges)         is List__Semantic_Graph__Edges
            assert len(graph.nodes)          == 3
            assert len(graph.edges)          == 2
            assert graph.graph_id            == str(Obj_Id.from_seed('test:graph:simple_class'))
            assert graph.obj()               == __(graph_id_source = None                                ,
                                                   version          = '1.0.0'                             ,
                                                   graph_id         = 'c13f47de'                          ,
                                                   ontology_ref     = 'code_structure'                    ,
                                                   rule_set_ref     = 'code_structure_rules'              ,
                                                   nodes            = __(ff5bcf64  = __(node_id_source = __(source_type = 'deterministic'           ,
                                                                                                            seed        = 'test:node:my_module')    ,
                                                                                         node_id       = 'ff5bcf64'                                ,
                                                                                         node_type     = 'module'                                  ,
                                                                                         name          = 'my_module'                               ,
                                                                                         line_number   = 0                                         ),
                                                                          _02a4d1fa = __(node_id_source = __(source_type = 'deterministic'           ,
                                                                                                            seed        = 'test:node:MyClass')      ,
                                                                                         node_id       = '02a4d1fa'                                ,
                                                                                         node_type     = 'class'                                   ,
                                                                                         name          = 'MyClass'                                 ,
                                                                                         line_number   = 0                                         ),
                                                                          _53b63bbe = __(node_id_source = __(source_type = 'deterministic'           ,
                                                                                                            seed        = 'test:node:my_method')     ,
                                                                                         node_id       = '53b63bbe'                                ,
                                                                                         node_type     = 'method'                                  ,
                                                                                         name          = 'my_method'                               ,
                                                                                         line_number   = 10                                        )),
                                                   edges            = [__(edge_id_source = __(source_type = 'deterministic'                         ,
                                                                                             seed        = 'test:edge:module_contains_class')      ,
                                                                          line_number     = 0                                                     ,
                                                                          edge_id         = 'fa07486e'                                            ,
                                                                          from_node       = 'ff5bcf64'                                            ,
                                                                          verb            = 'contains'                                            ,
                                                                          to_node         = '02a4d1fa'                                           ),
                                                                       __(edge_id_source = __(source_type = 'deterministic'                         ,
                                                                                             seed        = 'test:edge:class_contains_method')      ,
                                                                          line_number     = 0                                                     ,
                                                                          edge_id         = '95e10d20'                                            ,
                                                                          from_node       = '02a4d1fa'                                            ,
                                                                          verb            = 'contains'                                            ,
                                                                          to_node         = '53b63bbe'                                           )])


    def test__create_graph__simple_class__nodes(self):                                     # Test graph nodes
        with self.qa as _:
            graph = _.create_graph__simple_class()

            node_names = [str(n.name) for n in graph.nodes.values()]
            assert 'my_module'  in node_names
            assert 'MyClass'    in node_names
            assert 'my_method'  in node_names

            node_types = [str(n.node_type) for n in graph.nodes.values()]
            assert 'module'  in node_types
            assert 'class'   in node_types
            assert 'method'  in node_types

    def test__create_graph__simple_class__edges(self):                                     # Test graph edges
        with self.qa as _:
            graph = _.create_graph__simple_class()

            assert len(graph.edges) == 2
            verbs = [str(e.verb) for e in graph.edges]
            assert verbs == ['contains', 'contains']                                       # module→class, class→method

    def test__create_graph__empty(self):                                                   # Test empty graph
        with self.qa as _:
            graph = _.create_graph__empty()

            assert type(graph)              is Schema__Semantic_Graph
            assert str(graph.ontology_ref)  == 'empty'
            assert str(graph.rule_set_ref)  == ''
            assert len(graph.nodes)         == 0
            assert len(graph.edges)         == 0
            assert graph.obj()              == __(graph_id_source = None             ,
                                                  version          = '1.0.0'         ,
                                                  graph_id         = 'b3f23601'      ,
                                                  ontology_ref     = 'empty'         ,
                                                  rule_set_ref     = ''              ,
                                                  nodes            = __()            ,
                                                  edges            = []             )


    def test__create_graph__deterministic_id(self):                                        # Test deterministic graph ID
        with self.qa as _:
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

        with self.qa as _:
            node_id_1 = _.deterministic_node_id(Safe_Str__Id__Seed('test:same:seed'))
            node_id_2 = _.deterministic_node_id(Safe_Str__Id__Seed('test:same:seed'))
            node_id_3 = _.deterministic_node_id(Safe_Str__Id__Seed('test:different:seed'))

            assert type(node_id_1) is Node_Id
            assert node_id_1       == node_id_2                                            # Same seed → same ID
            assert node_id_1       != node_id_3                                            # Different seed → different ID

    def test__deterministic_edge_id(self):                                                 # Test deterministic edge ID helper
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed

        with self.qa as _:
            edge_id_1 = _.deterministic_edge_id(Safe_Str__Id__Seed('test:edge:seed'))
            edge_id_2 = _.deterministic_edge_id(Safe_Str__Id__Seed('test:edge:seed'))

            assert type(edge_id_1) is Edge_Id
            assert edge_id_1       == edge_id_2                                            # Same seed → same ID

    def test__deterministic_graph_id(self):                                                # Test deterministic graph ID helper
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed

        with self.qa as _:
            graph_id_1 = _.deterministic_graph_id(Safe_Str__Id__Seed('test:graph:seed'))
            graph_id_2 = _.deterministic_graph_id(Safe_Str__Id__Seed('test:graph:seed'))

            assert type(graph_id_1) is Graph_Id
            assert graph_id_1       == graph_id_2                                          # Same seed → same ID

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__all_test_data__is_consistent(self):                                          # Test data consistency
        with self.qa as _:
            taxonomy = _.create_taxonomy__code_elements()
            ontology = _.create_ontology__code_structure()
            rule_set = _.create_rule_set__code_structure()
            graph    = _.create_graph__simple_class()

            assert ontology.taxonomy_ref == taxonomy.taxonomy_ref                # Ontology refs taxonomy
            assert rule_set.ontology_ref == ontology.ontology_ref                # Rules ref ontology
            assert graph.ontology_ref    == ontology.ontology_ref                # Graph refs ontology
            assert graph.rule_set_ref    == rule_set.rule_set_ref                # Graph refs rules

    def test__graph_nodes__have_valid_types(self):                                         # Graph node types in ontology
        with self.qa as _:
            ontology = _.create_ontology__code_structure()
            graph    = _.create_graph__simple_class     ()

            ontology_types = set(str(k) for k in ontology.node_types.keys())
            graph_types    = set(str(n.node_type) for n in graph.nodes.values())

            assert graph_types.issubset(ontology_types)                                    # All graph types in ontology
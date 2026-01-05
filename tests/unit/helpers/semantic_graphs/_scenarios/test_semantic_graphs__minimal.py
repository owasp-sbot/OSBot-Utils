# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic Graphs - Minimal Integration
#
# A minimal integration test to verify all core components work together:
#   - Taxonomy with simple hierarchy
#   - Ontology with node types, predicates, properties
#   - Rule set with validation rules
#   - Semantic graph with nodes and edges
#   - Cross-component validation
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


class test_semantic_graphs__minimal(TestCase):                                         # Minimal integration

    def test__full_stack__create_and_validate(self):                                   # Full creation and validation
        # ═══════════════════════════════════════════════════════════════════════
        # Step 1: Create Taxonomy
        # ═══════════════════════════════════════════════════════════════════════
        cat_root_id  = Category_Id(Obj_Id.from_seed('min:cat:root'))
        cat_item_id  = Category_Id(Obj_Id.from_seed('min:cat:item'))

        categories = Dict__Categories__By_Id()
        categories[cat_root_id] = Schema__Taxonomy__Category(
            category_id  = cat_root_id                                                  ,
            category_ref = Category_Ref('entity')                                       ,
            parent_id    = None                                                         ,
            child_ids    = List__Category_Ids([cat_item_id])
        )
        categories[cat_item_id] = Schema__Taxonomy__Category(
            category_id  = cat_item_id                                                  ,
            category_ref = Category_Ref('item')                                         ,
            parent_id    = cat_root_id                                                  ,
            child_ids    = List__Category_Ids()
        )

        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('min:taxonomy'))
        taxonomy = Schema__Taxonomy(
            taxonomy_id  = taxonomy_id                                                  ,
            taxonomy_ref = Taxonomy_Ref('minimal')                                      ,
            root_id      = cat_root_id                                                  ,
            categories   = categories
        )

        # ═══════════════════════════════════════════════════════════════════════
        # Step 2: Create Ontology
        # ═══════════════════════════════════════════════════════════════════════
        nt_parent_id = Node_Type_Id(Obj_Id.from_seed('min:nt:parent'))
        nt_child_id  = Node_Type_Id(Obj_Id.from_seed('min:nt:child'))
        pred_has_id  = Predicate_Id(Obj_Id.from_seed('min:pred:has'))
        pt_str_id    = Property_Type_Id(Obj_Id.from_seed('min:pt:str'))
        pn_name_id   = Property_Name_Id(Obj_Id.from_seed('min:pn:name'))

        node_types = Dict__Node_Types__By_Id()
        node_types[nt_parent_id] = Schema__Ontology__Node_Type(
            node_type_id  = nt_parent_id                                                ,
            node_type_ref = Node_Type_Ref('parent')                                     ,
            category_id   = cat_item_id
        )
        node_types[nt_child_id] = Schema__Ontology__Node_Type(
            node_type_id  = nt_child_id                                                 ,
            node_type_ref = Node_Type_Ref('child')                                      ,
            category_id   = cat_item_id
        )

        predicates = Dict__Predicates__By_Id()
        predicates[pred_has_id] = Schema__Ontology__Predicate(
            predicate_id  = pred_has_id                                                 ,
            predicate_ref = Predicate_Ref('has')                                        ,
            inverse_id    = None
        )

        property_types = Dict__Property_Types__By_Id()
        property_types[pt_str_id] = Schema__Ontology__Property_Type(
            property_type_id  = pt_str_id                                               ,
            property_type_ref = Property_Type_Ref('string')
        )

        property_names = Dict__Property_Names__By_Id()
        property_names[pn_name_id] = Schema__Ontology__Property_Name(
            property_name_id  = pn_name_id                                              ,
            property_name_ref = Property_Name_Ref('name')                               ,
            property_type_id  = pt_str_id
        )

        edge_rules = List__Edge_Rules()
        edge_rules.append(Schema__Ontology__Edge_Rule(
            source_type_id = nt_parent_id                                               ,
            predicate_id   = pred_has_id                                                ,
            target_type_id = nt_child_id
        ))

        ontology_id = Ontology_Id(Obj_Id.from_seed('min:ontology'))
        ontology = Schema__Ontology(
            ontology_id    = ontology_id                                                ,
            ontology_ref   = Ontology_Ref('minimal')                                    ,
            taxonomy_id    = taxonomy_id                                                ,
            node_types     = node_types                                                 ,
            predicates     = predicates                                                 ,
            property_types = property_types                                             ,
            property_names = property_names                                             ,
            edge_rules     = edge_rules
        )

        # ═══════════════════════════════════════════════════════════════════════
        # Step 3: Create Rule Set
        # ═══════════════════════════════════════════════════════════════════════
        required_props = List__Rules__Required_Node_Property()
        required_props.append(Schema__Rule__Required_Node_Property(
            node_type_id     = nt_parent_id                                             ,
            property_name_id = pn_name_id                                               ,
            required         = True
        ))

        rule_set_id = Rule_Set_Id(Obj_Id.from_seed('min:rules'))
        rule_set = Schema__Rule_Set(
            rule_set_id              = rule_set_id                                      ,
            rule_set_ref             = Rule_Set_Ref('minimal_rules')                    ,
            ontology_id              = ontology_id                                      ,
            required_node_properties = required_props
        )

        # ═══════════════════════════════════════════════════════════════════════
        # Step 4: Create Graph
        # ═══════════════════════════════════════════════════════════════════════
        node_p_id = Node_Id(Obj_Id.from_seed('min:node:parent'))
        node_c_id = Node_Id(Obj_Id.from_seed('min:node:child'))

        nodes = Dict__Nodes__By_Id()
        nodes[node_p_id] = Schema__Semantic_Graph__Node(
            node_id      = node_p_id                                                    ,
            node_type_id = nt_parent_id                                                 ,
            name        = 'Parent Node'
        )
        nodes[node_c_id] = Schema__Semantic_Graph__Node(
            node_id      = node_c_id                                                    ,
            node_type_id = nt_child_id                                                  ,
            name        = 'Child Node'
        )

        edges = List__Semantic_Graph__Edges()
        edges.append(Schema__Semantic_Graph__Edge(
            from_node_id    = node_p_id                                                    ,
            predicate_id = pred_has_id                                                  ,
            to_node_id    = node_c_id
        ))

        graph_id = Graph_Id(Obj_Id.from_seed('min:graph'))
        graph = Schema__Semantic_Graph(
            graph_id    = graph_id                                                      ,
            ontology_id = ontology_id                                                   ,
            nodes       = nodes                                                         ,
            edges       = edges
        )

        # ═══════════════════════════════════════════════════════════════════════
        # Step 5: Validate with Utils
        # ═══════════════════════════════════════════════════════════════════════
        tax_utils = Taxonomy__Utils()
        ont_utils = Ontology__Utils()
        rule_utils = Rule_Set__Utils()

        # Taxonomy validation
        root = tax_utils.get_root_category(taxonomy)
        assert root.category_id == cat_root_id
        assert tax_utils.has_category(taxonomy, cat_item_id)
        assert tax_utils.get_parent(taxonomy, cat_item_id).category_id == cat_root_id

        # Ontology validation
        assert ont_utils.has_node_type(ontology, nt_parent_id)
        assert ont_utils.has_predicate(ontology, pred_has_id)
        assert ont_utils.is_valid_edge(ontology, nt_parent_id, pred_has_id, nt_child_id)
        assert not ont_utils.is_valid_edge(ontology, nt_child_id, pred_has_id, nt_parent_id)

        # Property validation
        name_prop = ont_utils.get_property_name(ontology, pn_name_id)
        assert name_prop.property_type_id == pt_str_id

        # Rule validation
        assert rule_utils.has_required_node_property_rule(rule_set, nt_parent_id, pn_name_id)
        assert rule_utils.is_node_property_required(rule_set, nt_parent_id, pn_name_id)
        assert not rule_utils.has_required_node_property_rule(rule_set, nt_child_id, pn_name_id)

        # Graph validation
        assert len(graph.nodes) == 2
        assert len(graph.edges) == 1
        assert graph.edges[0].from_node_id == node_p_id
        assert graph.edges[0].to_node_id == node_c_id

        # Cross-component: node type → category → taxonomy
        parent_type = ont_utils.get_node_type(ontology, nt_parent_id)
        item_cat = tax_utils.get_category(taxonomy, parent_type.category_id)
        assert str(item_cat.category_ref) == 'item'

    def test__id_determinism(self):                                                    # Verify ID determinism
        # Same seed produces same ID
        id1 = Obj_Id.from_seed('test:determinism')
        id2 = Obj_Id.from_seed('test:determinism')
        assert str(id1) == str(id2)

        # Different seed produces different ID
        id3 = Obj_Id.from_seed('test:different')
        assert str(id1) != str(id3)

    def test__type_safety(self):                                                       # Verify type safety
        # Category_Id and Node_Type_Id are distinct types
        cat_id = Category_Id(Obj_Id.from_seed('test:cat'))
        nt_id  = Node_Type_Id(Obj_Id.from_seed('test:cat'))  # Same seed

        # Same underlying value but different types
        assert str(cat_id) == str(nt_id)
        assert type(cat_id) is Category_Id
        assert type(nt_id) is Node_Type_Id
        assert type(cat_id) is not type(nt_id)

    def test__json_roundtrip(self):                                                    # Verify JSON serialization
        # Create a simple taxonomy
        cat_id = Category_Id(Obj_Id.from_seed('json:cat'))
        categories = Dict__Categories__By_Id()
        categories[cat_id] = Schema__Taxonomy__Category(
            category_id  = cat_id                                                       ,
            category_ref = Category_Ref('test')                                         ,
            parent_id    = None                                                         ,
            child_ids    = List__Category_Ids()
        )

        taxonomy = Schema__Taxonomy(
            taxonomy_id  = Taxonomy_Id(Obj_Id.from_seed('json:tax'))                    ,
            taxonomy_ref = Taxonomy_Ref('json_test')                                    ,
            root_id      = cat_id                                                       ,
            categories   = categories
        )

        # Serialize and deserialize
        json_data = taxonomy.json()
        restored = Schema__Taxonomy.from_json(json_data)

        # Verify
        assert str(restored.taxonomy_id) == str(taxonomy.taxonomy_id)
        assert str(restored.taxonomy_ref) == str(taxonomy.taxonomy_ref)
        assert str(restored.root_id) == str(taxonomy.root_id)
        assert len(restored.categories) == len(taxonomy.categories)
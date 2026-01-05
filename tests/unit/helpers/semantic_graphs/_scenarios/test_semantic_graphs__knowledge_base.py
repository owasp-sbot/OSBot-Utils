# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic Graphs - Knowledge Base Scenario
#
# Demonstrates semantic graphs for a knowledge base / wiki:
#   - Taxonomy: content → article, concept, reference
#   - Ontology: topic, article, author, tag with relationships
#   - Rules: articles must have author, concepts need definitions
#   - Graph: interconnected knowledge articles
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                   import TestCase

from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Registry import Ontology__Registry
from osbot_utils.helpers.semantic_graphs.projector.Semantic_Graph__Projector import Semantic_Graph__Projector
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
from osbot_utils.helpers.semantic_graphs.taxonomy.Taxonomy__Registry import Taxonomy__Registry
from osbot_utils.helpers.semantic_graphs.taxonomy.Taxonomy__Utils                               import Taxonomy__Utils
from osbot_utils.helpers.semantic_graphs.rule.Rule_Set__Utils                                   import Rule_Set__Utils
from osbot_utils.testing.Graph__Deterministic__Ids import graph_deterministic_ids
from osbot_utils.testing.__ import __, __SKIP__
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                import Obj_Id


class test_semantic_graphs__knowledge_base(TestCase):                                  # Knowledge base scenario

    @classmethod
    def setUpClass(cls):                                                               # Build complete knowledge model
        cls.build_taxonomy()
        cls.build_ontology()
        cls.build_rule_set()
        cls.build_graph()
        cls.build_projection()

    # ═══════════════════════════════════════════════════════════════════════════
    # Model Construction
    # ═══════════════════════════════════════════════════════════════════════════

    @classmethod
    def build_taxonomy(cls):                                                           # Create content taxonomy
        # Category IDs
        cls.cat_root_id      = Category_Id(Obj_Id.from_seed('kb:cat:root'))
        cls.cat_content_id   = Category_Id(Obj_Id.from_seed('kb:cat:content'))
        cls.cat_metadata_id  = Category_Id(Obj_Id.from_seed('kb:cat:metadata'))
        cls.cat_entity_id    = Category_Id(Obj_Id.from_seed('kb:cat:entity'))

        # Build hierarchy
        cat_root = Schema__Taxonomy__Category(
            category_id  = cls.cat_root_id                                              ,
            category_ref = Category_Ref('knowledge')                                    ,
            parent_id    = None                                                         ,
            child_ids    = List__Category_Ids([cls.cat_content_id, cls.cat_metadata_id, cls.cat_entity_id])
        )
        cat_content = Schema__Taxonomy__Category(
            category_id  = cls.cat_content_id                                           ,
            category_ref = Category_Ref('content')                                      ,
            parent_id    = cls.cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )
        cat_metadata = Schema__Taxonomy__Category(
            category_id  = cls.cat_metadata_id                                          ,
            category_ref = Category_Ref('metadata')                                     ,
            parent_id    = cls.cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )
        cat_entity = Schema__Taxonomy__Category(
            category_id  = cls.cat_entity_id                                            ,
            category_ref = Category_Ref('entity')                                       ,
            parent_id    = cls.cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )

        categories = Dict__Categories__By_Id()
        categories[cls.cat_root_id]     = cat_root
        categories[cls.cat_content_id]  = cat_content
        categories[cls.cat_metadata_id] = cat_metadata
        categories[cls.cat_entity_id]   = cat_entity

        cls.taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('kb:taxonomy'))
        cls.taxonomy = Schema__Taxonomy(
            taxonomy_id  = cls.taxonomy_id                                              ,
            taxonomy_ref = Taxonomy_Ref('knowledge_base')                               ,
            root_id      = cls.cat_root_id                                              ,
            categories   = categories
        )

    @classmethod
    def build_ontology(cls):                                                           # Create knowledge base ontology
        # Node Type IDs
        cls.nt_topic_id   = Node_Type_Id(Obj_Id.from_seed('kb:nt:topic'))
        cls.nt_article_id = Node_Type_Id(Obj_Id.from_seed('kb:nt:article'))
        cls.nt_concept_id = Node_Type_Id(Obj_Id.from_seed('kb:nt:concept'))
        cls.nt_author_id  = Node_Type_Id(Obj_Id.from_seed('kb:nt:author'))
        cls.nt_tag_id     = Node_Type_Id(Obj_Id.from_seed('kb:nt:tag'))

        # Predicate IDs
        cls.pred_contains_id    = Predicate_Id(Obj_Id.from_seed('kb:pred:contains'))
        cls.pred_in_id          = Predicate_Id(Obj_Id.from_seed('kb:pred:in'))
        cls.pred_references_id  = Predicate_Id(Obj_Id.from_seed('kb:pred:references'))
        cls.pred_written_by_id  = Predicate_Id(Obj_Id.from_seed('kb:pred:written_by'))
        cls.pred_authored_id    = Predicate_Id(Obj_Id.from_seed('kb:pred:authored'))
        cls.pred_tagged_with_id = Predicate_Id(Obj_Id.from_seed('kb:pred:tagged_with'))
        cls.pred_defines_id     = Predicate_Id(Obj_Id.from_seed('kb:pred:defines'))
        cls.pred_related_to_id  = Predicate_Id(Obj_Id.from_seed('kb:pred:related_to'))

        # Property Type IDs
        cls.pt_string_id   = Property_Type_Id(Obj_Id.from_seed('kb:pt:string'))
        cls.pt_datetime_id = Property_Type_Id(Obj_Id.from_seed('kb:pt:datetime'))
        cls.pt_url_id      = Property_Type_Id(Obj_Id.from_seed('kb:pt:url'))

        # Property Name IDs
        cls.pn_title_id       = Property_Name_Id(Obj_Id.from_seed('kb:pn:title'))
        cls.pn_created_at_id  = Property_Name_Id(Obj_Id.from_seed('kb:pn:created_at'))
        cls.pn_updated_at_id  = Property_Name_Id(Obj_Id.from_seed('kb:pn:updated_at'))
        cls.pn_definition_id  = Property_Name_Id(Obj_Id.from_seed('kb:pn:definition'))
        cls.pn_url_id         = Property_Name_Id(Obj_Id.from_seed('kb:pn:url'))

        # Node Types
        node_types = Dict__Node_Types__By_Id()
        node_types[cls.nt_topic_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_topic_id                                             ,
            node_type_ref = Node_Type_Ref('topic')                                      ,
            category_id   = cls.cat_content_id
        )
        node_types[cls.nt_article_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_article_id                                           ,
            node_type_ref = Node_Type_Ref('article')                                    ,
            category_id   = cls.cat_content_id
        )
        node_types[cls.nt_concept_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_concept_id                                           ,
            node_type_ref = Node_Type_Ref('concept')                                    ,
            category_id   = cls.cat_content_id
        )
        node_types[cls.nt_author_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_author_id                                            ,
            node_type_ref = Node_Type_Ref('author')                                     ,
            category_id   = cls.cat_entity_id
        )
        node_types[cls.nt_tag_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_tag_id                                               ,
            node_type_ref = Node_Type_Ref('tag')                                        ,
            category_id   = cls.cat_metadata_id
        )

        # Predicates (with inverses where applicable)
        predicates = Dict__Predicates__By_Id()
        predicates[cls.pred_contains_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_contains_id                                        ,
            predicate_ref = Predicate_Ref('contains')                                   ,
            inverse_id    = cls.pred_in_id
        )
        predicates[cls.pred_in_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_in_id                                              ,
            predicate_ref = Predicate_Ref('in')                                         ,
            inverse_id    = cls.pred_contains_id
        )
        predicates[cls.pred_references_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_references_id                                      ,
            predicate_ref = Predicate_Ref('references')                                 ,
            inverse_id    = None
        )
        predicates[cls.pred_written_by_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_written_by_id                                      ,
            predicate_ref = Predicate_Ref('written_by')                                 ,
            inverse_id    = cls.pred_authored_id
        )
        predicates[cls.pred_authored_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_authored_id                                        ,
            predicate_ref = Predicate_Ref('authored')                                   ,
            inverse_id    = cls.pred_written_by_id
        )
        predicates[cls.pred_tagged_with_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_tagged_with_id                                     ,
            predicate_ref = Predicate_Ref('tagged_with')                                ,
            inverse_id    = None
        )
        predicates[cls.pred_defines_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_defines_id                                         ,
            predicate_ref = Predicate_Ref('defines')                                    ,
            inverse_id    = None
        )
        predicates[cls.pred_related_to_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_related_to_id                                      ,
            predicate_ref = Predicate_Ref('related_to')                                 ,
            inverse_id    = cls.pred_related_to_id                                      # symmetric
        )

        # Property Types
        property_types = Dict__Property_Types__By_Id()
        property_types[cls.pt_string_id] = Schema__Ontology__Property_Type(
            property_type_id  = cls.pt_string_id                                        ,
            property_type_ref = Property_Type_Ref('string')
        )
        property_types[cls.pt_datetime_id] = Schema__Ontology__Property_Type(
            property_type_id  = cls.pt_datetime_id                                      ,
            property_type_ref = Property_Type_Ref('datetime')
        )
        property_types[cls.pt_url_id] = Schema__Ontology__Property_Type(
            property_type_id  = cls.pt_url_id                                           ,
            property_type_ref = Property_Type_Ref('url')
        )

        # Property Names
        property_names = Dict__Property_Names__By_Id()
        property_names[cls.pn_title_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_title_id                                         ,
            property_name_ref = Property_Name_Ref('title')                              ,
            property_type_id  = cls.pt_string_id
        )
        property_names[cls.pn_created_at_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_created_at_id                                    ,
            property_name_ref = Property_Name_Ref('created_at')                         ,
            property_type_id  = cls.pt_datetime_id
        )
        property_names[cls.pn_updated_at_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_updated_at_id                                    ,
            property_name_ref = Property_Name_Ref('updated_at')                         ,
            property_type_id  = cls.pt_datetime_id
        )
        property_names[cls.pn_definition_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_definition_id                                    ,
            property_name_ref = Property_Name_Ref('definition')                         ,
            property_type_id  = cls.pt_string_id
        )
        property_names[cls.pn_url_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_url_id                                           ,
            property_name_ref = Property_Name_Ref('url')                                ,
            property_type_id  = cls.pt_url_id
        )

        # Edge Rules
        edge_rules = List__Edge_Rules()
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_topic_id,   predicate_id=cls.pred_contains_id,    target_type_id=cls.nt_article_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_article_id, predicate_id=cls.pred_references_id,  target_type_id=cls.nt_article_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_article_id, predicate_id=cls.pred_written_by_id,  target_type_id=cls.nt_author_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_article_id, predicate_id=cls.pred_tagged_with_id, target_type_id=cls.nt_tag_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_article_id, predicate_id=cls.pred_defines_id,     target_type_id=cls.nt_concept_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_concept_id, predicate_id=cls.pred_related_to_id,  target_type_id=cls.nt_concept_id))

        cls.ontology_id = Ontology_Id(Obj_Id.from_seed('kb:ontology'))
        cls.ontology = Schema__Ontology(
            ontology_id    = cls.ontology_id                                            ,
            ontology_ref   = Ontology_Ref('knowledge_base')                             ,
            taxonomy_id    = cls.taxonomy_id                                            ,
            node_types     = node_types                                                 ,
            predicates     = predicates                                                 ,
            property_types = property_types                                             ,
            property_names = property_names                                             ,
            edge_rules     = edge_rules
        )

    @classmethod
    def build_rule_set(cls):                                                           # Create validation rules
        required_node_properties = List__Rules__Required_Node_Property()
        required_node_properties.append(Schema__Rule__Required_Node_Property(
            node_type_id     = cls.nt_article_id                                        ,
            property_name_id = cls.pn_title_id                                          ,
            required         = True
        ))
        required_node_properties.append(Schema__Rule__Required_Node_Property(
            node_type_id     = cls.nt_article_id                                        ,
            property_name_id = cls.pn_created_at_id                                     ,
            required         = True
        ))
        required_node_properties.append(Schema__Rule__Required_Node_Property(
            node_type_id     = cls.nt_concept_id                                        ,
            property_name_id = cls.pn_definition_id                                     ,
            required         = True
        ))

        cls.rule_set_id = Rule_Set_Id(Obj_Id.from_seed('kb:rules'))
        cls.rule_set = Schema__Rule_Set(
            rule_set_id              = cls.rule_set_id                                  ,
            rule_set_ref             = Rule_Set_Ref('kb_validation')                    ,
            ontology_id              = cls.ontology_id                                  ,
            required_node_properties = required_node_properties
        )

    @classmethod
    def build_graph(cls):                                                              # Create sample knowledge graph
        # Node IDs
        cls.node_topic_ml_id      = Node_Id(Obj_Id.from_seed('kb:node:topic_ml'))
        cls.node_art_neural_id    = Node_Id(Obj_Id.from_seed('kb:node:art_neural'))
        cls.node_art_gradient_id  = Node_Id(Obj_Id.from_seed('kb:node:art_gradient'))
        cls.node_art_backprop_id  = Node_Id(Obj_Id.from_seed('kb:node:art_backprop'))
        cls.node_concept_nn_id    = Node_Id(Obj_Id.from_seed('kb:node:concept_nn'))
        cls.node_concept_grad_id  = Node_Id(Obj_Id.from_seed('kb:node:concept_grad'))
        cls.node_author1_id       = Node_Id(Obj_Id.from_seed('kb:node:author1'))
        cls.node_author2_id       = Node_Id(Obj_Id.from_seed('kb:node:author2'))
        cls.node_tag_ml_id        = Node_Id(Obj_Id.from_seed('kb:node:tag_ml'))
        cls.node_tag_dl_id        = Node_Id(Obj_Id.from_seed('kb:node:tag_dl'))

        # Nodes
        nodes = Dict__Nodes__By_Id()
        nodes[cls.node_topic_ml_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_topic_ml_id                                         ,
            node_type_id = cls.nt_topic_id                                              ,
            name         = 'Machine Learning'
        )
        nodes[cls.node_art_neural_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_art_neural_id                                       ,
            node_type_id = cls.nt_article_id                                            ,
            name         = 'Introduction to Neural Networks'
        )
        nodes[cls.node_art_gradient_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_art_gradient_id                                     ,
            node_type_id = cls.nt_article_id                                            ,
            name         = 'Understanding Gradient Descent'
        )
        nodes[cls.node_art_backprop_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_art_backprop_id                                     ,
            node_type_id = cls.nt_article_id                                            ,
            name         = 'Backpropagation Explained'
        )
        nodes[cls.node_concept_nn_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_concept_nn_id                                       ,
            node_type_id = cls.nt_concept_id                                            ,
            name         = 'Neural Network'
        )
        nodes[cls.node_concept_grad_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_concept_grad_id                                     ,
            node_type_id = cls.nt_concept_id                                            ,
            name         = 'Gradient'
        )
        nodes[cls.node_author1_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_author1_id                                          ,
            node_type_id = cls.nt_author_id                                             ,
            name         = 'Dr. Sarah Chen'
        )
        nodes[cls.node_author2_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_author2_id                                          ,
            node_type_id = cls.nt_author_id                                             ,
            name         = 'Prof. Alex Kumar'
        )
        nodes[cls.node_tag_ml_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_tag_ml_id                                           ,
            node_type_id = cls.nt_tag_id                                                ,
            name         = 'machine-learning'
        )
        nodes[cls.node_tag_dl_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_tag_dl_id                                           ,
            node_type_id = cls.nt_tag_id                                                ,
            name         = 'deep-learning'
        )

        # Edges
        edges = List__Semantic_Graph__Edges()
        # Topic contains articles
        with graph_deterministic_ids():
            edges.append(Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node_id=cls.node_topic_ml_id,     predicate_id=cls.pred_contains_id,    to_node_id=cls.node_art_neural_id))
            edges.append(Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node_id=cls.node_topic_ml_id,     predicate_id=cls.pred_contains_id,    to_node_id=cls.node_art_gradient_id))
            edges.append(Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node_id=cls.node_topic_ml_id,     predicate_id=cls.pred_contains_id,    to_node_id=cls.node_art_backprop_id))
            # Article references
            edges.append(Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node_id=cls.node_art_backprop_id, predicate_id=cls.pred_references_id,  to_node_id=cls.node_art_neural_id))
            edges.append(Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node_id=cls.node_art_backprop_id, predicate_id=cls.pred_references_id,  to_node_id=cls.node_art_gradient_id))
            # Authorship
            edges.append(Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node_id=cls.node_art_neural_id,   predicate_id=cls.pred_written_by_id,  to_node_id=cls.node_author1_id))
            edges.append(Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node_id=cls.node_art_gradient_id, predicate_id=cls.pred_written_by_id,  to_node_id=cls.node_author2_id))
            edges.append(Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node_id=cls.node_art_backprop_id, predicate_id=cls.pred_written_by_id,  to_node_id=cls.node_author1_id))
            # Tags
            edges.append(Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node_id=cls.node_art_neural_id,   predicate_id=cls.pred_tagged_with_id, to_node_id=cls.node_tag_dl_id))
            edges.append(Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node_id=cls.node_art_gradient_id, predicate_id=cls.pred_tagged_with_id, to_node_id=cls.node_tag_ml_id))
            edges.append(Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node_id=cls.node_art_backprop_id, predicate_id=cls.pred_tagged_with_id, to_node_id=cls.node_tag_dl_id))
            # Concept definitions
            edges.append(Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node_id=cls.node_art_neural_id,   predicate_id=cls.pred_defines_id,     to_node_id=cls.node_concept_nn_id))
            edges.append(Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node_id=cls.node_art_gradient_id, predicate_id=cls.pred_defines_id,     to_node_id=cls.node_concept_grad_id))
            # Related concepts
            edges.append(Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node_id=cls.node_concept_nn_id,   predicate_id=cls.pred_related_to_id,  to_node_id=cls.node_concept_grad_id))

        cls.graph_id = Graph_Id(Obj_Id.from_seed('kb:graph'))
        cls.graph = Schema__Semantic_Graph(
            graph_id    = cls.graph_id                                                  ,
            ontology_id = cls.ontology_id                                               ,
            nodes       = nodes                                                         ,
            edges       = edges
        )

    @classmethod
    def build_projection(cls):
        cls.ontology_registry = Ontology__Registry()
        cls.taxonomy_registry = Taxonomy__Registry()
        cls.ontology_registry.register(ontology = cls.ontology)
        cls.taxonomy_registry.register(taxonomy = cls.taxonomy)
        cls.projector = Semantic_Graph__Projector(ontology_registry = cls.ontology_registry,
                                                  taxonomy_registry = cls.taxonomy_registry)
        cls.projection = cls.projector.project(cls.graph)
    # ═══════════════════════════════════════════════════════════════════════════
    # Graph Query Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__graph__find_articles_in_topic(self):                                     # Find all articles in a topic
        topic_edges = [e for e in self.graph.edges
                       if e.from_node_id == self.node_topic_ml_id
                       and e.predicate_id == self.pred_contains_id]

        article_ids = [e.to_node_id for e in topic_edges]
        assert len(article_ids) == 3
        assert self.node_art_neural_id in article_ids
        assert self.node_art_gradient_id in article_ids
        assert self.node_art_backprop_id in article_ids

    def test__graph__find_articles_by_author(self):                                    # Find all articles by an author
        author1_articles = [e.from_node_id for e in self.graph.edges
                            if e.predicate_id == self.pred_written_by_id
                            and e.to_node_id == self.node_author1_id]

        assert len(author1_articles) == 2  # Dr. Chen wrote 2 articles
        assert self.node_art_neural_id in author1_articles
        assert self.node_art_backprop_id in author1_articles

    def test__graph__find_article_references(self):                                    # Find articles referenced by another
        backprop_refs = [e.to_node_id for e in self.graph.edges
                         if e.from_node_id == self.node_art_backprop_id
                         and e.predicate_id == self.pred_references_id]

        assert len(backprop_refs) == 2
        assert self.node_art_neural_id in backprop_refs
        assert self.node_art_gradient_id in backprop_refs

    def test__graph__find_articles_by_tag(self):                                       # Find articles with a tag
        dl_tagged = [e.from_node_id for e in self.graph.edges
                     if e.predicate_id == self.pred_tagged_with_id
                     and e.to_node_id == self.node_tag_dl_id]

        assert len(dl_tagged) == 2  # deep-learning tag
        assert self.node_art_neural_id in dl_tagged
        assert self.node_art_backprop_id in dl_tagged

    def test__graph__find_concepts_defined_by_article(self):                           # Find concepts an article defines
        neural_concepts = [e.to_node_id for e in self.graph.edges
                           if e.from_node_id == self.node_art_neural_id
                           and e.predicate_id == self.pred_defines_id]

        assert len(neural_concepts) == 1
        assert self.node_concept_nn_id in neural_concepts

    def test__graph__find_related_concepts(self):                                      # Find related concepts
        nn_related = [e.to_node_id for e in self.graph.edges
                      if e.from_node_id == self.node_concept_nn_id
                      and e.predicate_id == self.pred_related_to_id]

        assert len(nn_related) == 1
        assert self.node_concept_grad_id in nn_related

    # ═══════════════════════════════════════════════════════════════════════════
    # Ontology Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__ontology__symmetric_predicate(self):                                     # Test symmetric relationship
        utils = Ontology__Utils()

        # related_to is symmetric (inverse of itself)
        inverse = utils.get_inverse_predicate(self.ontology, self.pred_related_to_id)
        assert inverse.predicate_id == self.pred_related_to_id

    def test__ontology__authorship_inverse(self):                                      # Test authorship inverse
        utils = Ontology__Utils()

        # written_by ↔ authored
        assert utils.get_inverse_predicate(self.ontology, self.pred_written_by_id).predicate_id == self.pred_authored_id
        assert utils.get_inverse_predicate(self.ontology, self.pred_authored_id  ).predicate_id == self.pred_written_by_id


    def test__ontology__valid_content_relationships(self):                             # Test valid content edges
        utils = Ontology__Utils()

        # Valid relationships
        assert utils.is_valid_edge(self.ontology, self.nt_topic_id,   self.pred_contains_id,    self.nt_article_id)
        assert utils.is_valid_edge(self.ontology, self.nt_article_id, self.pred_references_id,  self.nt_article_id)
        assert utils.is_valid_edge(self.ontology, self.nt_article_id, self.pred_written_by_id,  self.nt_author_id)
        assert utils.is_valid_edge(self.ontology, self.nt_article_id, self.pred_defines_id,     self.nt_concept_id)

        # Invalid relationships
        assert not utils.is_valid_edge(self.ontology, self.nt_author_id, self.pred_contains_id, self.nt_article_id)
        assert not utils.is_valid_edge(self.ontology, self.nt_tag_id, self.pred_written_by_id, self.nt_author_id)

    # ═══════════════════════════════════════════════════════════════════════════
    # Rule Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__rules__article_requirements(self):                                       # Test article property rules
        utils = Rule_Set__Utils()

        # Articles require title and created_at
        required = utils.get_required_properties_for_node_type(self.rule_set, self.nt_article_id)
        assert len(required) == 2
        assert self.pn_title_id in required
        assert self.pn_created_at_id in required

    def test__rules__concept_requirements(self):                                       # Test concept property rules
        utils = Rule_Set__Utils()

        # Concepts require definition
        required = utils.get_required_properties_for_node_type(self.rule_set, self.nt_concept_id)
        assert len(required) == 1
        assert self.pn_definition_id in required

    def test__rules__metadata_no_requirements(self):                                   # Test tags have no requirements
        utils = Rule_Set__Utils()

        # Tags have no required properties
        required = utils.get_required_properties_for_node_type(self.rule_set, self.nt_tag_id)
        assert len(required) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Cross-Component Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__integration__node_type_category_lookup(self):                            # Test node type → category → taxonomy
        ont_utils = Ontology__Utils()
        tax_utils = Taxonomy__Utils()

        # Get article node type
        article_type = ont_utils.get_node_type(self.ontology, self.nt_article_id)
        assert article_type.category_id == self.cat_content_id

        # Get category from taxonomy
        content_cat = tax_utils.get_category(self.taxonomy, self.cat_content_id)
        assert str(content_cat.category_ref) == 'content'

        # Get parent (root)
        parent = tax_utils.get_parent(self.taxonomy, self.cat_content_id)
        assert parent.category_id == self.cat_root_id

    def test__integration__property_type_chain(self):                                  # Test property name → property type
        utils = Ontology__Utils()

        # title property → string type
        title_prop = utils.get_property_name(self.ontology, self.pn_title_id)
        assert title_prop.property_type_id == self.pt_string_id

        title_type = utils.get_property_type(self.ontology, self.pt_string_id)
        assert str(title_type.property_type_ref) == 'string'

        # created_at property → datetime type
        created_prop = utils.get_property_name(self.ontology, self.pn_created_at_id)
        assert created_prop.property_type_id == self.pt_datetime_id

        created_type = utils.get_property_type(self.ontology, self.pt_datetime_id)
        assert str(created_type.property_type_ref) == 'datetime'

    def test__scenario_data(self):
        assert self.projection.obj() == __(projection=__(nodes=[__(properties=None,
                                                               ref='topic',
                                                               name='Machine_Learning'),
                                                            __(properties=None,
                                                               ref='article',
                                                               name='Introduction_to_Neural_Networks'),
                                                            __(properties=None,
                                                               ref='article',
                                                               name='Understanding_Gradient_Descent'),
                                                            __(properties=None,
                                                               ref='article',
                                                               name='Backpropagation_Explained'),
                                                            __(properties=None,
                                                               ref='concept',
                                                               name='Neural_Network'),
                                                            __(properties=None, ref='concept', name='Gradient'),
                                                            __(properties=None,
                                                               ref='author',
                                                               name='Dr__Sarah_Chen'),
                                                            __(properties=None,
                                                               ref='author',
                                                               name='Prof__Alex_Kumar'),
                                                            __(properties=None, ref='tag', name='machine-learning'),
                                                            __(properties=None, ref='tag', name='deep-learning')],
                                                     edges=[__(properties=None,
                                                               from_name='Machine_Learning',
                                                               to_name='Introduction_to_Neural_Networks',
                                                               ref='contains'),
                                                            __(properties=None,
                                                               from_name='Machine_Learning',
                                                               to_name='Understanding_Gradient_Descent',
                                                               ref='contains'),
                                                            __(properties=None,
                                                               from_name='Machine_Learning',
                                                               to_name='Backpropagation_Explained',
                                                               ref='contains'),
                                                            __(properties=None,
                                                               from_name='Backpropagation_Explained',
                                                               to_name='Introduction_to_Neural_Networks',
                                                               ref='references'),
                                                            __(properties=None,
                                                               from_name='Backpropagation_Explained',
                                                               to_name='Understanding_Gradient_Descent',
                                                               ref='references'),
                                                            __(properties=None,
                                                               from_name='Introduction_to_Neural_Networks',
                                                               to_name='Dr__Sarah_Chen',
                                                               ref='written_by'),
                                                            __(properties=None,
                                                               from_name='Understanding_Gradient_Descent',
                                                               to_name='Prof__Alex_Kumar',
                                                               ref='written_by'),
                                                            __(properties=None,
                                                               from_name='Backpropagation_Explained',
                                                               to_name='Dr__Sarah_Chen',
                                                               ref='written_by'),
                                                            __(properties=None,
                                                               from_name='Introduction_to_Neural_Networks',
                                                               to_name='deep-learning',
                                                               ref='tagged_with'),
                                                            __(properties=None,
                                                               from_name='Understanding_Gradient_Descent',
                                                               to_name='machine-learning',
                                                               ref='tagged_with'),
                                                            __(properties=None,
                                                               from_name='Backpropagation_Explained',
                                                               to_name='deep-learning',
                                                               ref='tagged_with'),
                                                            __(properties=None,
                                                               from_name='Introduction_to_Neural_Networks',
                                                               to_name='Neural_Network',
                                                               ref='defines'),
                                                            __(properties=None,
                                                               from_name='Understanding_Gradient_Descent',
                                                               to_name='Gradient',
                                                               ref='defines'),
                                                            __(properties=None,
                                                               from_name='Neural_Network',
                                                               to_name='Gradient',
                                                               ref='related_to')]),
                                       references=__(node_types=__(topic='28ee888e',
                                                                   article='e47c230a',
                                                                   concept='ae92aaa3',
                                                                   author='75ac5e19',
                                                                   tag='faf33d23'),
                                                     predicates=__(contains='2c0e9743',
                                                                   references='3e27723d',
                                                                   written_by='2978d10a',
                                                                   tagged_with='4d778313',
                                                                   defines='c6c59f0e',
                                                                   related_to='ebf7120e'),
                                                     categories=__(metadata='f6c464cf',
                                                                   entity='1d568a65',
                                                                   knowledge='327d7688',
                                                                   content='74141e61'),
                                                     property_names=__(),
                                                     property_types=__()),
                                       taxonomy=__(node_type_categories=__(topic='content',
                                                                           article='content',
                                                                           concept='content',
                                                                           author='entity',
                                                                           tag='metadata'),
                                                   category_parents=__(metadata='knowledge',
                                                                       entity='knowledge',
                                                                       knowledge='',
                                                                       content='knowledge')),
                                       sources=__(ontology_seed=None,
                                                  source_graph_id='34d0e0a3',
                                                  generated_at=__SKIP__)) != __(projection=__(nodes=[], edges=[]),
                                       references=__(node_types=__(),
                                                     predicates=__(),
                                                     categories=__(),
                                                     property_names=__(),
                                                     property_types=__()),
                                       taxonomy=__(node_type_categories=__(), category_parents=__()),
                                       sources=__(ontology_seed=None,
                                                  source_graph_id='',
                                                  generated_at=__SKIP__))

        assert self.rule_set.obj() == __(rule_set_id_source=None,
                                           version='1.0.0',
                                           rule_set_id='e5ea36c9',
                                           rule_set_ref='kb_validation',
                                           ontology_id='d7eff75c',
                                           transitivity_rules=[],
                                           cardinality_rules=[],
                                           required_node_properties=[__(required=True,
                                                                        node_type_id='e47c230a',
                                                                        property_name_id='83772de0'),
                                                                     __(required=True,
                                                                        node_type_id='e47c230a',
                                                                        property_name_id='c1d7b5fb'),
                                                                     __(required=True,
                                                                        node_type_id='ae92aaa3',
                                                                        property_name_id='c63d900f')],
                                           required_edge_properties=[])
        assert self.taxonomy.obj() == __(taxonomy_id_source=None,
   version='1.0.0',
   taxonomy_id='db44d51c',
   taxonomy_ref='knowledge_base',
   root_id='327d7688',
   categories=__(_327d7688=__(parent_id=None,
                              category_id='327d7688',
                              category_ref='knowledge',
                              child_ids=['74141e61', 'f6c464cf', '1d568a65']),
                 _74141e61=__(parent_id='327d7688',
                              category_id='74141e61',
                              category_ref='content',
                              child_ids=[]),
                 f6c464cf=__(parent_id='327d7688',
                             category_id='f6c464cf',
                             category_ref='metadata',
                             child_ids=[]),
                 _1d568a65=__(parent_id='327d7688',
                              category_id='1d568a65',
                              category_ref='entity',
                              child_ids=[])))

        assert self.ontology.obj() == __(ontology_id_source=None,
   taxonomy_id='db44d51c',
   ontology_id='d7eff75c',
   ontology_ref='knowledge_base',
   node_types=__(_28ee888e=__(node_type_id_source=None,
                              category_id='74141e61',
                              node_type_id='28ee888e',
                              node_type_ref='topic'),
                 e47c230a=__(node_type_id_source=None,
                             category_id='74141e61',
                             node_type_id='e47c230a',
                             node_type_ref='article'),
                 ae92aaa3=__(node_type_id_source=None,
                             category_id='74141e61',
                             node_type_id='ae92aaa3',
                             node_type_ref='concept'),
                 _75ac5e19=__(node_type_id_source=None,
                              category_id='1d568a65',
                              node_type_id='75ac5e19',
                              node_type_ref='author'),
                 faf33d23=__(node_type_id_source=None,
                             category_id='f6c464cf',
                             node_type_id='faf33d23',
                             node_type_ref='tag')),
   predicates=__(_2c0e9743=__(predicate_id_source=None,
                              inverse_id='9220ce05',
                              description=None,
                              predicate_id='2c0e9743',
                              predicate_ref='contains'),
                 _9220ce05=__(predicate_id_source=None,
                              inverse_id='2c0e9743',
                              description=None,
                              predicate_id='9220ce05',
                              predicate_ref='in'),
                 _3e27723d=__(predicate_id_source=None,
                              inverse_id=None,
                              description=None,
                              predicate_id='3e27723d',
                              predicate_ref='references'),
                 _2978d10a=__(predicate_id_source=None,
                              inverse_id='c27de8e9',
                              description=None,
                              predicate_id='2978d10a',
                              predicate_ref='written_by'),
                 c27de8e9=__(predicate_id_source=None,
                             inverse_id='2978d10a',
                             description=None,
                             predicate_id='c27de8e9',
                             predicate_ref='authored'),
                 _4d778313=__(predicate_id_source=None,
                              inverse_id=None,
                              description=None,
                              predicate_id='4d778313',
                              predicate_ref='tagged_with'),
                 c6c59f0e=__(predicate_id_source=None,
                             inverse_id=None,
                             description=None,
                             predicate_id='c6c59f0e',
                             predicate_ref='defines'),
                 ebf7120e=__(predicate_id_source=None,
                             inverse_id='ebf7120e',
                             description=None,
                             predicate_id='ebf7120e',
                             predicate_ref='related_to')),
   property_names=__(_83772de0=__(property_name_id_source=None,
                                  property_type_id='ed77666f',
                                  property_name_id='83772de0',
                                  property_name_ref='title'),
                     c1d7b5fb=__(property_name_id_source=None,
                                 property_type_id='51775033',
                                 property_name_id='c1d7b5fb',
                                 property_name_ref='created_at'),
                     _49705c8a=__(property_name_id_source=None,
                                  property_type_id='51775033',
                                  property_name_id='49705c8a',
                                  property_name_ref='updated_at'),
                     c63d900f=__(property_name_id_source=None,
                                 property_type_id='ed77666f',
                                 property_name_id='c63d900f',
                                 property_name_ref='definition'),
                     _0697e334=__(property_name_id_source=None,
                                  property_type_id='e21b10b7',
                                  property_name_id='0697e334',
                                  property_name_ref='url')),
   property_types=__(ed77666f=__(property_type_id_source=None,
                                 property_type_id='ed77666f',
                                 property_type_ref='string'),
                     _51775033=__(property_type_id_source=None,
                                  property_type_id='51775033',
                                  property_type_ref='datetime'),
                     e21b10b7=__(property_type_id_source=None,
                                 property_type_id='e21b10b7',
                                 property_type_ref='url')),
   edge_rules=[__(source_type_id='28ee888e',
                  predicate_id='2c0e9743',
                  target_type_id='e47c230a'),
               __(source_type_id='e47c230a',
                  predicate_id='3e27723d',
                  target_type_id='e47c230a'),
               __(source_type_id='e47c230a',
                  predicate_id='2978d10a',
                  target_type_id='75ac5e19'),
               __(source_type_id='e47c230a',
                  predicate_id='4d778313',
                  target_type_id='faf33d23'),
               __(source_type_id='e47c230a',
                  predicate_id='c6c59f0e',
                  target_type_id='ae92aaa3'),
               __(source_type_id='ae92aaa3',
                  predicate_id='ebf7120e',
                  target_type_id='ae92aaa3')])



        assert self.graph.obj() == __(graph_id_source=None,
   rule_set_id=None,
   graph_id='34d0e0a3',
   ontology_id='d7eff75c',
   nodes=__(b1f8b0e4=__(node_id_source=None,
                        properties=None,
                        node_id='b1f8b0e4',
                        node_type_id='28ee888e',
                        name='Machine Learning'),
            b6b60ecd=__(node_id_source=None,
                        properties=None,
                        node_id='b6b60ecd',
                        node_type_id='e47c230a',
                        name='Introduction to Neural Networks'),
            fa99243d=__(node_id_source=None,
                        properties=None,
                        node_id='fa99243d',
                        node_type_id='e47c230a',
                        name='Understanding Gradient Descent'),
            d84fe289=__(node_id_source=None,
                        properties=None,
                        node_id='d84fe289',
                        node_type_id='e47c230a',
                        name='Backpropagation Explained'),
            c542c0e4=__(node_id_source=None,
                        properties=None,
                        node_id='c542c0e4',
                        node_type_id='ae92aaa3',
                        name='Neural Network'),
            _7d0bac99=__(node_id_source=None,
                         properties=None,
                         node_id='7d0bac99',
                         node_type_id='ae92aaa3',
                         name='Gradient'),
            a8769a06=__(node_id_source=None,
                        properties=None,
                        node_id='a8769a06',
                        node_type_id='75ac5e19',
                        name='Dr. Sarah Chen'),
            _2b8948cb=__(node_id_source=None,
                         properties=None,
                         node_id='2b8948cb',
                         node_type_id='75ac5e19',
                         name='Prof. Alex Kumar'),
            _13ec60e1=__(node_id_source=None,
                         properties=None,
                         node_id='13ec60e1',
                         node_type_id='faf33d23',
                         name='machine-learning'),
            _11fcb818=__(node_id_source=None,
                         properties=None,
                         node_id='11fcb818',
                         node_type_id='faf33d23',
                         name='deep-learning')),
   edges=[__(edge_id_source=None,
             properties=None,
             edge_id='e0000001',
             from_node_id='b1f8b0e4',
             to_node_id='b6b60ecd',
             predicate_id='2c0e9743'),
          __(edge_id_source=None,
             properties=None,
             edge_id='e0000002',
             from_node_id='b1f8b0e4',
             to_node_id='fa99243d',
             predicate_id='2c0e9743'),
          __(edge_id_source=None,
             properties=None,
             edge_id='e0000003',
             from_node_id='b1f8b0e4',
             to_node_id='d84fe289',
             predicate_id='2c0e9743'),
          __(edge_id_source=None,
             properties=None,
             edge_id='e0000004',
             from_node_id='d84fe289',
             to_node_id='b6b60ecd',
             predicate_id='3e27723d'),
          __(edge_id_source=None,
             properties=None,
             edge_id='e0000005',
             from_node_id='d84fe289',
             to_node_id='fa99243d',
             predicate_id='3e27723d'),
          __(edge_id_source=None,
             properties=None,
             edge_id='e0000006',
             from_node_id='b6b60ecd',
             to_node_id='a8769a06',
             predicate_id='2978d10a'),
          __(edge_id_source=None,
             properties=None,
             edge_id='e0000007',
             from_node_id='fa99243d',
             to_node_id='2b8948cb',
             predicate_id='2978d10a'),
          __(edge_id_source=None,
             properties=None,
             edge_id='e0000008',
             from_node_id='d84fe289',
             to_node_id='a8769a06',
             predicate_id='2978d10a'),
          __(edge_id_source=None,
             properties=None,
             edge_id='e0000009',
             from_node_id='b6b60ecd',
             to_node_id='11fcb818',
             predicate_id='4d778313'),
          __(edge_id_source=None,
             properties=None,
             edge_id='e0000010',
             from_node_id='fa99243d',
             to_node_id='13ec60e1',
             predicate_id='4d778313'),
          __(edge_id_source=None,
             properties=None,
             edge_id='e0000011',
             from_node_id='d84fe289',
             to_node_id='11fcb818',
             predicate_id='4d778313'),
          __(edge_id_source=None,
             properties=None,
             edge_id='e0000012',
             from_node_id='b6b60ecd',
             to_node_id='c542c0e4',
             predicate_id='c6c59f0e'),
          __(edge_id_source=None,
             properties=None,
             edge_id='e0000013',
             from_node_id='fa99243d',
             to_node_id='7d0bac99',
             predicate_id='c6c59f0e'),
          __(edge_id_source=None,
             properties=None,
             edge_id='e0000014',
             from_node_id='c542c0e4',
             to_node_id='7d0bac99',
             predicate_id='ebf7120e')])
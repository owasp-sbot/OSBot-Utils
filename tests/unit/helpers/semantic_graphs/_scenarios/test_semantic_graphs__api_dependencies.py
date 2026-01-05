# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic Graphs - API Dependencies Scenario
#
# Demonstrates semantic graphs for microservice architecture:
#   - Taxonomy: component → service, database, queue, cache
#   - Ontology: service, endpoint, database, message_queue with relationships
#   - Rules: services must have version, endpoints need path
#   - Graph: service dependency map
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
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Required_Edge_Property import List__Rules__Required_Edge_Property
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
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Edge_Property      import Schema__Rule__Required_Edge_Property
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Node_Property      import Schema__Rule__Required_Node_Property
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph                   import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge             import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node             import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy                      import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category            import Schema__Taxonomy__Category
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Utils                               import Ontology__Utils
from osbot_utils.helpers.semantic_graphs.taxonomy.Taxonomy__Utils                               import Taxonomy__Utils
from osbot_utils.helpers.semantic_graphs.rule.Rule_Set__Utils                                   import Rule_Set__Utils
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                              import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                               import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                import Obj_Id


class test_semantic_graphs__api_dependencies(TestCase):                                # API dependencies scenario

    @classmethod
    def setUpClass(cls):                                                               # Build complete API model
        cls.build_taxonomy()
        cls.build_ontology()
        cls.build_rule_set()
        cls.build_graph()

    # ═══════════════════════════════════════════════════════════════════════════
    # Model Construction
    # ═══════════════════════════════════════════════════════════════════════════

    @classmethod
    def build_taxonomy(cls):                                                           # Create infrastructure taxonomy
        # Category IDs
        cls.cat_root_id      = Category_Id(Obj_Id.from_seed('api:cat:root'))
        cls.cat_compute_id   = Category_Id(Obj_Id.from_seed('api:cat:compute'))
        cls.cat_storage_id   = Category_Id(Obj_Id.from_seed('api:cat:storage'))
        cls.cat_messaging_id = Category_Id(Obj_Id.from_seed('api:cat:messaging'))

        # Build hierarchy
        cat_root = Schema__Taxonomy__Category(
            category_id  = cls.cat_root_id                                              ,
            category_ref = Category_Ref('infrastructure')                               ,
            parent_id    = None                                                         ,
            child_ids    = List__Category_Ids([cls.cat_compute_id, cls.cat_storage_id, cls.cat_messaging_id])
        )
        cat_compute = Schema__Taxonomy__Category(
            category_id  = cls.cat_compute_id                                           ,
            category_ref = Category_Ref('compute')                                      ,
            parent_id    = cls.cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )
        cat_storage = Schema__Taxonomy__Category(
            category_id  = cls.cat_storage_id                                           ,
            category_ref = Category_Ref('storage')                                      ,
            parent_id    = cls.cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )
        cat_messaging = Schema__Taxonomy__Category(
            category_id  = cls.cat_messaging_id                                         ,
            category_ref = Category_Ref('messaging')                                    ,
            parent_id    = cls.cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )

        categories = Dict__Categories__By_Id()
        categories[cls.cat_root_id]      = cat_root
        categories[cls.cat_compute_id]   = cat_compute
        categories[cls.cat_storage_id]   = cat_storage
        categories[cls.cat_messaging_id] = cat_messaging

        cls.taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('api:taxonomy'))
        cls.taxonomy = Schema__Taxonomy(
            taxonomy_id  = cls.taxonomy_id                                              ,
            taxonomy_ref = Taxonomy_Ref('infrastructure')                               ,
            root_id      = cls.cat_root_id                                              ,
            categories   = categories
        )

    @classmethod
    def build_ontology(cls):                                                           # Create API ontology
        # Node Type IDs
        cls.nt_service_id  = Node_Type_Id(Obj_Id.from_seed('api:nt:service'))
        cls.nt_endpoint_id = Node_Type_Id(Obj_Id.from_seed('api:nt:endpoint'))
        cls.nt_database_id = Node_Type_Id(Obj_Id.from_seed('api:nt:database'))
        cls.nt_queue_id    = Node_Type_Id(Obj_Id.from_seed('api:nt:queue'))
        cls.nt_cache_id    = Node_Type_Id(Obj_Id.from_seed('api:nt:cache'))

        # Predicate IDs
        cls.pred_exposes_id      = Predicate_Id(Obj_Id.from_seed('api:pred:exposes'))
        cls.pred_calls_id        = Predicate_Id(Obj_Id.from_seed('api:pred:calls'))
        cls.pred_reads_from_id   = Predicate_Id(Obj_Id.from_seed('api:pred:reads_from'))
        cls.pred_writes_to_id    = Predicate_Id(Obj_Id.from_seed('api:pred:writes_to'))
        cls.pred_publishes_to_id = Predicate_Id(Obj_Id.from_seed('api:pred:publishes_to'))
        cls.pred_subscribes_id   = Predicate_Id(Obj_Id.from_seed('api:pred:subscribes_to'))
        cls.pred_caches_in_id    = Predicate_Id(Obj_Id.from_seed('api:pred:caches_in'))

        # Property Type IDs
        cls.pt_string_id  = Property_Type_Id(Obj_Id.from_seed('api:pt:string'))
        cls.pt_version_id = Property_Type_Id(Obj_Id.from_seed('api:pt:version'))
        cls.pt_int_id     = Property_Type_Id(Obj_Id.from_seed('api:pt:int'))

        # Property Name IDs
        cls.pn_version_id  = Property_Name_Id(Obj_Id.from_seed('api:pn:version'))
        cls.pn_path_id     = Property_Name_Id(Obj_Id.from_seed('api:pn:path'))
        cls.pn_method_id   = Property_Name_Id(Obj_Id.from_seed('api:pn:method'))
        cls.pn_port_id     = Property_Name_Id(Obj_Id.from_seed('api:pn:port'))
        cls.pn_timeout_id  = Property_Name_Id(Obj_Id.from_seed('api:pn:timeout'))

        # Node Types
        node_types = Dict__Node_Types__By_Id()
        node_types[cls.nt_service_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_service_id                                           ,
            node_type_ref = Node_Type_Ref('service')                                    ,
            category_id   = cls.cat_compute_id
        )
        node_types[cls.nt_endpoint_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_endpoint_id                                          ,
            node_type_ref = Node_Type_Ref('endpoint')                                   ,
            category_id   = cls.cat_compute_id
        )
        node_types[cls.nt_database_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_database_id                                          ,
            node_type_ref = Node_Type_Ref('database')                                   ,
            category_id   = cls.cat_storage_id
        )
        node_types[cls.nt_queue_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_queue_id                                             ,
            node_type_ref = Node_Type_Ref('message_queue')                              ,
            category_id   = cls.cat_messaging_id
        )
        node_types[cls.nt_cache_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_cache_id                                             ,
            node_type_ref = Node_Type_Ref('cache')                                      ,
            category_id   = cls.cat_storage_id
        )

        # Predicates
        predicates = Dict__Predicates__By_Id()
        predicates[cls.pred_exposes_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_exposes_id                                         ,
            predicate_ref = Predicate_Ref('exposes')                                    ,
            inverse_id    = None
        )
        predicates[cls.pred_calls_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_calls_id                                           ,
            predicate_ref = Predicate_Ref('calls')                                      ,
            inverse_id    = None
        )
        predicates[cls.pred_reads_from_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_reads_from_id                                      ,
            predicate_ref = Predicate_Ref('reads_from')                                 ,
            inverse_id    = None
        )
        predicates[cls.pred_writes_to_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_writes_to_id                                       ,
            predicate_ref = Predicate_Ref('writes_to')                                  ,
            inverse_id    = None
        )
        predicates[cls.pred_publishes_to_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_publishes_to_id                                    ,
            predicate_ref = Predicate_Ref('publishes_to')                               ,
            inverse_id    = None
        )
        predicates[cls.pred_subscribes_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_subscribes_id                                      ,
            predicate_ref = Predicate_Ref('subscribes_to')                              ,
            inverse_id    = None
        )
        predicates[cls.pred_caches_in_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_caches_in_id                                       ,
            predicate_ref = Predicate_Ref('caches_in')                                  ,
            inverse_id    = None
        )

        # Property Types
        property_types = Dict__Property_Types__By_Id()
        property_types[cls.pt_string_id] = Schema__Ontology__Property_Type(
            property_type_id  = cls.pt_string_id                                        ,
            property_type_ref = Property_Type_Ref('string')
        )
        property_types[cls.pt_version_id] = Schema__Ontology__Property_Type(
            property_type_id  = cls.pt_version_id                                       ,
            property_type_ref = Property_Type_Ref('semver')
        )
        property_types[cls.pt_int_id] = Schema__Ontology__Property_Type(
            property_type_id  = cls.pt_int_id                                           ,
            property_type_ref = Property_Type_Ref('int')
        )

        # Property Names
        property_names = Dict__Property_Names__By_Id()
        property_names[cls.pn_version_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_version_id                                       ,
            property_name_ref = Property_Name_Ref('version')                            ,
            property_type_id  = cls.pt_version_id
        )
        property_names[cls.pn_path_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_path_id                                          ,
            property_name_ref = Property_Name_Ref('path')                               ,
            property_type_id  = cls.pt_string_id
        )
        property_names[cls.pn_method_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_method_id                                        ,
            property_name_ref = Property_Name_Ref('http_method')                        ,
            property_type_id  = cls.pt_string_id
        )
        property_names[cls.pn_port_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_port_id                                          ,
            property_name_ref = Property_Name_Ref('port')                               ,
            property_type_id  = cls.pt_int_id
        )
        property_names[cls.pn_timeout_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_timeout_id                                       ,
            property_name_ref = Property_Name_Ref('timeout_ms')                         ,
            property_type_id  = cls.pt_int_id
        )

        # Edge Rules
        edge_rules = List__Edge_Rules()
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_service_id,  predicate_id=cls.pred_exposes_id,      target_type_id=cls.nt_endpoint_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_service_id,  predicate_id=cls.pred_calls_id,        target_type_id=cls.nt_endpoint_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_service_id,  predicate_id=cls.pred_reads_from_id,   target_type_id=cls.nt_database_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_service_id,  predicate_id=cls.pred_writes_to_id,    target_type_id=cls.nt_database_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_service_id,  predicate_id=cls.pred_publishes_to_id, target_type_id=cls.nt_queue_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_service_id,  predicate_id=cls.pred_subscribes_id,   target_type_id=cls.nt_queue_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_service_id,  predicate_id=cls.pred_caches_in_id,    target_type_id=cls.nt_cache_id))

        cls.ontology_id = Ontology_Id(Obj_Id.from_seed('api:ontology'))
        cls.ontology = Schema__Ontology(
            ontology_id    = cls.ontology_id                                            ,
            ontology_ref   = Ontology_Ref('api_dependencies')                           ,
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
            node_type_id     = cls.nt_service_id                                        ,
            property_name_id = cls.pn_version_id                                        ,
            required         = True
        ))
        required_node_properties.append(Schema__Rule__Required_Node_Property(
            node_type_id     = cls.nt_endpoint_id                                       ,
            property_name_id = cls.pn_path_id                                           ,
            required         = True
        ))
        required_node_properties.append(Schema__Rule__Required_Node_Property(
            node_type_id     = cls.nt_endpoint_id                                       ,
            property_name_id = cls.pn_method_id                                         ,
            required         = True
        ))

        # Edge property rules
        required_edge_properties = List__Rules__Required_Edge_Property()
        required_edge_properties.append(Schema__Rule__Required_Edge_Property(
            predicate_id     = cls.pred_calls_id                                        ,
            property_name_id = cls.pn_timeout_id                                        ,
            required         = False                                                    # Optional but tracked
        ))

        cls.rule_set_id = Rule_Set_Id(Obj_Id.from_seed('api:rules'))
        cls.rule_set = Schema__Rule_Set(
            rule_set_id              = cls.rule_set_id                                  ,
            rule_set_ref             = Rule_Set_Ref('api_validation')                   ,
            ontology_id              = cls.ontology_id                                  ,
            required_node_properties = required_node_properties                         ,
            required_edge_properties = required_edge_properties
        )

    @classmethod
    def build_graph(cls):                                                              # Create sample service graph
        # Node IDs - Services
        cls.node_api_gateway_id  = Node_Id(Obj_Id.from_seed('api:node:api_gateway'))
        cls.node_user_svc_id     = Node_Id(Obj_Id.from_seed('api:node:user_svc'))
        cls.node_order_svc_id    = Node_Id(Obj_Id.from_seed('api:node:order_svc'))
        cls.node_payment_svc_id  = Node_Id(Obj_Id.from_seed('api:node:payment_svc'))
        cls.node_notif_svc_id    = Node_Id(Obj_Id.from_seed('api:node:notif_svc'))

        # Node IDs - Endpoints
        cls.node_ep_users_id     = Node_Id(Obj_Id.from_seed('api:node:ep_users'))
        cls.node_ep_orders_id    = Node_Id(Obj_Id.from_seed('api:node:ep_orders'))
        cls.node_ep_payments_id  = Node_Id(Obj_Id.from_seed('api:node:ep_payments'))

        # Node IDs - Infrastructure
        cls.node_users_db_id     = Node_Id(Obj_Id.from_seed('api:node:users_db'))
        cls.node_orders_db_id    = Node_Id(Obj_Id.from_seed('api:node:orders_db'))
        cls.node_events_queue_id = Node_Id(Obj_Id.from_seed('api:node:events_queue'))
        cls.node_redis_cache_id  = Node_Id(Obj_Id.from_seed('api:node:redis_cache'))

        # Nodes
        nodes = Dict__Nodes__By_Id()
        # Services
        nodes[cls.node_api_gateway_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_api_gateway_id                                      ,
            node_type_id = cls.nt_service_id                                            ,
            name         = 'API Gateway'
        )
        nodes[cls.node_user_svc_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_user_svc_id                                         ,
            node_type_id = cls.nt_service_id                                            ,
            name         = 'User Service'
        )
        nodes[cls.node_order_svc_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_order_svc_id                                        ,
            node_type_id = cls.nt_service_id                                            ,
            name         = 'Order Service'
        )
        nodes[cls.node_payment_svc_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_payment_svc_id                                      ,
            node_type_id = cls.nt_service_id                                            ,
            name         = 'Payment Service'
        )
        nodes[cls.node_notif_svc_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_notif_svc_id                                        ,
            node_type_id = cls.nt_service_id                                            ,
            name         = 'Notification Service'
        )
        # Endpoints
        nodes[cls.node_ep_users_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_ep_users_id                                         ,
            node_type_id = cls.nt_endpoint_id                                           ,
            name         = 'GET /api/users'
        )
        nodes[cls.node_ep_orders_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_ep_orders_id                                        ,
            node_type_id = cls.nt_endpoint_id                                           ,
            name         = 'POST /api/orders'
        )
        nodes[cls.node_ep_payments_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_ep_payments_id                                      ,
            node_type_id = cls.nt_endpoint_id                                           ,
            name         = 'POST /api/payments'
        )
        # Infrastructure
        nodes[cls.node_users_db_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_users_db_id                                         ,
            node_type_id = cls.nt_database_id                                           ,
            name         = 'Users PostgreSQL'
        )
        nodes[cls.node_orders_db_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_orders_db_id                                        ,
            node_type_id = cls.nt_database_id                                           ,
            name         = 'Orders PostgreSQL'
        )
        nodes[cls.node_events_queue_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_events_queue_id                                     ,
            node_type_id = cls.nt_queue_id                                              ,
            name         = 'Events Kafka'
        )
        nodes[cls.node_redis_cache_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_redis_cache_id                                      ,
            node_type_id = cls.nt_cache_id                                              ,
            name         = 'Redis Cache'
        )

        # Edges
        edges = List__Semantic_Graph__Edges()
        # Service exposes endpoints
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_user_svc_id,    predicate_id=cls.pred_exposes_id,      to_node_id=cls.node_ep_users_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_order_svc_id,   predicate_id=cls.pred_exposes_id,      to_node_id=cls.node_ep_orders_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_payment_svc_id, predicate_id=cls.pred_exposes_id,      to_node_id=cls.node_ep_payments_id))
        # Gateway calls endpoints
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_api_gateway_id, predicate_id=cls.pred_calls_id,        to_node_id=cls.node_ep_users_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_api_gateway_id, predicate_id=cls.pred_calls_id,        to_node_id=cls.node_ep_orders_id))
        # Service to service calls
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_order_svc_id,   predicate_id=cls.pred_calls_id,        to_node_id=cls.node_ep_payments_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_order_svc_id,   predicate_id=cls.pred_calls_id,        to_node_id=cls.node_ep_users_id))
        # Database reads/writes
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_user_svc_id,    predicate_id=cls.pred_reads_from_id,   to_node_id=cls.node_users_db_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_user_svc_id,    predicate_id=cls.pred_writes_to_id,    to_node_id=cls.node_users_db_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_order_svc_id,   predicate_id=cls.pred_reads_from_id,   to_node_id=cls.node_orders_db_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_order_svc_id,   predicate_id=cls.pred_writes_to_id,    to_node_id=cls.node_orders_db_id))
        # Message queue pub/sub
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_order_svc_id,   predicate_id=cls.pred_publishes_to_id, to_node_id=cls.node_events_queue_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_payment_svc_id, predicate_id=cls.pred_publishes_to_id, to_node_id=cls.node_events_queue_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_notif_svc_id,   predicate_id=cls.pred_subscribes_id,   to_node_id=cls.node_events_queue_id))
        # Caching
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_user_svc_id,    predicate_id=cls.pred_caches_in_id,    to_node_id=cls.node_redis_cache_id))

        cls.graph_id = Graph_Id(Obj_Id.from_seed('api:graph'))
        cls.graph = Schema__Semantic_Graph(
            graph_id    = cls.graph_id                                                  ,
            ontology_id = cls.ontology_id                                               ,
            nodes       = nodes                                                         ,
            edges       = edges
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # Dependency Analysis Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__graph__service_dependencies(self):                                       # Find all service dependencies
        # Find what Order Service depends on
        order_deps = [e for e in self.graph.edges if e.from_node_id == self.node_order_svc_id]

        assert len(order_deps) == 6  # exposes, calls(2), reads, writes, publishes

        pred_types = set(e.predicate_id for e in order_deps)
        assert self.pred_exposes_id      in pred_types
        assert self.pred_calls_id        in pred_types
        assert self.pred_reads_from_id   in pred_types
        assert self.pred_writes_to_id    in pred_types
        assert self.pred_publishes_to_id in pred_types

    def test__graph__find_database_users(self):                                        # Find services that use a database
        users_db_readers = [e.from_node_id for e in self.graph.edges
                            if e.to_node_id == self.node_users_db_id
                            and e.predicate_id == self.pred_reads_from_id]

        assert len(users_db_readers) == 1
        assert self.node_user_svc_id in users_db_readers

    def test__graph__message_flow(self):                                               # Trace message flow through queue
        publishers = [e.from_node_id for e in self.graph.edges
                      if e.to_node_id == self.node_events_queue_id
                      and e.predicate_id == self.pred_publishes_to_id]

        subscribers = [e.from_node_id for e in self.graph.edges
                       if e.to_node_id == self.node_events_queue_id
                       and e.predicate_id == self.pred_subscribes_id]

        assert len(publishers) == 2   # order and payment services
        assert len(subscribers) == 1  # notification service

        assert self.node_order_svc_id in publishers
        assert self.node_payment_svc_id in publishers
        assert self.node_notif_svc_id in subscribers

    def test__graph__endpoint_exposure(self):                                          # Find which service exposes an endpoint
        users_endpoint_owner = [e.from_node_id for e in self.graph.edges
                                if e.to_node_id == self.node_ep_users_id
                                and e.predicate_id == self.pred_exposes_id]

        assert len(users_endpoint_owner) == 1
        assert self.node_user_svc_id in users_endpoint_owner

    def test__graph__find_callers(self):                                               # Find who calls an endpoint
        users_ep_callers = [e.from_node_id for e in self.graph.edges
                            if e.to_node_id == self.node_ep_users_id
                            and e.predicate_id == self.pred_calls_id]

        assert len(users_ep_callers) == 2  # gateway and order service
        assert self.node_api_gateway_id in users_ep_callers
        assert self.node_order_svc_id in users_ep_callers

    # ═══════════════════════════════════════════════════════════════════════════
    # Infrastructure Category Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__taxonomy__infrastructure_categories(self):                               # Test category hierarchy
        utils = Taxonomy__Utils()

        # Check structure
        root = utils.get_root_category(self.taxonomy)
        assert str(root.category_ref) == 'infrastructure'

        children = utils.get_children(self.taxonomy, self.cat_root_id)
        assert len(children) == 3
        assert self.cat_compute_id in children
        assert self.cat_storage_id in children
        assert self.cat_messaging_id in children

    def test__ontology__node_type_categories(self):                                    # Test node types in categories
        utils = Ontology__Utils()

        # Compute category: service, endpoint
        service_type = utils.get_node_type(self.ontology, self.nt_service_id)
        assert service_type.category_id == self.cat_compute_id

        endpoint_type = utils.get_node_type(self.ontology, self.nt_endpoint_id)
        assert endpoint_type.category_id == self.cat_compute_id

        # Storage category: database, cache
        db_type = utils.get_node_type(self.ontology, self.nt_database_id)
        assert db_type.category_id == self.cat_storage_id

        cache_type = utils.get_node_type(self.ontology, self.nt_cache_id)
        assert cache_type.category_id == self.cat_storage_id

        # Messaging category: queue
        queue_type = utils.get_node_type(self.ontology, self.nt_queue_id)
        assert queue_type.category_id == self.cat_messaging_id

    # ═══════════════════════════════════════════════════════════════════════════
    # Rule Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__rules__service_requirements(self):                                       # Test service property rules
        utils = Rule_Set__Utils()

        # Services require version
        required = utils.get_required_properties_for_node_type(self.rule_set, self.nt_service_id)
        assert len(required) == 1
        assert self.pn_version_id in required

    def test__rules__endpoint_requirements(self):                                      # Test endpoint property rules
        utils = Rule_Set__Utils()

        # Endpoints require path and method
        required = utils.get_required_properties_for_node_type(self.rule_set, self.nt_endpoint_id)
        assert len(required) == 2
        assert self.pn_path_id in required
        assert self.pn_method_id in required

    def test__rules__edge_properties(self):                                            # Test edge property rules
        utils = Rule_Set__Utils()

        # calls predicate has optional timeout
        assert utils.has_required_edge_property_rule(self.rule_set, self.pred_calls_id, self.pn_timeout_id)
        assert not utils.is_edge_property_required(self.rule_set, self.pred_calls_id, self.pn_timeout_id)

    def test__rules__infrastructure_no_requirements(self):                             # Test infra has no required props
        utils = Rule_Set__Utils()

        # Database, queue, cache have no required properties
        assert len(utils.get_required_properties_for_node_type(self.rule_set, self.nt_database_id)) == 0
        assert len(utils.get_required_properties_for_node_type(self.rule_set, self.nt_queue_id)) == 0
        assert len(utils.get_required_properties_for_node_type(self.rule_set, self.nt_cache_id)) == 0
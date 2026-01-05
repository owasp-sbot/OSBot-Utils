# ═══════════════════════════════════════════════════════════════════════════════
# Ontology__Utils - Operations on Schema__Ontology (business logic)
#
# Updated for Brief 3.8:
#   - Added property name and property type query methods
#   - Added create_property_name and create_property_type methods
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Node_Type_Ids           import List__Node_Type_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Predicate_Ids           import List__Predicate_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Property_Name_Ids       import List__Property_Name_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Property_Type_Ids       import List__Property_Type_Ids
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                  import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                 import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                  import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref                 import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id              import Property_Name_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Ref             import Property_Name_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Id              import Property_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Ref             import Property_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                   import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source            import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type               import Enum__Id__Source_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Edge_Rule     import Schema__Ontology__Edge_Rule
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type     import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Predicate     import Schema__Ontology__Predicate
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Property_Name import Schema__Ontology__Property_Name
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Property_Type import Schema__Ontology__Property_Type
from osbot_utils.type_safe.Type_Safe                                                      import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                          import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed     import Safe_Str__Id__Seed
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                            import type_safe


class Ontology__Utils(Type_Safe):                                                      # Operations on ontology schemas

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Type Creation
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_node_type(self                              ,
                         node_type_ref : Node_Type_Ref     ,
                         category_id   : Category_Id   = None,
                         seed          : Safe_Str__Id__Seed = None) -> Schema__Ontology__Node_Type:
        if seed:                                                                       # Create node type with ID
            node_type_id        = Node_Type_Id(Obj_Id.from_seed(seed))
            node_type_id_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                                     seed        = seed                               )
        else:
            node_type_id        = Node_Type_Id(Obj_Id())
            node_type_id_source = None

        return Schema__Ontology__Node_Type(node_type_id        = node_type_id       ,
                                           node_type_id_source = node_type_id_source,
                                           node_type_ref       = node_type_ref      ,
                                           category_id         = category_id        )

    # ═══════════════════════════════════════════════════════════════════════════
    # Predicate Creation
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_predicate(self                               ,
                         predicate_ref : Predicate_Ref      ,
                         inverse_id    : Predicate_Id  = None,
                         seed          : Safe_Str__Id__Seed = None) -> Schema__Ontology__Predicate:
        if seed:                                                                       # Create predicate with ID
            predicate_id        = Predicate_Id(Obj_Id.from_seed(seed))
            predicate_id_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                                     seed        = seed                               )
        else:
            predicate_id        = Predicate_Id(Obj_Id())
            predicate_id_source = None

        return Schema__Ontology__Predicate(predicate_id        = predicate_id       ,
                                           predicate_id_source = predicate_id_source,
                                           predicate_ref       = predicate_ref      ,
                                           inverse_id          = inverse_id         )

    @type_safe
    def create_predicate_pair(self                                  ,
                              predicate_ref : Predicate_Ref         ,
                              inverse_ref   : Predicate_Ref         ,
                              seed          : Safe_Str__Id__Seed = None,
                              inverse_seed  : Safe_Str__Id__Seed = None) -> tuple:
        if seed:                                                                       # Create linked predicate pair
            predicate_id = Predicate_Id(Obj_Id.from_seed(seed))
        else:
            predicate_id = Predicate_Id(Obj_Id())

        if inverse_seed:
            inverse_id = Predicate_Id(Obj_Id.from_seed(inverse_seed))
        else:
            inverse_id = Predicate_Id(Obj_Id())

        predicate = self.create_predicate(predicate_ref = predicate_ref,
                                          inverse_id    = inverse_id   ,
                                          seed          = seed         )

        inverse = self.create_predicate(predicate_ref = inverse_ref  ,
                                        inverse_id    = predicate_id ,
                                        seed          = inverse_seed )

        return (predicate, inverse)

    # ═══════════════════════════════════════════════════════════════════════════
    # Property Name Creation
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_property_name(self                                   ,
                             property_name_ref : Property_Name_Ref  ,
                             property_type_id  : Property_Type_Id = None,
                             seed              : Safe_Str__Id__Seed = None) -> Schema__Ontology__Property_Name:
        if seed:                                                                       # Create property name with ID
            property_name_id        = Property_Name_Id(Obj_Id.from_seed(seed))
            property_name_id_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                                         seed        = seed                               )
        else:
            property_name_id        = Property_Name_Id(Obj_Id())
            property_name_id_source = None

        return Schema__Ontology__Property_Name(property_name_id        = property_name_id       ,
                                               property_name_id_source = property_name_id_source,
                                               property_name_ref       = property_name_ref      ,
                                               property_type_id        = property_type_id       )

    # ═══════════════════════════════════════════════════════════════════════════
    # Property Type Creation
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_property_type(self                                   ,
                             property_type_ref : Property_Type_Ref  ,
                             seed              : Safe_Str__Id__Seed = None) -> Schema__Ontology__Property_Type:
        if seed:                                                                       # Create property type with ID
            property_type_id        = Property_Type_Id(Obj_Id.from_seed(seed))
            property_type_id_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                                         seed        = seed                               )
        else:
            property_type_id        = Property_Type_Id(Obj_Id())
            property_type_id_source = None

        return Schema__Ontology__Property_Type(property_type_id        = property_type_id       ,
                                               property_type_id_source = property_type_id_source,
                                               property_type_ref       = property_type_ref      )

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Rule Creation
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_edge_rule(self                           ,
                         source_type_id : Node_Type_Id  ,
                         predicate_id   : Predicate_Id  ,
                         target_type_id : Node_Type_Id  ) -> Schema__Ontology__Edge_Rule:
        return Schema__Ontology__Edge_Rule(source_type_id = source_type_id,            # Create edge rule
                                           predicate_id   = predicate_id  ,
                                           target_type_id = target_type_id)

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Type Queries
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_node_type(self                        ,
                      ontology     : Schema__Ontology,
                      node_type_id : Node_Type_Id    ) -> Schema__Ontology__Node_Type:
        return ontology.node_types.get(node_type_id)                                   # Get node type by ID

    @type_safe
    def get_node_type_by_ref(self                        ,
                             ontology      : Schema__Ontology,
                             node_type_ref : Node_Type_Ref   ) -> Schema__Ontology__Node_Type:
        for node_type in ontology.node_types.values():                                 # Get node type by ref (linear scan)
            if node_type.node_type_ref == node_type_ref:
                return node_type
        return None

    @type_safe
    def get_node_type_id_by_ref(self                        ,
                                ontology      : Schema__Ontology,
                                node_type_ref : Node_Type_Ref   ) -> Node_Type_Id:
        node_type = self.get_node_type_by_ref(ontology, node_type_ref)                 # Resolve ref → ID
        if node_type is None:
            return None
        return node_type.node_type_id

    @type_safe
    def has_node_type(self                        ,
                      ontology     : Schema__Ontology,
                      node_type_id : Node_Type_Id    ) -> bool:
        return node_type_id in ontology.node_types                                     # Check if node type exists by ID

    @type_safe
    def has_node_type_ref(self                        ,
                          ontology      : Schema__Ontology,
                          node_type_ref : Node_Type_Ref   ) -> bool:
        return self.get_node_type_by_ref(ontology, node_type_ref) is not None          # Check if node type exists by ref

    @type_safe
    def node_type_ids(self                   ,
                      ontology : Schema__Ontology) -> List__Node_Type_Ids:
        result = List__Node_Type_Ids()                                                 # All node type IDs
        for node_type_id in ontology.node_types.keys():
            result.append(node_type_id)
        return result

    # ═══════════════════════════════════════════════════════════════════════════
    # Predicate Queries
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_predicate(self                       ,
                      ontology     : Schema__Ontology,
                      predicate_id : Predicate_Id    ) -> Schema__Ontology__Predicate:
        return ontology.predicates.get(predicate_id)                                   # Get predicate by ID

    @type_safe
    def get_predicate_by_ref(self                       ,
                             ontology      : Schema__Ontology,
                             predicate_ref : Predicate_Ref   ) -> Schema__Ontology__Predicate:
        for predicate in ontology.predicates.values():                                 # Get predicate by ref (linear scan)
            if predicate.predicate_ref == predicate_ref:
                return predicate
        return None

    @type_safe
    def get_predicate_id_by_ref(self                       ,
                                ontology      : Schema__Ontology,
                                predicate_ref : Predicate_Ref   ) -> Predicate_Id:
        predicate = self.get_predicate_by_ref(ontology, predicate_ref)                 # Resolve ref → ID
        if predicate is None:
            return None
        return predicate.predicate_id

    @type_safe
    def has_predicate(self                       ,
                      ontology     : Schema__Ontology,
                      predicate_id : Predicate_Id    ) -> bool:
        return predicate_id in ontology.predicates                                     # Check if predicate exists by ID

    @type_safe
    def predicate_ids(self                   ,
                      ontology : Schema__Ontology) -> List__Predicate_Ids:
        result = List__Predicate_Ids()                                                 # All predicate IDs
        for predicate_id in ontology.predicates.keys():
            result.append(predicate_id)
        return result

    @type_safe
    def get_inverse_predicate(self                       ,
                              ontology     : Schema__Ontology,
                              predicate_id : Predicate_Id    ) -> Schema__Ontology__Predicate:
        predicate = self.get_predicate(ontology, predicate_id)                         # Get inverse predicate
        if predicate is None or predicate.inverse_id is None:
            return None
        return self.get_predicate(ontology, predicate.inverse_id)

    # ═══════════════════════════════════════════════════════════════════════════
    # Property Name Queries
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_property_name(self                           ,
                          ontology         : Schema__Ontology  ,
                          property_name_id : Property_Name_Id  ) -> Schema__Ontology__Property_Name:
        return ontology.property_names.get(property_name_id)                           # Get property name by ID

    @type_safe
    def get_property_name_by_ref(self                            ,
                                 ontology          : Schema__Ontology  ,
                                 property_name_ref : Property_Name_Ref ) -> Schema__Ontology__Property_Name:
        for prop_name in ontology.property_names.values():                             # Get property name by ref (linear scan)
            if prop_name.property_name_ref == property_name_ref:
                return prop_name
        return None

    @type_safe
    def get_property_name_id_by_ref(self                            ,
                                    ontology          : Schema__Ontology  ,
                                    property_name_ref : Property_Name_Ref ) -> Property_Name_Id:
        prop_name = self.get_property_name_by_ref(ontology, property_name_ref)         # Resolve ref → ID
        if prop_name is None:
            return None
        return prop_name.property_name_id

    @type_safe
    def has_property_name(self                           ,
                          ontology         : Schema__Ontology  ,
                          property_name_id : Property_Name_Id  ) -> bool:
        return property_name_id in ontology.property_names                             # Check if property name exists by ID

    @type_safe
    def property_name_ids(self                   ,
                          ontology : Schema__Ontology) -> List__Property_Name_Ids:
        result = List__Property_Name_Ids()                                             # All property name IDs
        for prop_id in ontology.property_names.keys():
            result.append(prop_id)
        return result

    # ═══════════════════════════════════════════════════════════════════════════
    # Property Type Queries
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_property_type(self                           ,
                          ontology         : Schema__Ontology  ,
                          property_type_id : Property_Type_Id  ) -> Schema__Ontology__Property_Type:
        return ontology.property_types.get(property_type_id)                           # Get property type by ID

    @type_safe
    def get_property_type_by_ref(self                            ,
                                 ontology          : Schema__Ontology  ,
                                 property_type_ref : Property_Type_Ref ) -> Schema__Ontology__Property_Type:
        for prop_type in ontology.property_types.values():                             # Get property type by ref (linear scan)
            if prop_type.property_type_ref == property_type_ref:
                return prop_type
        return None

    @type_safe
    def get_property_type_id_by_ref(self                            ,
                                    ontology          : Schema__Ontology  ,
                                    property_type_ref : Property_Type_Ref ) -> Property_Type_Id:
        prop_type = self.get_property_type_by_ref(ontology, property_type_ref)         # Resolve ref → ID
        if prop_type is None:
            return None
        return prop_type.property_type_id

    @type_safe
    def has_property_type(self                           ,
                          ontology         : Schema__Ontology  ,
                          property_type_id : Property_Type_Id  ) -> bool:
        return property_type_id in ontology.property_types                             # Check if property type exists by ID

    @type_safe
    def property_type_ids(self                   ,
                          ontology : Schema__Ontology) -> List__Property_Type_Ids:
        result = List__Property_Type_Ids()                                             # All property type IDs
        for type_id in ontology.property_types.keys():
            result.append(type_id)
        return result

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Rule Queries
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def is_valid_edge(self                         ,
                      ontology       : Schema__Ontology,
                      source_type_id : Node_Type_Id    ,
                      predicate_id   : Predicate_Id    ,
                      target_type_id : Node_Type_Id    ) -> bool:
        for rule in ontology.edge_rules:                                               # Check if edge is valid per rules
            if (rule.source_type_id == source_type_id and
                rule.predicate_id   == predicate_id   and
                rule.target_type_id == target_type_id):
                return True
        return False

    @type_safe
    def is_valid_edge_by_ref(self                         ,
                             ontology       : Schema__Ontology,
                             source_type_ref: Node_Type_Ref   ,
                             predicate_ref  : Predicate_Ref   ,
                             target_type_ref: Node_Type_Ref   ) -> bool:
        source_type_id = self.get_node_type_id_by_ref(ontology, source_type_ref)       # Resolve refs to IDs then check
        predicate_id   = self.get_predicate_id_by_ref(ontology, predicate_ref)
        target_type_id = self.get_node_type_id_by_ref(ontology, target_type_ref)

        if source_type_id is None or predicate_id is None or target_type_id is None:
            return False

        return self.is_valid_edge(ontology, source_type_id, predicate_id, target_type_id)

    @type_safe
    def valid_targets_for(self                         ,
                          ontology       : Schema__Ontology,
                          source_type_id : Node_Type_Id    ,
                          predicate_id   : Predicate_Id    ) -> List__Node_Type_Ids:
        result = List__Node_Type_Ids()                                                 # Get valid target types for edge
        for rule in ontology.edge_rules:
            if (rule.source_type_id == source_type_id and
                rule.predicate_id   == predicate_id):
                if rule.target_type_id not in result:
                    result.append(rule.target_type_id)
        return result

    @type_safe
    def valid_predicates_for(self                         ,
                             ontology       : Schema__Ontology,
                             source_type_id : Node_Type_Id    ) -> List__Predicate_Ids:
        result = List__Predicate_Ids()                                                 # Get valid predicates from source type
        for rule in ontology.edge_rules:
            if rule.source_type_id == source_type_id:
                if rule.predicate_id not in result:
                    result.append(rule.predicate_id)
        return result

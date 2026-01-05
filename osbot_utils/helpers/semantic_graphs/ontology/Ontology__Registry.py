# ═══════════════════════════════════════════════════════════════════════════════
# Ontology__Registry - Registry for ontology definitions with factory methods
#
# Updated for Brief 3.8:
#   - Added property name and property type lookup methods
#   - Factory methods support property_names and property_types dicts
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id     import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Ontologies__By_Id     import Dict__Ontologies__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Ontologies__By_Ref    import Dict__Ontologies__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicates__By_Id     import Dict__Predicates__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Names__By_Id import Dict__Property_Names__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Types__By_Id import Dict__Property_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Edge_Rules            import List__Edge_Rules
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Ontology_Ids          import List__Ontology_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Ontology_Refs         import List__Ontology_Refs
from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type             import Enum__Id__Source_Type
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref               import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                 import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref                import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref               import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id            import Property_Name_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Ref           import Property_Name_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Id            import Property_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Ref           import Property_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source          import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                 import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology              import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type   import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Predicate   import Schema__Ontology__Predicate
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Property_Name import Schema__Ontology__Property_Name
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Property_Type import Schema__Ontology__Property_Type
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed   import Safe_Str__Id__Seed
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                          import type_safe


class Ontology__Registry(Type_Safe):                                                  # Registry for ontology definitions
    ontologies_by_id  : Dict__Ontologies__By_Id                                       # Primary: lookup by instance ID
    ontologies_by_ref : Dict__Ontologies__By_Ref                                      # Secondary: lookup by reference name

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory methods for creating ontologies with different ID modes
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_with__random_id(self                                     ,
                               ontology_ref   : Ontology_Ref            ,
                               taxonomy_id    : Taxonomy_Id        = None,
                               node_types     : Dict__Node_Types__By_Id     = None,
                               predicates     : Dict__Predicates__By_Id     = None,
                               property_names : Dict__Property_Names__By_Id = None,
                               property_types : Dict__Property_Types__By_Id = None,
                               edge_rules     : List__Edge_Rules            = None) -> Schema__Ontology:
        ontology_id = Ontology_Id(Obj_Id())                                           # Random ID
        ontology    = Schema__Ontology(ontology_id    = ontology_id                           ,
                                       ontology_ref   = ontology_ref                          ,
                                       taxonomy_id    = taxonomy_id                           ,
                                       node_types     = node_types     or Dict__Node_Types__By_Id()    ,
                                       predicates     = predicates     or Dict__Predicates__By_Id()    ,
                                       property_names = property_names or Dict__Property_Names__By_Id(),
                                       property_types = property_types or Dict__Property_Types__By_Id(),
                                       edge_rules     = edge_rules     or List__Edge_Rules()           )
        self.register(ontology)
        return ontology

    @type_safe
    def create_with__deterministic_id(self                                     ,
                                      ontology_ref   : Ontology_Ref            ,
                                      seed           : Safe_Str__Id__Seed      ,
                                      taxonomy_id    : Taxonomy_Id        = None,
                                      node_types     : Dict__Node_Types__By_Id     = None,
                                      predicates     : Dict__Predicates__By_Id     = None,
                                      property_names : Dict__Property_Names__By_Id = None,
                                      property_types : Dict__Property_Types__By_Id = None,
                                      edge_rules     : List__Edge_Rules            = None) -> Schema__Ontology:
        ontology_id        = Ontology_Id(Obj_Id.from_seed(seed))                      # Deterministic ID from seed
        ontology_id_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                                seed        = seed                    )
        ontology = Schema__Ontology(ontology_id        = ontology_id                          ,
                                    ontology_id_source = ontology_id_source                   ,
                                    ontology_ref       = ontology_ref                         ,
                                    taxonomy_id        = taxonomy_id                          ,
                                    node_types         = node_types     or Dict__Node_Types__By_Id()    ,
                                    predicates         = predicates     or Dict__Predicates__By_Id()    ,
                                    property_names     = property_names or Dict__Property_Names__By_Id(),
                                    property_types     = property_types or Dict__Property_Types__By_Id(),
                                    edge_rules         = edge_rules     or List__Edge_Rules()           )
        self.register(ontology)
        return ontology

    @type_safe
    def create_with__explicit_id(self                                          ,
                                 ontology_ref       : Ontology_Ref             ,
                                 ontology_id        : Ontology_Id              ,
                                 ontology_id_source : Schema__Id__Source  = None,
                                 taxonomy_id        : Taxonomy_Id         = None,
                                 node_types         : Dict__Node_Types__By_Id     = None,
                                 predicates         : Dict__Predicates__By_Id     = None,
                                 property_names     : Dict__Property_Names__By_Id = None,
                                 property_types     : Dict__Property_Types__By_Id = None,
                                 edge_rules         : List__Edge_Rules            = None) -> Schema__Ontology:
        ontology = Schema__Ontology(ontology_id        = ontology_id                          ,
                                    ontology_id_source = ontology_id_source                   ,
                                    ontology_ref       = ontology_ref                         ,
                                    taxonomy_id        = taxonomy_id                          ,
                                    node_types         = node_types     or Dict__Node_Types__By_Id()    ,
                                    predicates         = predicates     or Dict__Predicates__By_Id()    ,
                                    property_names     = property_names or Dict__Property_Names__By_Id(),
                                    property_types     = property_types or Dict__Property_Types__By_Id(),
                                    edge_rules         = edge_rules     or List__Edge_Rules()           )
        self.register(ontology)
        return ontology

    # ═══════════════════════════════════════════════════════════════════════════
    # Registration and lookup
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def register(self, ontology: Schema__Ontology) -> Schema__Ontology:               # Register ontology in both indexes
        if ontology.ontology_id:                                                      # Primary index by ID
            self.ontologies_by_id[ontology.ontology_id] = ontology
        self.ontologies_by_ref[ontology.ontology_ref] = ontology                      # Secondary index by ref
        return ontology

    @type_safe
    def get_by_id(self, ontology_id: Ontology_Id) -> Schema__Ontology:                # Primary: lookup by instance ID
        return self.ontologies_by_id.get(ontology_id)

    @type_safe
    def get_by_ref(self, ontology_ref: Ontology_Ref) -> Schema__Ontology:             # Secondary: lookup by reference name
        return self.ontologies_by_ref.get(ontology_ref)

    @type_safe
    def has_id(self, ontology_id: Ontology_Id) -> bool:                               # Check if ID exists
        return ontology_id in self.ontologies_by_id

    @type_safe
    def has_ref(self, ontology_ref: Ontology_Ref) -> bool:                            # Check if ref exists
        return ontology_ref in self.ontologies_by_ref

    @type_safe
    def all_ids(self) -> List__Ontology_Ids:                                          # All registered IDs
        result = List__Ontology_Ids()
        for id in self.ontologies_by_id.keys():
            result.append(id)
        return result

    @type_safe
    def all_refs(self) -> List__Ontology_Refs:                                        # All registered refs
        result = List__Ontology_Refs()
        for ref in self.ontologies_by_ref.keys():
            result.append(ref)
        return result

    # ═══════════════════════════════════════════════════════════════════════════
    # Predicate lookup (dual indexing within ontology)
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_predicate_by_id(self                       ,
                            ontology_id  : Ontology_Id ,
                            predicate_id : Predicate_Id) -> Schema__Ontology__Predicate:
        ontology = self.get_by_id(ontology_id)                                        # Get predicate by ID from ontology
        if ontology is None:
            return None
        return ontology.predicates.get(predicate_id)

    @type_safe
    def get_predicate_by_ref(self                        ,
                             ontology_id   : Ontology_Id ,
                             predicate_ref : Predicate_Ref) -> Schema__Ontology__Predicate:
        ontology = self.get_by_id(ontology_id)                                        # Get predicate by ref from ontology
        if ontology is None:
            return None
        for predicate in ontology.predicates.values():                                # Linear scan
            if predicate.predicate_ref == predicate_ref:
                return predicate
        return None

    @type_safe
    def get_predicate_id_by_ref(self                        ,
                                ontology_id   : Ontology_Id ,
                                predicate_ref : Predicate_Ref) -> Predicate_Id:
        predicate = self.get_predicate_by_ref(ontology_id, predicate_ref)             # Resolve ref → ID
        if predicate is None:
            return None
        return predicate.predicate_id

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Type lookup (dual indexing within ontology)
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_node_type_by_id(self                        ,
                            ontology_id  : Ontology_Id  ,
                            node_type_id : Node_Type_Id ) -> Schema__Ontology__Node_Type:
        ontology = self.get_by_id(ontology_id)                                        # Get node type by ID from ontology
        if ontology is None:
            return None
        return ontology.node_types.get(node_type_id)

    @type_safe
    def get_node_type_by_ref(self                         ,
                             ontology_id   : Ontology_Id  ,
                             node_type_ref : Node_Type_Ref) -> Schema__Ontology__Node_Type:
        ontology = self.get_by_id(ontology_id)                                        # Get node type by ref from ontology
        if ontology is None:
            return None
        for node_type in ontology.node_types.values():                                # Linear scan
            if node_type.node_type_ref == node_type_ref:
                return node_type
        return None

    @type_safe
    def get_node_type_id_by_ref(self                         ,
                                ontology_id   : Ontology_Id  ,
                                node_type_ref : Node_Type_Ref) -> Node_Type_Id:
        node_type = self.get_node_type_by_ref(ontology_id, node_type_ref)             # Resolve ref → ID
        if node_type is None:
            return None
        return node_type.node_type_id

    # ═══════════════════════════════════════════════════════════════════════════
    # Property Name lookup (dual indexing within ontology)
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_property_name_by_id(self                           ,
                                ontology_id      : Ontology_Id     ,
                                property_name_id : Property_Name_Id) -> Schema__Ontology__Property_Name:
        ontology = self.get_by_id(ontology_id)                                        # Get property name by ID
        if ontology is None:
            return None
        return ontology.property_names.get(property_name_id)

    @type_safe
    def get_property_name_by_ref(self                            ,
                                 ontology_id       : Ontology_Id     ,
                                 property_name_ref : Property_Name_Ref) -> Schema__Ontology__Property_Name:
        ontology = self.get_by_id(ontology_id)                                        # Get property name by ref
        if ontology is None:
            return None
        for prop_name in ontology.property_names.values():                            # Linear scan
            if prop_name.property_name_ref == property_name_ref:
                return prop_name
        return None

    @type_safe
    def get_property_name_id_by_ref(self                            ,
                                    ontology_id       : Ontology_Id     ,
                                    property_name_ref : Property_Name_Ref) -> Property_Name_Id:
        prop_name = self.get_property_name_by_ref(ontology_id, property_name_ref)     # Resolve ref → ID
        if prop_name is None:
            return None
        return prop_name.property_name_id

    # ═══════════════════════════════════════════════════════════════════════════
    # Property Type lookup (dual indexing within ontology)
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_property_type_by_id(self                           ,
                                ontology_id      : Ontology_Id     ,
                                property_type_id : Property_Type_Id) -> Schema__Ontology__Property_Type:
        ontology = self.get_by_id(ontology_id)                                        # Get property type by ID
        if ontology is None:
            return None
        return ontology.property_types.get(property_type_id)

    @type_safe
    def get_property_type_by_ref(self                            ,
                                 ontology_id       : Ontology_Id     ,
                                 property_type_ref : Property_Type_Ref) -> Schema__Ontology__Property_Type:
        ontology = self.get_by_id(ontology_id)                                        # Get property type by ref
        if ontology is None:
            return None
        for prop_type in ontology.property_types.values():                            # Linear scan
            if prop_type.property_type_ref == property_type_ref:
                return prop_type
        return None

    @type_safe
    def get_property_type_id_by_ref(self                            ,
                                    ontology_id       : Ontology_Id     ,
                                    property_type_ref : Property_Type_Ref) -> Property_Type_Id:
        prop_type = self.get_property_type_by_ref(ontology_id, property_type_ref)     # Resolve ref → ID
        if prop_type is None:
            return None
        return prop_type.property_type_id

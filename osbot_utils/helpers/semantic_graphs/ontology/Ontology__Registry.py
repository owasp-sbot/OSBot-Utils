# ═══════════════════════════════════════════════════════════════════════════════
# Ontology__Registry - Registry for ontology definitions with factory methods
# Provides lookup by ref (name) and by id (instance identifier)
#
# Also provides dual indexing for predicates and node_types within ontologies:
#   - get_predicate_by_id / get_predicate_by_ref
#   - get_node_type_by_id / get_node_type_by_ref
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id   import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Ontologies__By_Id   import Dict__Ontologies__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Ontologies__By_Ref  import Dict__Ontologies__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicates__By_Id   import Dict__Predicates__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Edge_Rules          import List__Edge_Rules
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Ontology_Ids        import List__Ontology_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Ontology_Refs       import List__Ontology_Refs
from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type           import Enum__Id__Source_Type
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id              import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref             import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id               import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref              import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id              import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref             import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source        import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id               import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology            import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Predicate import Schema__Ontology__Predicate
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text          import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                      import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                        import type_safe


class Ontology__Registry(Type_Safe):                                                  # Registry for ontology definitions
    ontologies_by_ref : Dict__Ontologies__By_Ref                                      # Lookup by reference name
    ontologies_by_id  : Dict__Ontologies__By_Id                                       # Lookup by instance ID

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory methods for creating ontologies with different ID modes
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_with__random_id(self                                ,
                               ontology_ref  : Ontology_Ref        ,
                               taxonomy_id   : Taxonomy_Id         = None,
                               description   : Safe_Str__Text      = None,
                               node_types    : Dict__Node_Types__By_Id  = None,
                               predicates    : Dict__Predicates__By_Id  = None,
                               edge_rules    : List__Edge_Rules         = None) -> Schema__Ontology:
        ontology_id = Ontology_Id(Obj_Id())                                           # Random ID
        ontology    = Schema__Ontology(ontology_id   = ontology_id                            ,
                                       ontology_ref  = ontology_ref                           ,
                                       taxonomy_id   = taxonomy_id                            ,
                                       description   = description   or Safe_Str__Text()      ,
                                       node_types    = node_types    or Dict__Node_Types__By_Id(),
                                       predicates    = predicates    or Dict__Predicates__By_Id(),
                                       edge_rules    = edge_rules    or List__Edge_Rules()       )
        self.register(ontology)
        return ontology

    @type_safe
    def create_with__deterministic_id(self                                ,
                                      ontology_ref  : Ontology_Ref        ,
                                      seed          : Safe_Str__Id__Seed  ,
                                      taxonomy_id   : Taxonomy_Id         = None,
                                      description   : Safe_Str__Text      = None,
                                      node_types    : Dict__Node_Types__By_Id  = None,
                                      predicates    : Dict__Predicates__By_Id  = None,
                                      edge_rules    : List__Edge_Rules         = None) -> Schema__Ontology:
        ontology_id        = Ontology_Id(Obj_Id.from_seed(seed))                      # Deterministic ID from seed
        ontology_id_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                                seed        = seed                    )
        ontology = Schema__Ontology(ontology_id        = ontology_id                          ,
                                    ontology_id_source = ontology_id_source                   ,
                                    ontology_ref       = ontology_ref                         ,
                                    taxonomy_id        = taxonomy_id                          ,
                                    description        = description   or Safe_Str__Text()    ,
                                    node_types         = node_types    or Dict__Node_Types__By_Id(),
                                    predicates         = predicates    or Dict__Predicates__By_Id(),
                                    edge_rules         = edge_rules    or List__Edge_Rules()       )
        self.register(ontology)
        return ontology

    @type_safe
    def create_with__explicit_id(self                                ,
                                 ontology_ref       : Ontology_Ref        ,
                                 ontology_id        : Ontology_Id         ,
                                 ontology_id_source : Schema__Id__Source  = None,
                                 taxonomy_id        : Taxonomy_Id         = None,
                                 description        : Safe_Str__Text      = None,
                                 node_types         : Dict__Node_Types__By_Id  = None,
                                 predicates         : Dict__Predicates__By_Id  = None,
                                 edge_rules         : List__Edge_Rules         = None) -> Schema__Ontology:
        ontology = Schema__Ontology(ontology_id        = ontology_id                          ,
                                    ontology_id_source = ontology_id_source                   ,
                                    ontology_ref       = ontology_ref                         ,
                                    taxonomy_id        = taxonomy_id                          ,
                                    description        = description   or Safe_Str__Text()    ,
                                    node_types         = node_types    or Dict__Node_Types__By_Id(),
                                    predicates         = predicates    or Dict__Predicates__By_Id(),
                                    edge_rules         = edge_rules    or List__Edge_Rules()       )
        self.register(ontology)
        return ontology

    # ═══════════════════════════════════════════════════════════════════════════
    # Registration and lookup
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def register(self, ontology: Schema__Ontology) -> Schema__Ontology:               # Register ontology in both indexes
        self.ontologies_by_ref[ontology.ontology_ref] = ontology
        if ontology.ontology_id:                                                      # Only index if ID is set
            self.ontologies_by_id[ontology.ontology_id] = ontology
        return ontology

    @type_safe
    def get_by_ref(self, ontology_ref: Ontology_Ref) -> Schema__Ontology:             # Lookup by reference name
        return self.ontologies_by_ref.get(ontology_ref)

    @type_safe
    def get_by_id(self, ontology_id: Ontology_Id) -> Schema__Ontology:                # Lookup by instance ID
        return self.ontologies_by_id.get(ontology_id)

    @type_safe
    def has_ref(self, ontology_ref: Ontology_Ref) -> bool:                            # Check if ref exists
        return ontology_ref in self.ontologies_by_ref

    @type_safe
    def has_id(self, ontology_id: Ontology_Id) -> bool:                               # Check if ID exists
        return ontology_id in self.ontologies_by_id

    @type_safe
    def all_refs(self) -> List__Ontology_Refs:                                        # All registered refs
        result = List__Ontology_Refs()
        for ref in self.ontologies_by_ref.keys():
            result.append(ref)
        return result

    @type_safe
    def all_ids(self) -> List__Ontology_Ids:                                          # All registered IDs
        result = List__Ontology_Ids()
        for id in self.ontologies_by_id.keys():
            result.append(id)
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
        for predicate in ontology.predicates.values():                                # Linear scan - could optimize with index
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
        for node_type in ontology.node_types.values():                                # Linear scan - could optimize with index
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

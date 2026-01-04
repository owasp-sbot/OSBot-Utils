# ═══════════════════════════════════════════════════════════════════════════════
# Ontology__Registry - Registry for ontology definitions with factory methods
# Provides lookup by ref (name) and by id (instance identifier)
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Ref  import Dict__Node_Types__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Ontologies__By_Id   import Dict__Ontologies__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Ontologies__By_Ref  import Dict__Ontologies__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Ontology_Ids        import List__Ontology_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Ontology_Refs       import List__Ontology_Refs
from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type           import Enum__Id__Source_Type
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id               import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref              import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source        import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref              import Taxonomy_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology            import Schema__Ontology
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text          import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version       import Safe_Str__Version
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
                               taxonomy_ref  : Taxonomy_Ref        ,
                               description   : Safe_Str__Text      = None,
                               version       : Safe_Str__Version   = None,
                               node_types    : Dict__Node_Types__By_Ref = None) -> Schema__Ontology:
        ontology_id = Ontology_Id(Obj_Id())                                           # Random ID
        ontology    = Schema__Ontology(ontology_id   = ontology_id                  ,
                                       ontology_ref  = ontology_ref                 ,
                                       taxonomy_ref  = taxonomy_ref                 ,
                                       description   = description   or Safe_Str__Text()        ,
                                       version       = version       or Safe_Str__Version('1.0.0'),
                                       node_types    = node_types    or Dict__Node_Types__By_Ref())
        self.register(ontology)
        return ontology

    @type_safe
    def create_with__deterministic_id(self                                ,
                                      ontology_ref  : Ontology_Ref        ,
                                      taxonomy_ref  : Taxonomy_Ref        ,
                                      seed          : Safe_Str__Id__Seed  ,
                                      description   : Safe_Str__Text      = None,
                                      version       : Safe_Str__Version   = None,
                                      node_types    : Dict__Node_Types__By_Ref = None) -> Schema__Ontology:
        ontology_id        = Ontology_Id(Obj_Id.from_seed(seed))                      # Deterministic ID from seed
        ontology_id_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                                seed        = seed                    )
        ontology = Schema__Ontology(ontology_id        = ontology_id                ,
                                    ontology_id_source = ontology_id_source         ,
                                    ontology_ref       = ontology_ref               ,
                                    taxonomy_ref       = taxonomy_ref               ,
                                    description        = description   or Safe_Str__Text()        ,
                                    version            = version       or Safe_Str__Version('1.0.0'),
                                    node_types         = node_types    or Dict__Node_Types__By_Ref())
        self.register(ontology)
        return ontology

    @type_safe
    def create_with__explicit_id(self                                ,
                                 ontology_ref       : Ontology_Ref        ,
                                 taxonomy_ref       : Taxonomy_Ref        ,
                                 ontology_id        : Ontology_Id         ,
                                 ontology_id_source : Schema__Id__Source  = None,
                                 description        : Safe_Str__Text      = None,
                                 version            : Safe_Str__Version   = None,
                                 node_types         : Dict__Node_Types__By_Ref = None) -> Schema__Ontology:
        ontology = Schema__Ontology(ontology_id        = ontology_id                ,
                                    ontology_id_source = ontology_id_source         ,
                                    ontology_ref       = ontology_ref               ,
                                    taxonomy_ref       = taxonomy_ref               ,
                                    description        = description   or Safe_Str__Text()        ,
                                    version            = version       or Safe_Str__Version('1.0.0'),
                                    node_types         = node_types    or Dict__Node_Types__By_Ref())
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

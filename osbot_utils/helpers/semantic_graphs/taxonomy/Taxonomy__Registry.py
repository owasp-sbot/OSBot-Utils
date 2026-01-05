# ═══════════════════════════════════════════════════════════════════════════════
# Taxonomy__Registry - Registry for taxonomy definitions with factory methods
#
# Updated for Brief 3.8:
#   - ID-based lookup is primary (get_by_id)
#   - get_by_ref still available for convenience
#   - Factory methods use ID-based Schema__Taxonomy
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Id   import Dict__Categories__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Taxonomies__By_Id   import Dict__Taxonomies__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Taxonomies__By_Ref  import Dict__Taxonomies__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Taxonomy_Ids        import List__Taxonomy_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Taxonomy_Refs       import List__Taxonomy_Refs
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id               import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type           import Enum__Id__Source_Type
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source        import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id               import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref              import Taxonomy_Ref
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy            import Schema__Taxonomy
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version       import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                      import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                        import type_safe


class Taxonomy__Registry(Type_Safe):                                                  # Registry for taxonomy definitions
    taxonomies_by_id  : Dict__Taxonomies__By_Id                                       # Primary: lookup by instance ID
    taxonomies_by_ref : Dict__Taxonomies__By_Ref                                      # Secondary: lookup by reference name

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory methods for creating taxonomies with different ID modes
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_with__random_id(self                                ,
                               taxonomy_ref : Taxonomy_Ref         ,
                               root_id      : Category_Id          ,
                               version      : Safe_Str__Version   = None,
                               categories   : Dict__Categories__By_Id = None) -> Schema__Taxonomy:
        taxonomy_id = Taxonomy_Id(Obj_Id())                                           # Random ID
        taxonomy    = Schema__Taxonomy(taxonomy_id  = taxonomy_id                   ,
                                       taxonomy_ref = taxonomy_ref                  ,
                                       root_id      = root_id                       ,
                                       version      = version    or Safe_Str__Version('1.0.0'),
                                       categories   = categories or Dict__Categories__By_Id())
        self.register(taxonomy)
        return taxonomy

    @type_safe
    def create_with__deterministic_id(self                                ,
                                      taxonomy_ref : Taxonomy_Ref         ,
                                      root_id      : Category_Id          ,
                                      seed         : Safe_Str__Id__Seed   ,
                                      version      : Safe_Str__Version   = None,
                                      categories   : Dict__Categories__By_Id = None) -> Schema__Taxonomy:
        taxonomy_id        = Taxonomy_Id(Obj_Id.from_seed(seed))                      # Deterministic ID from seed
        taxonomy_id_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                                seed        = seed                    )
        taxonomy = Schema__Taxonomy(taxonomy_id        = taxonomy_id                ,
                                    taxonomy_id_source = taxonomy_id_source         ,
                                    taxonomy_ref       = taxonomy_ref               ,
                                    root_id            = root_id                    ,
                                    version            = version    or Safe_Str__Version('1.0.0'),
                                    categories         = categories or Dict__Categories__By_Id())
        self.register(taxonomy)
        return taxonomy

    @type_safe
    def create_with__explicit_id(self                                     ,
                                 taxonomy_ref       : Taxonomy_Ref        ,
                                 root_id            : Category_Id         ,
                                 taxonomy_id        : Taxonomy_Id         ,
                                 taxonomy_id_source : Schema__Id__Source = None,
                                 version            : Safe_Str__Version  = None,
                                 categories         : Dict__Categories__By_Id = None) -> Schema__Taxonomy:
        taxonomy = Schema__Taxonomy(taxonomy_id        = taxonomy_id                ,
                                    taxonomy_id_source = taxonomy_id_source         ,
                                    taxonomy_ref       = taxonomy_ref               ,
                                    root_id            = root_id                    ,
                                    version            = version    or Safe_Str__Version('1.0.0'),
                                    categories         = categories or Dict__Categories__By_Id())
        self.register(taxonomy)
        return taxonomy

    # ═══════════════════════════════════════════════════════════════════════════
    # Registration and lookup
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def register(self, taxonomy: Schema__Taxonomy) -> Schema__Taxonomy:               # Register taxonomy in both indexes
        if taxonomy.taxonomy_id:                                                      # Primary index by ID
            self.taxonomies_by_id[taxonomy.taxonomy_id] = taxonomy
        self.taxonomies_by_ref[taxonomy.taxonomy_ref] = taxonomy                      # Secondary index by ref
        return taxonomy

    @type_safe
    def get_by_id(self, taxonomy_id: Taxonomy_Id) -> Schema__Taxonomy:                # Primary: lookup by instance ID
        return self.taxonomies_by_id.get(taxonomy_id)

    @type_safe
    def get_by_ref(self, taxonomy_ref: Taxonomy_Ref) -> Schema__Taxonomy:             # Secondary: lookup by reference name
        return self.taxonomies_by_ref.get(taxonomy_ref)

    @type_safe
    def has_id(self, taxonomy_id: Taxonomy_Id) -> bool:                               # Check if ID exists
        return taxonomy_id in self.taxonomies_by_id

    @type_safe
    def has_ref(self, taxonomy_ref: Taxonomy_Ref) -> bool:                            # Check if ref exists
        return taxonomy_ref in self.taxonomies_by_ref

    @type_safe
    def all_ids(self) -> List__Taxonomy_Ids:                                          # All registered IDs
        result = List__Taxonomy_Ids()
        for id in self.taxonomies_by_id.keys():
            result.append(id)
        return result

    @type_safe
    def all_refs(self) -> List__Taxonomy_Refs:                                        # All registered refs
        result = List__Taxonomy_Refs()
        for ref in self.taxonomies_by_ref.keys():
            result.append(ref)
        return result

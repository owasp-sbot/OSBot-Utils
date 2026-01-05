# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Taxonomy - Complete taxonomy definition (pure data)
#
# Updated for Brief 3.8:
#   - Uses root_id (not root_category ref)
#   - Uses Dict__Categories__By_Id (not By_Ref)
#   - Removed 'description' field
#
# Fields:
#   - taxonomy_id + taxonomy_id_source: Instance identity with provenance
#   - taxonomy_ref: Human-readable reference name for lookup
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Id import Dict__Categories__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id             import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source      import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id             import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref            import Taxonomy_Ref
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version     import Safe_Str__Version


class Schema__Taxonomy(Type_Safe):                                                   # Complete taxonomy definition
    taxonomy_id        : Taxonomy_Id                                                 # Unique instance identifier
    taxonomy_id_source : Schema__Id__Source      = None                              # ID provenance (optional sidecar)
    taxonomy_ref       : Taxonomy_Ref                                                # Human-readable reference name
    version            : Safe_Str__Version       = '1.0.0'                           # Semantic version
    root_id            : Category_Id                                                 # FK to root category
    categories         : Dict__Categories__By_Id                                     # Category_Id → category

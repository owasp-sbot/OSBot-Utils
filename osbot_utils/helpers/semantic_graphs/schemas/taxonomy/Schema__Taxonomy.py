# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Taxonomy - Complete taxonomy definition (pure data)
# Business logic has been moved to Taxonomy__Utils
#
# Fields:
#   - taxonomy_id + taxonomy_id_source: Instance identity with provenance
#   - taxonomy_ref: Human-readable reference name for lookup
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Ref import Dict__Categories__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref             import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source       import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id              import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref             import Taxonomy_Ref
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text         import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version      import Safe_Str__Version


class Schema__Taxonomy(Type_Safe):                                                   # Complete taxonomy definition
    taxonomy_id        : Taxonomy_Id                                                 # Unique instance identifier
    taxonomy_id_source : Schema__Id__Source      = None                              # ID provenance (optional sidecar)
    taxonomy_ref       : Taxonomy_Ref                                                # Human-readable reference name
    version            : Safe_Str__Version       = '1.0.0'                           # Semantic version
    description        : Safe_Str__Text                                              # What this taxonomy classifies
    root_category      : Category_Ref                                                # Top-level category ref
    categories         : Dict__Categories__By_Ref                                    # ref → category

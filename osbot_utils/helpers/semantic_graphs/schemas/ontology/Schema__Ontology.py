# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Ontology - Complete ontology definition (pure data)
# Business logic has been moved to Ontology__Utils
#
# Fields:
#   - ontology_id + ontology_id_source: Instance identity with provenance
#   - ontology_ref: Human-readable reference name for lookup
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Ref import Dict__Node_Types__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id              import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref             import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source       import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref             import Taxonomy_Ref
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text         import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version      import Safe_Str__Version


class Schema__Ontology(Type_Safe):                                                   # Complete ontology definition
    ontology_id        : Ontology_Id                                                 # Unique instance identifier
    ontology_id_source : Schema__Id__Source      = None                              # ID provenance (optional sidecar)
    ontology_ref       : Ontology_Ref                                                # Human-readable reference name
    version            : Safe_Str__Version       = '1.0.0'                           # Semantic version
    description        : Safe_Str__Text                                              # What this ontology models
    taxonomy_ref       : Taxonomy_Ref                                                # Reference to taxonomy
    node_types         : Dict__Node_Types__By_Ref                                    # type_ref → definition

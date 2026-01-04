# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Id__Source - Provenance information for instance IDs
# Tracks how an ID was created (random, deterministic, sequential, explicit)
# Used as sidecar field: node_id + node_id_source, ontology_id + ontology_id_source
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type          import Enum__Id__Source_Type
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe


class Schema__Id__Source(Type_Safe):                                                 # ID provenance information
    source_type : Enum__Id__Source_Type                                              # How the ID was created
    seed        : Safe_Str__Id__Seed                                                 # Seed string (empty for RANDOM/SEQUENTIAL/EXPLICIT)

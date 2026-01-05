# ═══════════════════════════════════════════════════════════════════════════════
# Enum__Id__Source_Type - How an instance ID was created
# Used with Schema__Id__Source for provenance tracking
# ═══════════════════════════════════════════════════════════════════════════════
from enum import Enum


class Enum__Id__Source_Type(str, Enum):                                              # Source type for ID creation
    RANDOM        = 'random'                                                         # Created via Obj_Id() - random each time
    DETERMINISTIC = 'deterministic'                                                  # Created via Obj_Id.from_seed() - same seed → same ID
    SEQUENTIAL    = 'sequential'                                                     # Created inside graph_deterministic_ids() context
    EXPLICIT      = 'explicit'                                                       # Provided directly (e.g., from storage)
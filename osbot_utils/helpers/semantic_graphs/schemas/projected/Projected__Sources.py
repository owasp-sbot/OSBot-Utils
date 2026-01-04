# ═══════════════════════════════════════════════════════════════════════════════
# Projected__Sources - Provenance information
#
# Tracks where this projection came from, enabling tracing back to the
# original Schema__ data for debugging and auditing.
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                   import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed
from osbot_utils.type_safe.primitives.domains.identifiers.Timestamp_Now              import Timestamp_Now


class Projected__Sources(Type_Safe):                                                 # Projection provenance
    source_graph_id : Graph_Id                                                       # The Schema__ graph that was projected
    ontology_seed   : Safe_Str__Id__Seed = None                                      # Ontology identity seed (if deterministic)
    generated_at    : Timestamp_Now                                                  # When projection was created

# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Ontology - Complete ontology definition (pure data)
#
# Ontologies define the vocabulary for semantic graphs:
#   - node_types: What kinds of nodes can exist
#   - predicates: What relationships (edges) can exist
#   - edge_rules: Which node types can be connected by which predicates
#
# Fields:
#   - ontology_id + ontology_id_source: Instance identity with provenance
#   - ontology_ref: Human-readable reference name for lookup
#   - taxonomy_id: Foreign key to taxonomy definition
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id  import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicates__By_Id  import Dict__Predicates__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Edge_Rules         import List__Edge_Rules
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id              import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref             import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source       import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id              import Taxonomy_Id
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text         import Safe_Str__Text


class Schema__Ontology(Type_Safe):                                                   # Complete ontology definition
    ontology_id        : Ontology_Id                                                 # Unique instance identifier
    ontology_id_source : Schema__Id__Source      = None                              # ID provenance (optional sidecar)
    ontology_ref       : Ontology_Ref                                                # Human-readable reference name
    description        : Safe_Str__Text          = None                              # What this ontology models
    taxonomy_id        : Taxonomy_Id             = None                              # Foreign key to taxonomy
    node_types         : Dict__Node_Types__By_Id                                     # Node_Type_Id → definition
    predicates         : Dict__Predicates__By_Id                                     # Predicate_Id → definition
    edge_rules         : List__Edge_Rules                                            # Valid edge constraints

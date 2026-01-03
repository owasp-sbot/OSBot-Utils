# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Ontology - Complete ontology definition (pure data)
# Business logic has been moved to Ontology__Utils
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id             import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id             import Taxonomy_Id
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version     import Safe_Str__Version

# todo: questions
#     :
#       - what are we using the Taxonomy_Id for?
#       - we need to move the default version into a config value and should it be 1.0.0 or v1.0.0 or v0.0.1
#       - review how we can make this more compatible with existing Ontologies and Taxonomies that use URIs
#       - review the value of adding actually IDs (like Node_ID) which are unique Obj_Ids
#           (for example we could make Ontology_Id(Node_Id) and have Ontology_Ref(Semantic_Id), which probably would be Ontology_Ref(Semantic_Ref)

class Schema__Ontology(Type_Safe):                                                   # Complete ontology definition
    ontology_id  : Ontology_Id                                                       # Unique identifier
    version      : Safe_Str__Version = '1.0.0'                                       # Semantic version
    description  : Safe_Str__Text                                                    # What this ontology models
    taxonomy_ref : Taxonomy_Id                                                       # taxonomy reference
    node_types   : Dict__Node_Types__By_Id                                           # type_id → definition

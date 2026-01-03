# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Taxonomy - Complete taxonomy definition (pure data)
# Business logic has been moved to Taxonomy__Utils
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Id import Dict__Categories__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id             import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id             import Taxonomy_Id
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version     import Safe_Str__Version


# todo: questions
#     :
#       - see equivalent questions in 'Schema__Ontology' todo

class Schema__Taxonomy(Type_Safe):                                                   # Complete taxonomy definition
    taxonomy_id   : Taxonomy_Id                                                      # Unique identifier
    version       : Safe_Str__Version = '1.0.0'                                      # Semantic version
    description   : Safe_Str__Text                                                   # What this taxonomy classifies
    root_category : Category_Id                                                      # Top-level category
    categories    : Dict__Categories__By_Id                                          # id → category

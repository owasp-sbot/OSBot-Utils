# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Property_Types__By_Id - Maps property type IDs to definitions
# Used by Schema__Ontology for property type storage
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Id             import Property_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Property_Type import Schema__Ontology__Property_Type
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                    import Type_Safe__Dict


class Dict__Property_Types__By_Id(Type_Safe__Dict):                                  # Maps property type IDs to definitions
    expected_key_type   = Property_Type_Id
    expected_value_type = Schema__Ontology__Property_Type

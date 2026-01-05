# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Property_Names__By_Id - Maps property name IDs to definitions
# Used by Schema__Ontology for property name storage
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id             import Property_Name_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Property_Name import Schema__Ontology__Property_Name
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                    import Type_Safe__Dict


class Dict__Property_Names__By_Id(Type_Safe__Dict):                                  # Maps property name IDs to definitions
    expected_key_type   = Property_Name_Id
    expected_value_type = Schema__Ontology__Property_Name

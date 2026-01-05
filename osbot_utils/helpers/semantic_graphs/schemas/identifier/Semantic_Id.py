# ═══════════════════════════════════════════════════════════════════════════════
# Semantic_Id - Base class for all semantic graph instance IDs
# Parent class for Node_Id, Edge_Id, Graph_Id, Ontology_Id, Taxonomy_Id, Rule_Set_Id
#
# IMPORTANT: This is for INSTANCE IDs (unique per object)
#            NOT for references (use Semantic_Ref for human-readable labels)
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                     import Obj_Id


class Semantic_Id(Obj_Id):                                                           # Base for all instance IDs
    def __new__(cls, value=None):                                                    # Allow empty values
        if value is None or value == '':                                             # Empty case
            return str.__new__(cls, '')                                              # Create empty string
        else:
            return super().__new__(cls, value)                                       # Delegate to Obj_Id

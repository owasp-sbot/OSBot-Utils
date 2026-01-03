from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id            import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb  import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


class Schema__Rule__Transitivity(Type_Safe):                                         # Transitivity rule
    source_type : Node_Type_Id                                                       # e.g., "class"
    verb        : Safe_Str__Ontology__Verb                                           # e.g., "inherits_from"
    target_type : Node_Type_Id                                                       # e.g., "class"

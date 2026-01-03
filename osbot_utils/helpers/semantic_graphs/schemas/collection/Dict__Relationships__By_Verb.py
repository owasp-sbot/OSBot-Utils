from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Relationship import Schema__Ontology__Relationship
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb       import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                    import Type_Safe__Dict


class Dict__Relationships__By_Verb(Type_Safe__Dict):                                     # Maps verbs to relationship definitions
    expected_key_type   = Safe_Str__Ontology__Verb
    expected_value_type = Schema__Ontology__Relationship
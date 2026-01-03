from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id   import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology import Schema__Ontology
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict      import Type_Safe__Dict


class Dict__Ontologies__By_Id(Type_Safe__Dict):                                          # Maps ontology IDs to ontology definitions
    expected_key_type   = Ontology_Id
    expected_value_type = Schema__Ontology
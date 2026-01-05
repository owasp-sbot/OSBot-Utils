# ═══════════════════════════════════════════════════════════════════════════════
# Rule__Engine - Registry for rule set definitions with factory methods
# Provides lookup by ref (name) and by id (instance identifier)
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Rule_Sets__By_Id    import Dict__Rule_Sets__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Rule_Sets__By_Ref   import Dict__Rule_Sets__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rule_Set_Ids        import List__Rule_Set_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rule_Set_Refs       import List__Rule_Set_Refs
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Cardinality  import List__Rules__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Transitivity import List__Rules__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type           import Enum__Id__Source_Type
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref              import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id               import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref              import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source        import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                import Schema__Rule_Set
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text          import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version       import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                      import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                        import type_safe


class Rule__Engine(Type_Safe):                                                        # Registry for rule set definitions
    rule_sets_by_ref : Dict__Rule_Sets__By_Ref                                        # Lookup by reference name
    rule_sets_by_id  : Dict__Rule_Sets__By_Id                                         # Lookup by instance ID

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory methods for creating rule sets with different ID modes
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_with__random_id(self                                                ,
                               rule_set_ref      : Rule_Set_Ref                    ,
                               ontology_id       : Ontology_Id                     ,
                               version           : Safe_Str__Version         = None,
                               transitivity_rules: List__Rules__Transitivity = None,
                               cardinality_rules : List__Rules__Cardinality  = None) -> Schema__Rule_Set:
        rule_set_id = Rule_Set_Id(Obj_Id())                                           # Random ID
        rule_set    = Schema__Rule_Set(rule_set_id        = rule_set_id             ,
                                       rule_set_ref       = rule_set_ref            ,
                                       ontology_id        = ontology_id            ,
                                       version            = version            or Safe_Str__Version('1.0.0'),
                                       transitivity_rules = transitivity_rules or List__Rules__Transitivity(),
                                       cardinality_rules  = cardinality_rules  or List__Rules__Cardinality() )
        self.register(rule_set)
        return rule_set

    @type_safe
    def create_with__deterministic_id(self                                      ,
                                      rule_set_ref      : Rule_Set_Ref          ,
                                      ontology_id       : Ontology_Id           ,
                                      seed              : Safe_Str__Id__Seed    ,
                                      version           : Safe_Str__Version     = None,
                                      transitivity_rules: List__Rules__Transitivity = None,
                                      cardinality_rules : List__Rules__Cardinality  = None) -> Schema__Rule_Set:
        rule_set_id        = Rule_Set_Id(Obj_Id.from_seed(seed))                      # Deterministic ID from seed
        rule_set_id_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                                seed        = seed                    )
        rule_set = Schema__Rule_Set(rule_set_id        = rule_set_id                ,
                                    rule_set_id_source = rule_set_id_source         ,
                                    rule_set_ref       = rule_set_ref               ,
                                    ontology_id        = ontology_id                ,
                                    version            = version            or Safe_Str__Version('1.0.0'),
                                    transitivity_rules = transitivity_rules or List__Rules__Transitivity(),
                                    cardinality_rules  = cardinality_rules  or List__Rules__Cardinality() )
        self.register(rule_set)
        return rule_set

    @type_safe
    def create_with__explicit_id(self                                      ,
                                 rule_set_ref       : Rule_Set_Ref          ,
                                 ontology_id        : Ontology_Id          ,
                                 rule_set_id        : Rule_Set_Id           ,
                                 rule_set_id_source : Schema__Id__Source    = None,
                                 version            : Safe_Str__Version     = None,
                                 transitivity_rules : List__Rules__Transitivity = None,
                                 cardinality_rules  : List__Rules__Cardinality  = None) -> Schema__Rule_Set:
        rule_set = Schema__Rule_Set(rule_set_id        = rule_set_id                ,
                                    rule_set_id_source = rule_set_id_source         ,
                                    rule_set_ref       = rule_set_ref               ,
                                    ontology_id        = ontology_id                ,
                                    version            = version            or Safe_Str__Version('1.0.0'),
                                    transitivity_rules = transitivity_rules or List__Rules__Transitivity(),
                                    cardinality_rules  = cardinality_rules  or List__Rules__Cardinality() )
        self.register(rule_set)
        return rule_set

    # ═══════════════════════════════════════════════════════════════════════════
    # Registration and lookup
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def register(self, rule_set: Schema__Rule_Set) -> Schema__Rule_Set:               # Register rule set in both indexes
        self.rule_sets_by_ref[rule_set.rule_set_ref] = rule_set
        if rule_set.rule_set_id:                                                      # Only index if ID is set
            self.rule_sets_by_id[rule_set.rule_set_id] = rule_set
        return rule_set

    @type_safe
    def get_by_ref(self, rule_set_ref: Rule_Set_Ref) -> Schema__Rule_Set:             # Lookup by reference name
        return self.rule_sets_by_ref.get(rule_set_ref)

    @type_safe
    def get_by_id(self, rule_set_id: Rule_Set_Id) -> Schema__Rule_Set:                # Lookup by instance ID
        return self.rule_sets_by_id.get(rule_set_id)

    @type_safe
    def has_ref(self, rule_set_ref: Rule_Set_Ref) -> bool:                            # Check if ref exists
        return rule_set_ref in self.rule_sets_by_ref

    @type_safe
    def has_id(self, rule_set_id: Rule_Set_Id) -> bool:                               # Check if ID exists
        return rule_set_id in self.rule_sets_by_id

    @type_safe
    def all_refs(self) -> List__Rule_Set_Refs:                                        # All registered refs
        result = List__Rule_Set_Refs()
        for ref in self.rule_sets_by_ref.keys():
            result.append(ref)
        return result

    @type_safe
    def all_ids(self) -> List__Rule_Set_Ids:                                          # All registered IDs
        result = List__Rule_Set_Ids()
        for id in self.rule_sets_by_id.keys():
            result.append(id)
        return result

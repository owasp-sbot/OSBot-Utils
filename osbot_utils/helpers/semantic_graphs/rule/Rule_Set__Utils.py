# ═══════════════════════════════════════════════════════════════════════════════
# Rule_Set__Utils - Operations on Schema__Rule_Set (business logic)
#
# Updated for Brief 3.8:
#   - Added required property validation for nodes and edges
#   - Added rule lookup methods (get_required_node_property, etc.)
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph           import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge     import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node     import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id            import Property_Name_Id
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                  import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Node_Property import Schema__Rule__Required_Node_Property
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Edge_Property import Schema__Rule__Required_Edge_Property
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                          import type_safe


class Rule_Set__Utils(Type_Safe):                                                      # Operations on rule set schemas

    # ═══════════════════════════════════════════════════════════════════════════
    # Required Node Property Queries
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_required_node_property(self                           ,
                                   rule_set         : Schema__Rule_Set   ,
                                   node_type_id     : Node_Type_Id       ,
                                   property_name_id : Property_Name_Id   ) -> Schema__Rule__Required_Node_Property:
        for rule in rule_set.required_node_properties:                                # Get specific rule
            if rule.node_type_id == node_type_id and rule.property_name_id == property_name_id:
                return rule
        return None

    @type_safe
    def is_node_property_required(self                           ,
                                  rule_set         : Schema__Rule_Set   ,
                                  node_type_id     : Node_Type_Id       ,
                                  property_name_id : Property_Name_Id   ) -> bool:
        rule = self.get_required_node_property(rule_set, node_type_id, property_name_id)
        if rule is None:
            return False
        return rule.required if hasattr(rule, 'required') else True

    @type_safe
    def get_required_properties_for_node_type(self                       ,
                                              rule_set     : Schema__Rule_Set,
                                              node_type_id : Node_Type_Id    ) -> list:
        result = []                                                                   # Get required property IDs for node type
        for rule in rule_set.required_node_properties:
            if rule.node_type_id == node_type_id:
                result.append(rule.property_name_id)
        return result

    @type_safe
    def has_required_node_property_rule(self                           ,
                                        rule_set         : Schema__Rule_Set   ,
                                        node_type_id     : Node_Type_Id       ,
                                        property_name_id : Property_Name_Id   ) -> bool:
        for rule in rule_set.required_node_properties:                                # Check if rule exists
            if rule.node_type_id == node_type_id and rule.property_name_id == property_name_id:
                return True
        return False

    # ═══════════════════════════════════════════════════════════════════════════
    # Required Edge Property Queries
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_required_edge_property(self                           ,
                                   rule_set         : Schema__Rule_Set   ,
                                   predicate_id     : Predicate_Id       ,
                                   property_name_id : Property_Name_Id   ) -> Schema__Rule__Required_Edge_Property:
        for rule in rule_set.required_edge_properties:                                # Get specific rule
            if rule.predicate_id == predicate_id and rule.property_name_id == property_name_id:
                return rule
        return None

    @type_safe
    def is_edge_property_required(self                           ,
                                  rule_set         : Schema__Rule_Set   ,
                                  predicate_id     : Predicate_Id       ,
                                  property_name_id : Property_Name_Id   ) -> bool:
        rule = self.get_required_edge_property(rule_set, predicate_id, property_name_id)
        if rule is None:
            return False
        return rule.required if hasattr(rule, 'required') else True

    @type_safe
    def get_required_properties_for_predicate(self                      ,
                                              rule_set     : Schema__Rule_Set,
                                              predicate_id : Predicate_Id    ) -> list:
        result = []                                                                   # Get required property IDs for predicate
        for rule in rule_set.required_edge_properties:
            if rule.predicate_id == predicate_id:
                result.append(rule.property_name_id)
        return result

    @type_safe
    def has_required_edge_property_rule(self                           ,
                                        rule_set         : Schema__Rule_Set   ,
                                        predicate_id     : Predicate_Id       ,
                                        property_name_id : Property_Name_Id   ) -> bool:
        for rule in rule_set.required_edge_properties:                                # Check if rule exists
            if rule.predicate_id == predicate_id and rule.property_name_id == property_name_id:
                return True
        return False

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Property Validation
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def validate_node_properties(self                   ,
                                 rule_set : Schema__Rule_Set            ,
                                 node     : Schema__Semantic_Graph__Node) -> list:
        violations = []                                                               # Validate node has required properties
        required   = self.get_required_properties_for_node_type(rule_set, node.node_type_id)
        for prop_id in required:
            if node.properties is None or prop_id not in node.properties:
                violations.append({
                    'node_id'          : node.node_id         ,
                    'node_type_id'     : node.node_type_id    ,
                    'missing_property' : prop_id              ,
                    'rule_type'        : 'required_node_property'
                })
        return violations

    @type_safe
    def validate_all_node_properties(self                    ,
                                     rule_set : Schema__Rule_Set     ,
                                     graph    : Schema__Semantic_Graph) -> list:
        all_violations = []                                                           # Validate all nodes in graph
        for node in graph.nodes.values():
            violations = self.validate_node_properties(rule_set, node)
            all_violations.extend(violations)
        return all_violations

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Property Validation
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def validate_edge_properties(self                   ,
                                 rule_set : Schema__Rule_Set            ,
                                 edge     : Schema__Semantic_Graph__Edge) -> list:
        violations = []                                                               # Validate edge has required properties
        required   = self.get_required_properties_for_predicate(rule_set, edge.predicate_id)
        for prop_id in required:
            if edge.properties is None or prop_id not in edge.properties:
                violations.append({
                    'edge_id'          : edge.edge_id        ,
                    'predicate_id'     : edge.predicate_id   ,
                    'missing_property' : prop_id             ,
                    'rule_type'        : 'required_edge_property'
                })
        return violations

    @type_safe
    def validate_all_edge_properties(self                    ,
                                     rule_set : Schema__Rule_Set     ,
                                     graph    : Schema__Semantic_Graph) -> list:
        all_violations = []                                                           # Validate all edges in graph
        for edge in graph.edges:
            violations = self.validate_edge_properties(rule_set, edge)
            all_violations.extend(violations)
        return all_violations

    # ═══════════════════════════════════════════════════════════════════════════
    # Combined Validation
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def validate_all_properties(self                    ,
                                rule_set : Schema__Rule_Set     ,
                                graph    : Schema__Semantic_Graph) -> list:
        violations = []                                                               # Validate all property rules
        violations.extend(self.validate_all_node_properties(rule_set, graph))
        violations.extend(self.validate_all_edge_properties(rule_set, graph))
        return violations

    @type_safe
    def is_property_compliant(self                    ,
                              rule_set : Schema__Rule_Set     ,
                              graph    : Schema__Semantic_Graph) -> bool:
        return len(self.validate_all_properties(rule_set, graph)) == 0                # Check if graph is property-compliant
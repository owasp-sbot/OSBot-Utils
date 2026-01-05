# ═══════════════════════════════════════════════════════════════════════════════
# QA__Semantic_Graphs__Test_Data - Comprehensive test data for Brief 3.8
#
# Provides factory methods for creating test fixtures:
#   - Taxonomy with ID-based categories
#   - Ontology with property names and property types
#   - Graphs with nodes and edges that have properties
#   - Expected projection outputs
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Registry                            import Ontology__Registry
from osbot_utils.helpers.semantic_graphs.taxonomy.Taxonomy__Registry                            import Taxonomy__Registry
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Builder                          import Semantic_Graph__Builder
from osbot_utils.helpers.semantic_graphs.projector.Semantic_Graph__Projector                    import Semantic_Graph__Projector
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Id             import Dict__Categories__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Edge_Properties               import Dict__Edge_Properties
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Properties               import Dict__Node_Properties
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id             import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicates__By_Id             import Dict__Predicates__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Names__By_Id         import Dict__Property_Names__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Types__By_Id         import Dict__Property_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Ids                  import List__Category_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Edge_Rules                    import List__Edge_Rules
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Cardinality            import List__Rules__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Required_Edge_Property import List__Rules__Required_Edge_Property
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Required_Node_Property import List__Rules__Required_Node_Property
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Transitivity           import List__Rules__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type                     import Enum__Id__Source_Type
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                         import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                        import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                        import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                       import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                         import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref                        import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                        import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref                       import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id                    import Property_Name_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Ref                   import Property_Name_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Id                    import Property_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Ref                   import Property_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                         import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref                        import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source                  import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                         import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref                        import Taxonomy_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                      import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Edge_Rule           import Schema__Ontology__Edge_Rule
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type           import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Predicate           import Schema__Ontology__Predicate
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Property_Name       import Schema__Ontology__Property_Name
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Property_Type       import Schema__Ontology__Property_Type
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                          import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Edge_Property      import Schema__Rule__Required_Edge_Property
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Node_Property      import Schema__Rule__Required_Node_Property
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy                      import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category            import Schema__Taxonomy__Category
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph                   import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id                  import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges         import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node             import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge             import Schema__Semantic_Graph__Edge
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                               import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                              import Graph_Id
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                    import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version                 import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                               import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                 import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed           import Safe_Str__Id__Seed
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                  import type_safe


class QA__Semantic_Graphs__Test_Data(Type_Safe):                                     # Test data factory for Brief 3.8

    # ═══════════════════════════════════════════════════════════════════════════
    # Deterministic Seeds for Reproducible Tests
    # ═══════════════════════════════════════════════════════════════════════════

    SEED__TAXONOMY          = Safe_Str__Id__Seed('test-taxonomy-code-analysis')
    SEED__ONTOLOGY          = Safe_Str__Id__Seed('test-ontology-code-analysis')
    SEED__GRAPH             = Safe_Str__Id__Seed('test-graph-sample')

    # Category seeds
    SEED__CAT_ROOT          = Safe_Str__Id__Seed('cat-root')
    SEED__CAT_CALLABLE      = Safe_Str__Id__Seed('cat-callable')
    SEED__CAT_CONTAINER     = Safe_Str__Id__Seed('cat-container')
    SEED__CAT_DATA          = Safe_Str__Id__Seed('cat-data')

    # Node type seeds
    SEED__NT_CLASS          = Safe_Str__Id__Seed('nt-class')
    SEED__NT_METHOD         = Safe_Str__Id__Seed('nt-method')
    SEED__NT_FUNCTION       = Safe_Str__Id__Seed('nt-function')
    SEED__NT_MODULE         = Safe_Str__Id__Seed('nt-module')
    SEED__NT_VARIABLE       = Safe_Str__Id__Seed('nt-variable')

    # Predicate seeds
    SEED__PRED_CONTAINS     = Safe_Str__Id__Seed('pred-contains')
    SEED__PRED_CONTAINED_BY = Safe_Str__Id__Seed('pred-contained-by')
    SEED__PRED_CALLS        = Safe_Str__Id__Seed('pred-calls')
    SEED__PRED_CALLED_BY    = Safe_Str__Id__Seed('pred-called-by')
    SEED__PRED_USES         = Safe_Str__Id__Seed('pred-uses')
    SEED__PRED_USED_BY      = Safe_Str__Id__Seed('pred-used-by')

    # Property type seeds
    SEED__PT_INTEGER        = Safe_Str__Id__Seed('pt-integer')
    SEED__PT_BOOLEAN        = Safe_Str__Id__Seed('pt-boolean')
    SEED__PT_STRING         = Safe_Str__Id__Seed('pt-string')

    # Property name seeds
    SEED__PN_LINE_NUMBER    = Safe_Str__Id__Seed('pn-line-number')
    SEED__PN_IS_ASYNC       = Safe_Str__Id__Seed('pn-is-async')
    SEED__PN_DOCSTRING      = Safe_Str__Id__Seed('pn-docstring')
    SEED__PN_CALL_COUNT     = Safe_Str__Id__Seed('pn-call-count')

    # Node seeds
    SEED__NODE_MODULE_MAIN  = Safe_Str__Id__Seed('node-module-main')
    SEED__NODE_CLASS_FOO    = Safe_Str__Id__Seed('node-class-foo')
    SEED__NODE_METHOD_BAR   = Safe_Str__Id__Seed('node-method-bar')
    SEED__NODE_FUNC_HELPER  = Safe_Str__Id__Seed('node-func-helper')

    # ═══════════════════════════════════════════════════════════════════════════
    # ID Generation Helpers
    # ═══════════════════════════════════════════════════════════════════════════

    def _id_from_seed(self, seed: Safe_Str__Id__Seed) -> Obj_Id:
        return Obj_Id.from_seed(seed)

    def _source_from_seed(self, seed: Safe_Str__Id__Seed) -> Schema__Id__Source:
        return Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                  seed        = seed                               )

    # ═══════════════════════════════════════════════════════════════════════════
    # Taxonomy Factory (ID-based per Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_taxonomy(self) -> Schema__Taxonomy:                                   # Create test taxonomy with ID-based refs
        # Create category IDs
        cat_root_id      = Category_Id(self._id_from_seed(self.SEED__CAT_ROOT))
        cat_callable_id  = Category_Id(self._id_from_seed(self.SEED__CAT_CALLABLE))
        cat_container_id = Category_Id(self._id_from_seed(self.SEED__CAT_CONTAINER))
        cat_data_id      = Category_Id(self._id_from_seed(self.SEED__CAT_DATA))

        # Create categories with ID-based parent/child references
        cat_root = Schema__Taxonomy__Category(
            category_id  = cat_root_id                                              ,
            category_ref = Category_Ref('code_element')                             ,
            parent_id    = None                                                     ,
            child_ids    = List__Category_Ids([cat_callable_id, cat_container_id, cat_data_id])
        )

        cat_callable = Schema__Taxonomy__Category(
            category_id  = cat_callable_id                                          ,
            category_ref = Category_Ref('callable')                                 ,
            parent_id    = cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )

        cat_container = Schema__Taxonomy__Category(
            category_id  = cat_container_id                                         ,
            category_ref = Category_Ref('container')                                ,
            parent_id    = cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )

        cat_data = Schema__Taxonomy__Category(
            category_id  = cat_data_id                                              ,
            category_ref = Category_Ref('data')                                     ,
            parent_id    = cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )

        # Build categories dict
        categories = Dict__Categories__By_Id()
        categories[cat_root_id]      = cat_root
        categories[cat_callable_id]  = cat_callable
        categories[cat_container_id] = cat_container
        categories[cat_data_id]      = cat_data

        return Schema__Taxonomy(
            taxonomy_id        = Taxonomy_Id(self._id_from_seed(self.SEED__TAXONOMY)),
            taxonomy_id_source = self._source_from_seed(self.SEED__TAXONOMY)        ,
            taxonomy_ref       = Taxonomy_Ref('code_analysis')                      ,
            version            = Safe_Str__Version('1.0.0')                         ,
            root_id            = cat_root_id                                        ,
            categories         = categories
        )

    @type_safe
    def create_taxonomy_registry(self) -> Taxonomy__Registry:                        # Create registry with test taxonomy
        registry = Taxonomy__Registry()
        taxonomy = self.create_taxonomy()
        registry.register(taxonomy)
        return registry

    # ═══════════════════════════════════════════════════════════════════════════
    # Property Types Factory
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_property_types(self) -> Dict__Property_Types__By_Id:                  # Create standard property types
        pt_integer = Schema__Ontology__Property_Type(
            property_type_id        = Property_Type_Id(self._id_from_seed(self.SEED__PT_INTEGER)),
            property_type_id_source = self._source_from_seed(self.SEED__PT_INTEGER)             ,
            property_type_ref       = Property_Type_Ref('integer')
        )

        pt_boolean = Schema__Ontology__Property_Type(
            property_type_id        = Property_Type_Id(self._id_from_seed(self.SEED__PT_BOOLEAN)),
            property_type_id_source = self._source_from_seed(self.SEED__PT_BOOLEAN)             ,
            property_type_ref       = Property_Type_Ref('boolean')
        )

        pt_string = Schema__Ontology__Property_Type(
            property_type_id        = Property_Type_Id(self._id_from_seed(self.SEED__PT_STRING)),
            property_type_id_source = self._source_from_seed(self.SEED__PT_STRING)             ,
            property_type_ref       = Property_Type_Ref('string')
        )

        result = Dict__Property_Types__By_Id()
        result[pt_integer.property_type_id] = pt_integer
        result[pt_boolean.property_type_id] = pt_boolean
        result[pt_string.property_type_id]  = pt_string
        return result

    # ═══════════════════════════════════════════════════════════════════════════
    # Property Names Factory
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_property_names(self, property_types: Dict__Property_Types__By_Id) -> Dict__Property_Names__By_Id:
        # Get type IDs
        integer_id = Property_Type_Id(self._id_from_seed(self.SEED__PT_INTEGER))
        boolean_id = Property_Type_Id(self._id_from_seed(self.SEED__PT_BOOLEAN))
        string_id  = Property_Type_Id(self._id_from_seed(self.SEED__PT_STRING))

        pn_line_number = Schema__Ontology__Property_Name(
            property_name_id        = Property_Name_Id(self._id_from_seed(self.SEED__PN_LINE_NUMBER)),
            property_name_id_source = self._source_from_seed(self.SEED__PN_LINE_NUMBER)             ,
            property_name_ref       = Property_Name_Ref('line_number')                              ,
            property_type_id        = integer_id
        )

        pn_is_async = Schema__Ontology__Property_Name(
            property_name_id        = Property_Name_Id(self._id_from_seed(self.SEED__PN_IS_ASYNC)),
            property_name_id_source = self._source_from_seed(self.SEED__PN_IS_ASYNC)             ,
            property_name_ref       = Property_Name_Ref('is_async')                              ,
            property_type_id        = boolean_id
        )

        pn_docstring = Schema__Ontology__Property_Name(
            property_name_id        = Property_Name_Id(self._id_from_seed(self.SEED__PN_DOCSTRING)),
            property_name_id_source = self._source_from_seed(self.SEED__PN_DOCSTRING)             ,
            property_name_ref       = Property_Name_Ref('docstring')                              ,
            property_type_id        = string_id
        )

        pn_call_count = Schema__Ontology__Property_Name(
            property_name_id        = Property_Name_Id(self._id_from_seed(self.SEED__PN_CALL_COUNT)),
            property_name_id_source = self._source_from_seed(self.SEED__PN_CALL_COUNT)             ,
            property_name_ref       = Property_Name_Ref('call_count')                              ,
            property_type_id        = integer_id
        )

        result = Dict__Property_Names__By_Id()
        result[pn_line_number.property_name_id] = pn_line_number
        result[pn_is_async.property_name_id]    = pn_is_async
        result[pn_docstring.property_name_id]   = pn_docstring
        result[pn_call_count.property_name_id]  = pn_call_count
        return result

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Types Factory (with category_id links)
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_node_types(self) -> Dict__Node_Types__By_Id:                          # Create node types with category links
        # Category IDs for linking
        cat_callable_id  = Category_Id(self._id_from_seed(self.SEED__CAT_CALLABLE))
        cat_container_id = Category_Id(self._id_from_seed(self.SEED__CAT_CONTAINER))
        cat_data_id      = Category_Id(self._id_from_seed(self.SEED__CAT_DATA))

        nt_class = Schema__Ontology__Node_Type(
            node_type_id        = Node_Type_Id(self._id_from_seed(self.SEED__NT_CLASS)),
            node_type_id_source = self._source_from_seed(self.SEED__NT_CLASS)         ,
            node_type_ref       = Node_Type_Ref('class')                              ,
            category_id         = cat_container_id
        )

        nt_method = Schema__Ontology__Node_Type(
            node_type_id        = Node_Type_Id(self._id_from_seed(self.SEED__NT_METHOD)),
            node_type_id_source = self._source_from_seed(self.SEED__NT_METHOD)         ,
            node_type_ref       = Node_Type_Ref('method')                              ,
            category_id         = cat_callable_id
        )

        nt_function = Schema__Ontology__Node_Type(
            node_type_id        = Node_Type_Id(self._id_from_seed(self.SEED__NT_FUNCTION)),
            node_type_id_source = self._source_from_seed(self.SEED__NT_FUNCTION)         ,
            node_type_ref       = Node_Type_Ref('function')                              ,
            category_id         = cat_callable_id
        )

        nt_module = Schema__Ontology__Node_Type(
            node_type_id        = Node_Type_Id(self._id_from_seed(self.SEED__NT_MODULE)),
            node_type_id_source = self._source_from_seed(self.SEED__NT_MODULE)         ,
            node_type_ref       = Node_Type_Ref('module')                              ,
            category_id         = cat_container_id
        )

        nt_variable = Schema__Ontology__Node_Type(
            node_type_id        = Node_Type_Id(self._id_from_seed(self.SEED__NT_VARIABLE)),
            node_type_id_source = self._source_from_seed(self.SEED__NT_VARIABLE)         ,
            node_type_ref       = Node_Type_Ref('variable')                              ,
            category_id         = cat_data_id
        )

        result = Dict__Node_Types__By_Id()
        result[nt_class.node_type_id]    = nt_class
        result[nt_method.node_type_id]   = nt_method
        result[nt_function.node_type_id] = nt_function
        result[nt_module.node_type_id]   = nt_module
        result[nt_variable.node_type_id] = nt_variable
        return result

    # ═══════════════════════════════════════════════════════════════════════════
    # Predicates Factory
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_predicates(self) -> Dict__Predicates__By_Id:                          # Create predicates with inverse links
        contains_id     = Predicate_Id(self._id_from_seed(self.SEED__PRED_CONTAINS))
        contained_by_id = Predicate_Id(self._id_from_seed(self.SEED__PRED_CONTAINED_BY))
        calls_id        = Predicate_Id(self._id_from_seed(self.SEED__PRED_CALLS))
        called_by_id    = Predicate_Id(self._id_from_seed(self.SEED__PRED_CALLED_BY))
        uses_id         = Predicate_Id(self._id_from_seed(self.SEED__PRED_USES))
        used_by_id      = Predicate_Id(self._id_from_seed(self.SEED__PRED_USED_BY))

        pred_contains = Schema__Ontology__Predicate(
            predicate_id        = contains_id                                       ,
            predicate_id_source = self._source_from_seed(self.SEED__PRED_CONTAINS)  ,
            predicate_ref       = Predicate_Ref('contains')                         ,
            inverse_id          = contained_by_id
        )

        pred_contained_by = Schema__Ontology__Predicate(
            predicate_id        = contained_by_id                                      ,
            predicate_id_source = self._source_from_seed(self.SEED__PRED_CONTAINED_BY) ,
            predicate_ref       = Predicate_Ref('contained_by')                        ,
            inverse_id          = contains_id
        )

        pred_calls = Schema__Ontology__Predicate(
            predicate_id        = calls_id                                          ,
            predicate_id_source = self._source_from_seed(self.SEED__PRED_CALLS)     ,
            predicate_ref       = Predicate_Ref('calls')                            ,
            inverse_id          = called_by_id
        )

        pred_called_by = Schema__Ontology__Predicate(
            predicate_id        = called_by_id                                      ,
            predicate_id_source = self._source_from_seed(self.SEED__PRED_CALLED_BY) ,
            predicate_ref       = Predicate_Ref('called_by')                        ,
            inverse_id          = calls_id
        )

        pred_uses = Schema__Ontology__Predicate(
            predicate_id        = uses_id                                           ,
            predicate_id_source = self._source_from_seed(self.SEED__PRED_USES)      ,
            predicate_ref       = Predicate_Ref('uses')                             ,
            inverse_id          = used_by_id
        )

        pred_used_by = Schema__Ontology__Predicate(
            predicate_id        = used_by_id                                        ,
            predicate_id_source = self._source_from_seed(self.SEED__PRED_USED_BY)   ,
            predicate_ref       = Predicate_Ref('used_by')                          ,
            inverse_id          = uses_id
        )

        result = Dict__Predicates__By_Id()
        result[pred_contains.predicate_id]     = pred_contains
        result[pred_contained_by.predicate_id] = pred_contained_by
        result[pred_calls.predicate_id]        = pred_calls
        result[pred_called_by.predicate_id]    = pred_called_by
        result[pred_uses.predicate_id]         = pred_uses
        result[pred_used_by.predicate_id]      = pred_used_by
        return result

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Rules Factory
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_edge_rules(self) -> List__Edge_Rules:                                 # Create edge rules
        nt_class_id    = Node_Type_Id(self._id_from_seed(self.SEED__NT_CLASS))
        nt_method_id   = Node_Type_Id(self._id_from_seed(self.SEED__NT_METHOD))
        nt_function_id = Node_Type_Id(self._id_from_seed(self.SEED__NT_FUNCTION))
        nt_module_id   = Node_Type_Id(self._id_from_seed(self.SEED__NT_MODULE))
        nt_variable_id = Node_Type_Id(self._id_from_seed(self.SEED__NT_VARIABLE))

        contains_id = Predicate_Id(self._id_from_seed(self.SEED__PRED_CONTAINS))
        calls_id    = Predicate_Id(self._id_from_seed(self.SEED__PRED_CALLS))
        uses_id     = Predicate_Id(self._id_from_seed(self.SEED__PRED_USES))

        rules = List__Edge_Rules()

        # Module contains class/function
        rules.append(Schema__Ontology__Edge_Rule(source_type_id = nt_module_id  ,
                                                 predicate_id   = contains_id   ,
                                                 target_type_id = nt_class_id   ))
        rules.append(Schema__Ontology__Edge_Rule(source_type_id = nt_module_id  ,
                                                 predicate_id   = contains_id   ,
                                                 target_type_id = nt_function_id))

        # Class contains method
        rules.append(Schema__Ontology__Edge_Rule(source_type_id = nt_class_id   ,
                                                 predicate_id   = contains_id   ,
                                                 target_type_id = nt_method_id  ))

        # Method/function calls method/function
        rules.append(Schema__Ontology__Edge_Rule(source_type_id = nt_method_id  ,
                                                 predicate_id   = calls_id      ,
                                                 target_type_id = nt_method_id  ))
        rules.append(Schema__Ontology__Edge_Rule(source_type_id = nt_method_id  ,
                                                 predicate_id   = calls_id      ,
                                                 target_type_id = nt_function_id))
        rules.append(Schema__Ontology__Edge_Rule(source_type_id = nt_function_id,
                                                 predicate_id   = calls_id      ,
                                                 target_type_id = nt_function_id))

        # Method/function uses variable
        rules.append(Schema__Ontology__Edge_Rule(source_type_id = nt_method_id  ,
                                                 predicate_id   = uses_id       ,
                                                 target_type_id = nt_variable_id))
        rules.append(Schema__Ontology__Edge_Rule(source_type_id = nt_function_id,
                                                 predicate_id   = uses_id       ,
                                                 target_type_id = nt_variable_id))

        return rules

    # ═══════════════════════════════════════════════════════════════════════════
    # Full Ontology Factory
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_ontology(self) -> Schema__Ontology:                                   # Create complete ontology
        taxonomy        = self.create_taxonomy()
        property_types  = self.create_property_types()
        property_names  = self.create_property_names(property_types)
        node_types      = self.create_node_types()
        predicates      = self.create_predicates()
        edge_rules      = self.create_edge_rules()

        return Schema__Ontology(
            ontology_id        = Ontology_Id(self._id_from_seed(self.SEED__ONTOLOGY)),
            ontology_id_source = self._source_from_seed(self.SEED__ONTOLOGY)        ,
            ontology_ref       = Ontology_Ref('code_analysis')                      ,
            taxonomy_id        = taxonomy.taxonomy_id                               ,
            node_types         = node_types                                         ,
            predicates         = predicates                                         ,
            property_names     = property_names                                     ,
            property_types     = property_types                                     ,
            edge_rules         = edge_rules
        )

    @type_safe
    def create_ontology_registry(self) -> Ontology__Registry:                        # Create registry with test ontology
        registry = Ontology__Registry()
        ontology = self.create_ontology()
        registry.register(ontology)
        return registry

    # ═══════════════════════════════════════════════════════════════════════════
    # Rule Set Factory
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_rule_set(self) -> Schema__Rule_Set:                                   # Create rule set with property rules
        nt_method_id      = Node_Type_Id(self._id_from_seed(self.SEED__NT_METHOD))
        nt_function_id    = Node_Type_Id(self._id_from_seed(self.SEED__NT_FUNCTION))
        calls_id          = Predicate_Id(self._id_from_seed(self.SEED__PRED_CALLS))
        pn_line_number_id = Property_Name_Id(self._id_from_seed(self.SEED__PN_LINE_NUMBER))
        pn_call_count_id  = Property_Name_Id(self._id_from_seed(self.SEED__PN_CALL_COUNT))

        # Methods and functions require line_number
        required_node_properties = List__Rules__Required_Node_Property()
        required_node_properties.append(Schema__Rule__Required_Node_Property(
            node_type_id     = nt_method_id     ,
            property_name_id = pn_line_number_id
        ))
        required_node_properties.append(Schema__Rule__Required_Node_Property(
            node_type_id     = nt_function_id   ,
            property_name_id = pn_line_number_id
        ))

        # Calls edges require call_count
        required_edge_properties = List__Rules__Required_Edge_Property()
        required_edge_properties.append(Schema__Rule__Required_Edge_Property(
            predicate_id     = calls_id        ,
            property_name_id = pn_call_count_id
        ))

        return Schema__Rule_Set(
            rule_set_id              = Rule_Set_Id(Obj_Id())                                   ,
            rule_set_ref             = Rule_Set_Ref('code_analysis_rules')                     ,
            ontology_id              = Ontology_Id(self._id_from_seed(self.SEED__ONTOLOGY))    ,
            version                  = Safe_Str__Version('1.0.0')                              ,
            transitivity_rules       = List__Rules__Transitivity()                             ,
            cardinality_rules        = List__Rules__Cardinality()                              ,
            required_node_properties = required_node_properties                                ,
            required_edge_properties = required_edge_properties
        )

    @type_safe
    def create_rule_set__empty(self) -> Schema__Rule_Set:                             # Create empty rule set
        return Schema__Rule_Set(
            rule_set_id              = Rule_Set_Id(Obj_Id())                                   ,
            rule_set_ref             = Rule_Set_Ref('empty_rules')                             ,
            ontology_id              = Ontology_Id(self._id_from_seed(self.SEED__ONTOLOGY))    ,
            version                  = Safe_Str__Version('1.0.0')                              ,
            transitivity_rules       = List__Rules__Transitivity()                             ,
            cardinality_rules        = List__Rules__Cardinality()                              ,
            required_node_properties = List__Rules__Required_Node_Property()                   ,
            required_edge_properties = List__Rules__Required_Edge_Property()
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # Graph Factory (with properties)
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_graph__empty(self, seed: Safe_Str__Id__Seed = None) -> Schema__Semantic_Graph:

        if seed is None:
            seed = Safe_Str__Id__Seed('test-graph-empty')

        return Schema__Semantic_Graph(graph_id        = Graph_Id(Obj_Id.from_seed(seed)),
                                      graph_id_source = self._source_from_seed(seed)   ,
                                      ontology_id     = Ontology_Id(self._id_from_seed(self.SEED__ONTOLOGY)),
                                      nodes           = Dict__Nodes__By_Id()           ,
                                      edges           = List__Semantic_Graph__Edges()  )
    @type_safe
    def create_graph_with_properties(self) -> 'Semantic_Graph__Builder':             # Create graph with property data
        ontology = self.create_ontology()

        # Get IDs
        nt_module_id   = Node_Type_Id(self._id_from_seed(self.SEED__NT_MODULE))
        nt_class_id    = Node_Type_Id(self._id_from_seed(self.SEED__NT_CLASS))
        nt_method_id   = Node_Type_Id(self._id_from_seed(self.SEED__NT_METHOD))
        nt_function_id = Node_Type_Id(self._id_from_seed(self.SEED__NT_FUNCTION))

        contains_id = Predicate_Id(self._id_from_seed(self.SEED__PRED_CONTAINS))
        calls_id    = Predicate_Id(self._id_from_seed(self.SEED__PRED_CALLS))

        pn_line_number_id = Property_Name_Id(self._id_from_seed(self.SEED__PN_LINE_NUMBER))
        pn_is_async_id    = Property_Name_Id(self._id_from_seed(self.SEED__PN_IS_ASYNC))
        pn_docstring_id   = Property_Name_Id(self._id_from_seed(self.SEED__PN_DOCSTRING))
        pn_call_count_id  = Property_Name_Id(self._id_from_seed(self.SEED__PN_CALL_COUNT))

        # Build graph
        builder = Semantic_Graph__Builder()
        builder.with_ontology_id(ontology.ontology_id)
        builder.with_deterministic_graph_id(self.SEED__GRAPH)

        # Create node properties
        module_props = Dict__Node_Properties()
        module_props[pn_docstring_id] = Safe_Str__Text('Main module')

        class_props = Dict__Node_Properties()
        class_props[pn_line_number_id] = Safe_Str__Text('10')
        class_props[pn_docstring_id]   = Safe_Str__Text('Foo class')

        method_props = Dict__Node_Properties()
        method_props[pn_line_number_id] = Safe_Str__Text('15')
        method_props[pn_is_async_id]    = Safe_Str__Text('false')

        func_props = Dict__Node_Properties()
        func_props[pn_line_number_id] = Safe_Str__Text('50')

        # Add nodes with properties
        builder.add_node_with_seed(node_type_id = nt_module_id                      ,
                                   name         = Safe_Str__Id('main_module')       ,
                                   seed         = self.SEED__NODE_MODULE_MAIN       ,
                                   properties   = module_props                      )

        builder.add_node_with_seed(node_type_id = nt_class_id                       ,
                                   name         = Safe_Str__Id('Foo')               ,
                                   seed         = self.SEED__NODE_CLASS_FOO         ,
                                   properties   = class_props                       )

        builder.add_node_with_seed(node_type_id = nt_method_id                      ,
                                   name         = Safe_Str__Id('bar')               ,
                                   seed         = self.SEED__NODE_METHOD_BAR        ,
                                   properties   = method_props                      )

        builder.add_node_with_seed(node_type_id = nt_function_id                    ,
                                   name         = Safe_Str__Id('helper')            ,
                                   seed         = self.SEED__NODE_FUNC_HELPER       ,
                                   properties   = func_props                        )

        # Get node IDs for edges
        node_module_id = Node_Id(self._id_from_seed(self.SEED__NODE_MODULE_MAIN))
        node_class_id  = Node_Id(self._id_from_seed(self.SEED__NODE_CLASS_FOO))
        node_method_id = Node_Id(self._id_from_seed(self.SEED__NODE_METHOD_BAR))
        node_func_id   = Node_Id(self._id_from_seed(self.SEED__NODE_FUNC_HELPER))

        # Create edge properties
        calls_props = Dict__Edge_Properties()
        calls_props[pn_call_count_id] = Safe_Str__Text('3')

        # Add edges
        builder.add_edge(from_node_id = node_module_id ,
                         predicate_id = contains_id    ,
                         to_node_id   = node_class_id  )

        builder.add_edge(from_node_id = node_module_id ,
                         predicate_id = contains_id    ,
                         to_node_id   = node_func_id   )

        builder.add_edge(from_node_id = node_class_id  ,
                         predicate_id = contains_id    ,
                         to_node_id   = node_method_id )

        builder.add_edge(from_node_id = node_method_id ,
                         predicate_id = calls_id       ,
                         to_node_id   = node_func_id   ,
                         properties   = calls_props    )

        return builder

    # ═══════════════════════════════════════════════════════════════════════════
    # Create Nodes and Edges
    # ═══════════════════════════════════════════════════════════════════════════
    @type_safe
    def create_node(self                                    ,
                    node_type_id : Node_Type_Id             ,
                    name         : Safe_Str__Id             ,
                    seed         : Safe_Str__Id__Seed = None,
                    properties   : Dict__Node_Properties = None) -> Schema__Semantic_Graph__Node:

        if seed:
            node_id    = Node_Id(Obj_Id.from_seed(seed))
            id_source  = self._source_from_seed(seed)
        else:
            node_id    = Node_Id(Obj_Id())
            id_source  = None

        return Schema__Semantic_Graph__Node(node_id        = node_id     ,
                                            node_id_source = id_source   ,
                                            node_type_id   = node_type_id,
                                            name           = name        ,
                                            properties     = properties  )

    @type_safe
    def create_edge(self                                    ,
                    from_node_id : Node_Id                  ,
                    predicate_id : Predicate_Id             ,
                    to_node_id   : Node_Id                  ,
                    seed         : Safe_Str__Id__Seed = None,
                    properties   : Dict__Edge_Properties = None) -> Schema__Semantic_Graph__Edge:

        if seed:
            edge_id   = Edge_Id(Obj_Id.from_seed(seed))
            id_source = self._source_from_seed(seed)
        else:
            edge_id   = Edge_Id(Obj_Id())
            id_source = None

        return Schema__Semantic_Graph__Edge(edge_id        = edge_id     ,
                                            edge_id_source = id_source   ,
                                            from_node_id   = from_node_id,
                                            predicate_id   = predicate_id,
                                            to_node_id     = to_node_id  ,
                                            properties     = properties  )

    # ═══════════════════════════════════════════════════════════════════════════
    # Complete Test Fixture
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_complete_fixture(self) -> dict:                                       # Create all test data
        taxonomy_registry = self.create_taxonomy_registry()
        ontology_registry = self.create_ontology_registry()
        rule_set          = self.create_rule_set()
        graph_builder     = self.create_graph_with_properties()
        graph             = graph_builder.build()

        projector = Semantic_Graph__Projector(ontology_registry = ontology_registry,
                                              taxonomy_registry = taxonomy_registry)
        projection = projector.project(graph)

        return {
            'taxonomy_registry' : taxonomy_registry ,
            'ontology_registry' : ontology_registry ,
            'ontology'          : ontology_registry.get_by_ref(Ontology_Ref('code_analysis')),
            'taxonomy'          : taxonomy_registry.get_by_ref(Taxonomy_Ref('code_analysis')),
            'rule_set'          : rule_set          ,
            'graph'             : graph             ,
            'projection'        : projection        ,
            'projector'         : projector
        }

    # ═══════════════════════════════════════════════════════════════════════════
    # Accessor Methods for Individual IDs (for tests)
    # ═══════════════════════════════════════════════════════════════════════════

    def get_category_id__callable(self)  -> Category_Id:
        return Category_Id(self._id_from_seed(self.SEED__CAT_CALLABLE))

    def get_category_id__container(self) -> Category_Id:
        return Category_Id(self._id_from_seed(self.SEED__CAT_CONTAINER))

    def get_category_id__data(self) -> Category_Id:
        return Category_Id(self._id_from_seed(self.SEED__CAT_DATA))

    def get_category_id__root(self)  -> Category_Id:
        return Category_Id(self._id_from_seed(self.SEED__CAT_ROOT))

    def get_node_type_id__class(self)    -> Node_Type_Id:
        return Node_Type_Id(self._id_from_seed(self.SEED__NT_CLASS))

    def get_node_type_id__method(self)   -> Node_Type_Id:
        return Node_Type_Id(self._id_from_seed(self.SEED__NT_METHOD))

    def get_node_type_id__function(self) -> Node_Type_Id:
        return Node_Type_Id(self._id_from_seed(self.SEED__NT_FUNCTION))

    def get_predicate_id__contains(self) -> Predicate_Id:
        return Predicate_Id(self._id_from_seed(self.SEED__PRED_CONTAINS))

    def get_predicate_id__contained_by(self) -> Predicate_Id:
        return Predicate_Id(self._id_from_seed(self.SEED__PRED_CONTAINED_BY))

    def get_predicate_id__calls(self)    -> Predicate_Id:
        return Predicate_Id(self._id_from_seed(self.SEED__PRED_CALLS))

    def get_predicate_id__called_by(self)    -> Predicate_Id:
        return Predicate_Id(self._id_from_seed(self.SEED__PRED_CALLED_BY))

    def get_property_name_id__line_number(self) -> Property_Name_Id:
        return Property_Name_Id(self._id_from_seed(self.SEED__PN_LINE_NUMBER))

    def get_property_name_id__call_count(self)  -> Property_Name_Id:
        return Property_Name_Id(self._id_from_seed(self.SEED__PN_CALL_COUNT))

    def get_property_type_id__integer(self)     -> Property_Type_Id:
        return Property_Type_Id(self._id_from_seed(self.SEED__PT_INTEGER))

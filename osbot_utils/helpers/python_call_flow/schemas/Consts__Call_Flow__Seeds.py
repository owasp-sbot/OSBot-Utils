# ═══════════════════════════════════════════════════════════════════════════════
# Call Flow Seeds - Deterministic ID Seeds for Ontology and Taxonomy
# These seeds ensure consistent IDs across all instances
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
# Ontology and Taxonomy Root Seeds
# ═══════════════════════════════════════════════════════════════════════════════

SEED__ONTOLOGY                      = 'call_flow:ontology'
SEED__TAXONOMY                      = 'call_flow:taxonomy'


# ═══════════════════════════════════════════════════════════════════════════════
# Node Type Seeds
# ═══════════════════════════════════════════════════════════════════════════════

SEED__NODE_TYPE__CLASS              = 'call_flow:node_type:class'
SEED__NODE_TYPE__METHOD             = 'call_flow:node_type:method'
SEED__NODE_TYPE__FUNCTION           = 'call_flow:node_type:function'
SEED__NODE_TYPE__MODULE             = 'call_flow:node_type:module'
SEED__NODE_TYPE__EXTERNAL           = 'call_flow:node_type:external'


# ═══════════════════════════════════════════════════════════════════════════════
# Predicate Seeds (Edge Types)
# ═══════════════════════════════════════════════════════════════════════════════

SEED__PREDICATE__CONTAINS           = 'call_flow:predicate:contains'
SEED__PREDICATE__CONTAINED_BY       = 'call_flow:predicate:contained_by'
SEED__PREDICATE__CALLS              = 'call_flow:predicate:calls'
SEED__PREDICATE__CALLED_BY          = 'call_flow:predicate:called_by'
SEED__PREDICATE__CALLS_SELF         = 'call_flow:predicate:calls_self'
SEED__PREDICATE__CALLS_CHAIN        = 'call_flow:predicate:calls_chain'


# ═══════════════════════════════════════════════════════════════════════════════
# Property Name Seeds
# ═══════════════════════════════════════════════════════════════════════════════

SEED__PROP__QUALIFIED_NAME          = 'call_flow:property:qualified_name'
SEED__PROP__MODULE_NAME             = 'call_flow:property:module_name'
SEED__PROP__FILE_PATH               = 'call_flow:property:file_path'
SEED__PROP__LINE_NUMBER             = 'call_flow:property:line_number'
SEED__PROP__CALL_DEPTH              = 'call_flow:property:call_depth'
SEED__PROP__SOURCE_CODE             = 'call_flow:property:source_code'
SEED__PROP__IS_ENTRY                = 'call_flow:property:is_entry'
SEED__PROP__IS_EXTERNAL             = 'call_flow:property:is_external'
SEED__PROP__IS_RECURSIVE            = 'call_flow:property:is_recursive'
SEED__PROP__IS_CONDITIONAL          = 'call_flow:property:is_conditional'
SEED__PROP__CALL_LINE_NUMBER        = 'call_flow:property:call_line_number'


# ═══════════════════════════════════════════════════════════════════════════════
# Property Type Seeds
# ═══════════════════════════════════════════════════════════════════════════════

SEED__PROP_TYPE__STRING             = 'call_flow:property_type:string'
SEED__PROP_TYPE__TEXT               = 'call_flow:property_type:text'
SEED__PROP_TYPE__INTEGER            = 'call_flow:property_type:integer'
SEED__PROP_TYPE__BOOLEAN            = 'call_flow:property_type:boolean'


# ═══════════════════════════════════════════════════════════════════════════════
# Taxonomy Category Seeds
# ═══════════════════════════════════════════════════════════════════════════════

SEED__CATEGORY__CODE_ELEMENT        = 'call_flow:category:code_element'
SEED__CATEGORY__CONTAINER           = 'call_flow:category:container'
SEED__CATEGORY__CALLABLE            = 'call_flow:category:callable'
SEED__CATEGORY__REFERENCE           = 'call_flow:category:reference'

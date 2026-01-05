# ═══════════════════════════════════════════════════════════════════════════════
# Call Flow Data Generator - Creates ontology and taxonomy JSON files
# Run this script to regenerate the JSON files with deterministic IDs
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id           import Obj_Id
from osbot_utils.utils.Json                                                import json_save_file_pretty
from osbot_utils.utils.Files                                               import path_combine, parent_folder

from osbot_utils.helpers.python_call_flow.schemas.Consts__Call_Flow__Seeds import (SEED__ONTOLOGY                                                    ,
                                                                                   SEED__TAXONOMY                                                    ,
                                                                                   SEED__NODE_TYPE__CLASS, SEED__NODE_TYPE__METHOD                   ,
                                                                                   SEED__NODE_TYPE__FUNCTION, SEED__NODE_TYPE__MODULE                ,
                                                                                   SEED__NODE_TYPE__EXTERNAL                                         ,
                                                                                   SEED__PREDICATE__CONTAINS, SEED__PREDICATE__CONTAINED_BY          ,
                                                                                   SEED__PREDICATE__CALLS, SEED__PREDICATE__CALLED_BY                ,
                                                                                   SEED__PREDICATE__CALLS_SELF, SEED__PREDICATE__CALLS_CHAIN         ,
                                                                                   SEED__PROP__QUALIFIED_NAME, SEED__PROP__MODULE_NAME               ,
                                                                                   SEED__PROP__FILE_PATH, SEED__PROP__LINE_NUMBER                    ,
                                                                                   SEED__PROP__CALL_DEPTH, SEED__PROP__SOURCE_CODE                   ,
                                                                                   SEED__PROP__IS_ENTRY, SEED__PROP__IS_EXTERNAL                     ,
                                                                                   SEED__PROP__IS_RECURSIVE, SEED__PROP__IS_CONDITIONAL              ,
                                                                                   SEED__PROP__CALL_LINE_NUMBER                                      ,
                                                                                   SEED__PROP_TYPE__STRING, SEED__PROP_TYPE__TEXT                    ,
                                                                                   SEED__PROP_TYPE__INTEGER, SEED__PROP_TYPE__BOOLEAN                ,
                                                                                   SEED__CATEGORY__CODE_ELEMENT, SEED__CATEGORY__CONTAINER           ,
                                                                                   SEED__CATEGORY__CALLABLE, SEED__CATEGORY__REFERENCE               )


def id_from_seed(seed: str) -> str:                                              # Generate deterministic ID from seed
    return str(Obj_Id.from_seed(seed))


def generate_ontology() -> dict:                                                 # Generate complete ontology structure
    ontology_id         = id_from_seed(SEED__ONTOLOGY)
    taxonomy_id         = id_from_seed(SEED__TAXONOMY)

    class_type_id       = id_from_seed(SEED__NODE_TYPE__CLASS)                   # Node type IDs
    method_type_id      = id_from_seed(SEED__NODE_TYPE__METHOD)
    function_type_id    = id_from_seed(SEED__NODE_TYPE__FUNCTION)
    module_type_id      = id_from_seed(SEED__NODE_TYPE__MODULE)
    external_type_id    = id_from_seed(SEED__NODE_TYPE__EXTERNAL)

    contains_id         = id_from_seed(SEED__PREDICATE__CONTAINS)                # Predicate IDs
    contained_by_id     = id_from_seed(SEED__PREDICATE__CONTAINED_BY)
    calls_id            = id_from_seed(SEED__PREDICATE__CALLS)
    called_by_id        = id_from_seed(SEED__PREDICATE__CALLED_BY)
    calls_self_id       = id_from_seed(SEED__PREDICATE__CALLS_SELF)
    calls_chain_id      = id_from_seed(SEED__PREDICATE__CALLS_CHAIN)

    qualified_name_id   = id_from_seed(SEED__PROP__QUALIFIED_NAME)               # Property name IDs
    module_name_id      = id_from_seed(SEED__PROP__MODULE_NAME)
    file_path_id        = id_from_seed(SEED__PROP__FILE_PATH)
    line_number_id      = id_from_seed(SEED__PROP__LINE_NUMBER)
    call_depth_id       = id_from_seed(SEED__PROP__CALL_DEPTH)
    source_code_id      = id_from_seed(SEED__PROP__SOURCE_CODE)
    is_entry_id         = id_from_seed(SEED__PROP__IS_ENTRY)
    is_external_id      = id_from_seed(SEED__PROP__IS_EXTERNAL)
    is_recursive_id     = id_from_seed(SEED__PROP__IS_RECURSIVE)
    is_conditional_id   = id_from_seed(SEED__PROP__IS_CONDITIONAL)
    call_line_number_id = id_from_seed(SEED__PROP__CALL_LINE_NUMBER)

    string_type_id      = id_from_seed(SEED__PROP_TYPE__STRING)                  # Property type IDs
    text_type_id        = id_from_seed(SEED__PROP_TYPE__TEXT)
    integer_type_id     = id_from_seed(SEED__PROP_TYPE__INTEGER)
    boolean_type_id     = id_from_seed(SEED__PROP_TYPE__BOOLEAN)

    container_cat_id    = id_from_seed(SEED__CATEGORY__CONTAINER)                # Category IDs
    callable_cat_id     = id_from_seed(SEED__CATEGORY__CALLABLE)
    reference_cat_id    = id_from_seed(SEED__CATEGORY__REFERENCE)

    return {
        "ontology_id"  : ontology_id                                             ,
        "ontology_ref" : "call_flow"                                             ,
        "taxonomy_id"  : taxonomy_id                                             ,
        "version"      : "1.0.0"                                                 ,

        "node_types": {
            class_type_id: {
                "node_type_id"  : class_type_id                                  ,
                "node_type_ref" : "class"                                        ,
                "category_id"   : container_cat_id                               ,
            },
            method_type_id: {
                "node_type_id"  : method_type_id                                 ,
                "node_type_ref" : "method"                                       ,
                "category_id"   : callable_cat_id                                ,
            },
            function_type_id: {
                "node_type_id"  : function_type_id                               ,
                "node_type_ref" : "function"                                     ,
                "category_id"   : callable_cat_id                                ,
            },
            module_type_id: {
                "node_type_id"  : module_type_id                                 ,
                "node_type_ref" : "module"                                       ,
                "category_id"   : container_cat_id                               ,
            },
            external_type_id: {
                "node_type_id"  : external_type_id                               ,
                "node_type_ref" : "external"                                     ,
                "category_id"   : reference_cat_id                               ,
            },
        },

        "predicates": {
            contains_id: {
                "predicate_id"  : contains_id                                    ,
                "predicate_ref" : "contains"                                     ,
                "inverse_id"    : contained_by_id                                ,
            },
            contained_by_id: {
                "predicate_id"  : contained_by_id                                ,
                "predicate_ref" : "contained_by"                                 ,
                "inverse_id"    : contains_id                                    ,
            },
            calls_id: {
                "predicate_id"  : calls_id                                       ,
                "predicate_ref" : "calls"                                        ,
                "inverse_id"    : called_by_id                                   ,
            },
            called_by_id: {
                "predicate_id"  : called_by_id                                   ,
                "predicate_ref" : "called_by"                                    ,
                "inverse_id"    : calls_id                                       ,
            },
            calls_self_id: {
                "predicate_id"  : calls_self_id                                  ,
                "predicate_ref" : "calls_self"                                   ,
                "inverse_id"    : None                                           ,
            },
            calls_chain_id: {
                "predicate_id"  : calls_chain_id                                 ,
                "predicate_ref" : "calls_chain"                                  ,
                "inverse_id"    : None                                           ,
            },
        },

        "property_names": {
            qualified_name_id: {
                "property_name_id"  : qualified_name_id                          ,
                "property_name_ref" : "qualified_name"                           ,
                "property_type_id"  : string_type_id                             ,
            },
            module_name_id: {
                "property_name_id"  : module_name_id                             ,
                "property_name_ref" : "module_name"                              ,
                "property_type_id"  : string_type_id                             ,
            },
            file_path_id: {
                "property_name_id"  : file_path_id                               ,
                "property_name_ref" : "file_path"                                ,
                "property_type_id"  : string_type_id                             ,
            },
            line_number_id: {
                "property_name_id"  : line_number_id                             ,
                "property_name_ref" : "line_number"                              ,
                "property_type_id"  : integer_type_id                            ,
            },
            call_depth_id: {
                "property_name_id"  : call_depth_id                              ,
                "property_name_ref" : "call_depth"                               ,
                "property_type_id"  : integer_type_id                            ,
            },
            source_code_id: {
                "property_name_id"  : source_code_id                             ,
                "property_name_ref" : "source_code"                              ,
                "property_type_id"  : text_type_id                               ,
            },
            is_entry_id: {
                "property_name_id"  : is_entry_id                                ,
                "property_name_ref" : "is_entry"                                 ,
                "property_type_id"  : boolean_type_id                            ,
            },
            is_external_id: {
                "property_name_id"  : is_external_id                             ,
                "property_name_ref" : "is_external"                              ,
                "property_type_id"  : boolean_type_id                            ,
            },
            is_recursive_id: {
                "property_name_id"  : is_recursive_id                            ,
                "property_name_ref" : "is_recursive"                             ,
                "property_type_id"  : boolean_type_id                            ,
            },
            is_conditional_id: {
                "property_name_id"  : is_conditional_id                          ,
                "property_name_ref" : "is_conditional"                           ,
                "property_type_id"  : boolean_type_id                            ,
            },
            call_line_number_id: {
                "property_name_id"  : call_line_number_id                        ,
                "property_name_ref" : "call_line_number"                         ,
                "property_type_id"  : integer_type_id                            ,
            },
        },

        "property_types": {
            string_type_id: {
                "property_type_id"  : string_type_id                             ,
                "property_type_ref" : "string"                                   ,
            },
            text_type_id: {
                "property_type_id"  : text_type_id                               ,
                "property_type_ref" : "text"                                     ,
            },
            integer_type_id: {
                "property_type_id"  : integer_type_id                            ,
                "property_type_ref" : "integer"                                  ,
            },
            boolean_type_id: {
                "property_type_id"  : boolean_type_id                            ,
                "property_type_ref" : "boolean"                                  ,
            },
        },

        "edge_rules": [                                                          # Containment rules
            {"source_type_id": module_type_id  , "predicate_id": contains_id, "target_type_id": class_type_id   },
            {"source_type_id": module_type_id  , "predicate_id": contains_id, "target_type_id": function_type_id},
            {"source_type_id": class_type_id   , "predicate_id": contains_id, "target_type_id": method_type_id  },
                                                                                 # Call rules (any callable can call any callable or external)
            {"source_type_id": method_type_id  , "predicate_id": calls_id   , "target_type_id": method_type_id  },
            {"source_type_id": method_type_id  , "predicate_id": calls_id   , "target_type_id": function_type_id},
            {"source_type_id": method_type_id  , "predicate_id": calls_id   , "target_type_id": external_type_id},
            {"source_type_id": function_type_id, "predicate_id": calls_id   , "target_type_id": method_type_id  },
            {"source_type_id": function_type_id, "predicate_id": calls_id   , "target_type_id": function_type_id},
            {"source_type_id": function_type_id, "predicate_id": calls_id   , "target_type_id": external_type_id},
                                                                                 # Self calls (method calling another method in same class)
            {"source_type_id": method_type_id  , "predicate_id": calls_self_id , "target_type_id": method_type_id },
                                                                                 # Chain calls (calling through attribute chain)
            {"source_type_id": method_type_id  , "predicate_id": calls_chain_id, "target_type_id": method_type_id  },
            {"source_type_id": method_type_id  , "predicate_id": calls_chain_id, "target_type_id": external_type_id},
            {"source_type_id": function_type_id, "predicate_id": calls_chain_id, "target_type_id": method_type_id  },
            {"source_type_id": function_type_id, "predicate_id": calls_chain_id, "target_type_id": external_type_id},
        ],
    }


def generate_taxonomy() -> dict:                                                 # Generate complete taxonomy structure
    taxonomy_id       = id_from_seed(SEED__TAXONOMY)
    code_element_id   = id_from_seed(SEED__CATEGORY__CODE_ELEMENT)
    container_id      = id_from_seed(SEED__CATEGORY__CONTAINER)
    callable_id       = id_from_seed(SEED__CATEGORY__CALLABLE)
    reference_id      = id_from_seed(SEED__CATEGORY__REFERENCE)

    return {
        "taxonomy_id"  : taxonomy_id                                             ,
        "taxonomy_ref" : "call_flow_taxonomy"                                    ,
        "version"      : "1.0.0"                                                 ,
        "root_id"      : code_element_id                                         ,

        "categories": {
            code_element_id: {
                "category_id"  : code_element_id                                 ,
                "category_ref" : "code_element"                                  ,
                "parent_id"    : None                                            ,
                "child_ids"    : [container_id, callable_id, reference_id]       ,
            },
            container_id: {
                "category_id"  : container_id                                    ,
                "category_ref" : "container"                                     ,
                "parent_id"    : code_element_id                                 ,
                "child_ids"    : []                                              ,
            },
            callable_id: {
                "category_id"  : callable_id                                     ,
                "category_ref" : "callable"                                      ,
                "parent_id"    : code_element_id                                 ,
                "child_ids"    : []                                              ,
            },
            reference_id: {
                "category_id"  : reference_id                                    ,
                "category_ref" : "reference"                                     ,
                "parent_id"    : code_element_id                                 ,
                "child_ids"    : []                                              ,
            },
        },
    }


def generate_data_files(output_dir: str = None):                                 # Generate and save both JSON files
    if output_dir is None:
        output_dir = path_combine(parent_folder(__file__), 'data')

    ontology_path = path_combine(output_dir, 'ontology__call_flow.json')
    taxonomy_path = path_combine(output_dir, 'taxonomy__call_flow.json')

    ontology_data = generate_ontology()
    taxonomy_data = generate_taxonomy()

    json_save_file_pretty(ontology_data, ontology_path)
    json_save_file_pretty(taxonomy_data, taxonomy_path)

    #print(f"Generated: {ontology_path}")
    #print(f"Generated: {taxonomy_path}")

    return ontology_path, taxonomy_path

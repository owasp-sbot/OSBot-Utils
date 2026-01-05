# ═══════════════════════════════════════════════════════════════════════════════
# Call Flow Ontology - Load and Cache Call Flow Ontology and Taxonomy
# Provides lookup methods for node types, predicates, properties by ref
# ═══════════════════════════════════════════════════════════════════════════════

from pathlib                                                                    import Path
from typing                                                                     import Optional, Dict
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.utils.Json                                                     import json_load_file
from osbot_utils.utils.Files                                                    import path_combine, file_exists
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id        import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id        import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id         import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id         import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id         import Taxonomy_Id

FOLDER_NAME__CALL_FLOW__GRAPH_SPEC  = '../_graph_spec'
ONTOLOGY_FILE                       = 'ontology__call_flow.json'
TAXONOMY_FILE                       = 'taxonomy__call_flow.json'


class Call_Flow__Ontology(Type_Safe):                                            # Loads and caches the call flow ontology and taxonomy
    ontology_data       : dict                                                   # Raw ontology data from JSON
    taxonomy_data       : dict                                                   # Raw taxonomy data from JSON

    node_type_ref_to_id : Dict[str, Node_Type_Id ]                               # Cache: ref -> ID lookups
    predicate_ref_to_id : Dict[str, Predicate_Id ]
    prop_name_ref_to_id : Dict[str, str          ]                               # Property name ref -> ID (as string)
    prop_type_ref_to_id : Dict[str, str          ]                               # Property type ref -> ID (as string)
    category_ref_to_id  : Dict[str, Category_Id  ]

    _loaded             : bool = False                                           # Track if data has been loaded

    def setup(self) -> 'Call_Flow__Ontology':                                    # Load ontology and taxonomy from JSON files
        if self._loaded:
            return self

        target_folder = self.folder__call_flow__graph_spec()
        ontology_path = path_combine(target_folder, ONTOLOGY_FILE)
        taxonomy_path = path_combine(target_folder, TAXONOMY_FILE)

        if not file_exists(ontology_path):
            raise FileNotFoundError(f"Ontology file not found: {ontology_path}")
        if not file_exists(taxonomy_path):
            raise FileNotFoundError(f"Taxonomy file not found: {taxonomy_path}")

        self.ontology_data = json_load_file(ontology_path)
        self.taxonomy_data = json_load_file(taxonomy_path)

        self._build_lookup_caches()
        self._loaded = True

        return self

    def folder__call_flow__graph_spec(self):
        return path_combine(__file__, FOLDER_NAME__CALL_FLOW__GRAPH_SPEC)

    def _build_lookup_caches(self):                                              # Build ref → ID lookup caches
        self.node_type_ref_to_id = {}                                            # Node types: ref -> ID
        for node_type in self.ontology_data.get('node_types', {}).values():
            ref = node_type.get('node_type_ref')
            id_ = node_type.get('node_type_id')
            if ref and id_:
                self.node_type_ref_to_id[ref] = Node_Type_Id(id_)

        self.predicate_ref_to_id = {}                                            # Predicates: ref -> ID
        for predicate in self.ontology_data.get('predicates', {}).values():
            ref = predicate.get('predicate_ref')
            id_ = predicate.get('predicate_id')
            if ref and id_:
                self.predicate_ref_to_id[ref] = Predicate_Id(id_)

        self.prop_name_ref_to_id = {}                                            # Property names: ref -> ID (as string)
        for prop_name in self.ontology_data.get('property_names', {}).values():
            ref = prop_name.get('property_name_ref')
            id_ = prop_name.get('property_name_id')
            if ref and id_:
                self.prop_name_ref_to_id[ref] = id_

        self.prop_type_ref_to_id = {}                                            # Property types: ref -> ID (as string)
        for prop_type in self.ontology_data.get('property_types', {}).values():
            ref = prop_type.get('property_type_ref')
            id_ = prop_type.get('property_type_id')
            if ref and id_:
                self.prop_type_ref_to_id[ref] = id_

        self.category_ref_to_id = {}                                             # Categories: ref -> ID
        for category in self.taxonomy_data.get('categories', {}).values():
            ref = category.get('category_ref')
            id_ = category.get('category_id')
            if ref and id_:
                self.category_ref_to_id[ref] = Category_Id(id_)

    # ═══════════════════════════════════════════════════════════════════════════
    # ID Lookups by Ref
    # ═══════════════════════════════════════════════════════════════════════════

    def ontology_id(self) -> Ontology_Id:                                        # Get the ontology ID
        return Ontology_Id(self.ontology_data.get('ontology_id', ''))

    def taxonomy_id(self) -> Taxonomy_Id:                                        # Get the taxonomy ID
        return Taxonomy_Id(self.taxonomy_data.get('taxonomy_id', ''))

    def node_type_id(self, ref: str) -> Optional[Node_Type_Id]:                  # Get node type ID by ref (e.g., 'class', 'method')
        return self.node_type_ref_to_id.get(ref)

    def predicate_id(self, ref: str) -> Optional[Predicate_Id]:                  # Get predicate ID by ref (e.g., 'calls', 'contains')
        return self.predicate_ref_to_id.get(ref)

    def property_name_id(self, ref: str) -> Optional[str]:                       # Get property name ID by ref (e.g., 'line_number')
        return self.prop_name_ref_to_id.get(ref)

    def property_type_id(self, ref: str) -> Optional[str]:                       # Get property type ID by ref (e.g., 'string', 'integer')
        return self.prop_type_ref_to_id.get(ref)

    def category_id(self, ref: str) -> Optional[Category_Id]:                    # Get category ID by ref (e.g., 'callable', 'container')
        return self.category_ref_to_id.get(ref)

    # ═══════════════════════════════════════════════════════════════════════════
    # Convenience Methods - Node Types
    # ═══════════════════════════════════════════════════════════════════════════

    def node_type_id__class(self) -> Node_Type_Id:                               # Get the 'class' node type ID
        return self.node_type_id('class')

    def node_type_id__method(self) -> Node_Type_Id:                              # Get the 'method' node type ID
        return self.node_type_id('method')

    def node_type_id__function(self) -> Node_Type_Id:                            # Get the 'function' node type ID
        return self.node_type_id('function')

    def node_type_id__module(self) -> Node_Type_Id:                              # Get the 'module' node type ID
        return self.node_type_id('module')

    def node_type_id__external(self) -> Node_Type_Id:                            # Get the 'external' node type ID
        return self.node_type_id('external')

    # ═══════════════════════════════════════════════════════════════════════════
    # Convenience Methods - Predicates
    # ═══════════════════════════════════════════════════════════════════════════

    def predicate_id__contains(self) -> Predicate_Id:                            # Get the 'contains' predicate ID
        return self.predicate_id('contains')

    def predicate_id__calls(self) -> Predicate_Id:                               # Get the 'calls' predicate ID
        return self.predicate_id('calls')

    def predicate_id__calls_self(self) -> Predicate_Id:                          # Get the 'calls_self' predicate ID
        return self.predicate_id('calls_self')

    def predicate_id__calls_chain(self) -> Predicate_Id:                         # Get the 'calls_chain' predicate ID
        return self.predicate_id('calls_chain')

    # ═══════════════════════════════════════════════════════════════════════════
    # Convenience Methods - Property Names
    # ═══════════════════════════════════════════════════════════════════════════

    def property_name_id__qualified_name(self) -> str:                           # Get the 'qualified_name' property ID
        return self.property_name_id('qualified_name')

    def property_name_id__module_name(self) -> str:                              # Get the 'module_name' property ID
        return self.property_name_id('module_name')

    def property_name_id__file_path(self) -> str:                                # Get the 'file_path' property ID
        return self.property_name_id('file_path')

    def property_name_id__line_number(self) -> str:                              # Get the 'line_number' property ID
        return self.property_name_id('line_number')

    def property_name_id__call_depth(self) -> str:                               # Get the 'call_depth' property ID
        return self.property_name_id('call_depth')

    def property_name_id__source_code(self) -> str:                              # Get the 'source_code' property ID
        return self.property_name_id('source_code')

    def property_name_id__is_entry(self) -> str:                                 # Get the 'is_entry' property ID
        return self.property_name_id('is_entry')

    def property_name_id__is_external(self) -> str:                              # Get the 'is_external' property ID
        return self.property_name_id('is_external')

    def property_name_id__is_recursive(self) -> str:                             # Get the 'is_recursive' property ID
        return self.property_name_id('is_recursive')

    def property_name_id__is_conditional(self) -> str:                           # Get the 'is_conditional' property ID
        return self.property_name_id('is_conditional')

    def property_name_id__call_line_number(self) -> str:                         # Get the 'call_line_number' property ID
        return self.property_name_id('call_line_number')

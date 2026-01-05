# ═══════════════════════════════════════════════════════════════════════════════
# test_Call_Flow__Data__Generator - Tests for ontology/taxonomy JSON generation
# ═══════════════════════════════════════════════════════════════════════════════

import tempfile
from pathlib                                                                         import Path
from unittest                                                                        import TestCase
from osbot_utils.helpers.python_call_flow.Call_Flow__Data__Generator                 import (id_from_seed      ,
                                                                                             generate_ontology ,
                                                                                             generate_taxonomy ,
                                                                                             generate_data_files)
from osbot_utils.helpers.python_call_flow.schemas.Consts__Call_Flow__Seeds          import SEED__ONTOLOGY, SEED__NODE_TYPE__CLASS, SEED__PREDICATE__CONTAINS


class test_Call_Flow__Data__Generator(TestCase):                                     # Test data generator functions

    def test__id_from_seed(self):                                                    # Test deterministic ID generation
        id_1 = id_from_seed('test_seed')
        id_2 = id_from_seed('test_seed')
        id_3 = id_from_seed('different_seed')

        assert type(id_1) is str
        assert len(id_1)  == 8                                                       # Obj_Id length
        assert id_1       == id_2                                                    # Same seed = same ID
        assert id_1       != id_3                                                    # Different seed = different ID

    def test__id_from_seed__known_seeds(self):                                       # Test with known seeds
        ontology_id = id_from_seed(SEED__ONTOLOGY)
        class_id    = id_from_seed(SEED__NODE_TYPE__CLASS)
        contains_id = id_from_seed(SEED__PREDICATE__CONTAINS)

        assert type(ontology_id) is str
        assert type(class_id)    is str
        assert type(contains_id) is str
        assert ontology_id != class_id != contains_id                                # All unique

    def test__generate_ontology(self):                                               # Test ontology generation
        ontology = generate_ontology()

        assert type(ontology) is dict
        assert 'ontology_id'  in ontology
        assert 'ontology_ref' in ontology
        assert 'taxonomy_id'  in ontology
        assert 'version'      in ontology
        assert 'node_types'   in ontology
        assert 'predicates'   in ontology
        assert 'property_names' in ontology
        assert 'property_types' in ontology
        assert 'edge_rules'   in ontology

    def test__generate_ontology__node_types(self):                                   # Test node types in ontology
        ontology   = generate_ontology()
        node_types = ontology['node_types']

        assert len(node_types) == 5                                                  # class, method, function, module, external

        # Verify all have required fields
        for node_type_id, node_type in node_types.items():
            assert 'node_type_id'  in node_type
            assert 'node_type_ref' in node_type
            assert 'category_id'   in node_type

        # Verify expected refs exist
        refs = [nt['node_type_ref'] for nt in node_types.values()]
        assert 'class'    in refs
        assert 'method'   in refs
        assert 'function' in refs
        assert 'module'   in refs
        assert 'external' in refs

    def test__generate_ontology__predicates(self):                                   # Test predicates in ontology
        ontology   = generate_ontology()
        predicates = ontology['predicates']

        assert len(predicates) >= 6                                                  # contains, contained_by, calls, called_by, calls_self, calls_chain

        # Verify all have required fields
        for pred_id, pred in predicates.items():
            assert 'predicate_id'  in pred
            assert 'predicate_ref' in pred
            assert 'inverse_id'    in pred

        # Verify expected refs exist
        refs = [p['predicate_ref'] for p in predicates.values()]
        assert 'contains'     in refs
        assert 'contained_by' in refs
        assert 'calls'        in refs
        assert 'called_by'    in refs
        assert 'calls_self'   in refs
        assert 'calls_chain'  in refs

    def test__generate_ontology__property_names(self):                               # Test property names in ontology
        ontology       = generate_ontology()
        property_names = ontology['property_names']

        # Verify expected properties exist
        refs = [p['property_name_ref'] for p in property_names.values()]
        assert 'qualified_name' in refs
        assert 'module_name'    in refs
        assert 'is_entry'       in refs
        assert 'line_number'    in refs

    def test__generate_ontology__edge_rules(self):                                   # Test edge rules in ontology
        ontology   = generate_ontology()
        edge_rules = ontology['edge_rules']

        assert type(edge_rules) is list
        assert len(edge_rules)  >= 10                                                # Multiple rules defined

        # Verify all have required fields
        for rule in edge_rules:
            assert 'source_type_id' in rule
            assert 'predicate_id'   in rule
            assert 'target_type_id' in rule

    def test__generate_ontology__deterministic(self):                                # Test ontology is deterministic
        ontology_1 = generate_ontology()
        ontology_2 = generate_ontology()

        assert ontology_1['ontology_id'] == ontology_2['ontology_id']
        assert ontology_1['taxonomy_id'] == ontology_2['taxonomy_id']

    def test__generate_taxonomy(self):                                               # Test taxonomy generation
        taxonomy = generate_taxonomy()

        assert type(taxonomy)  is dict
        assert 'taxonomy_id'   in taxonomy
        assert 'taxonomy_ref'  in taxonomy
        assert 'version'       in taxonomy
        assert 'root_id'       in taxonomy
        assert 'categories'    in taxonomy

    def test__generate_taxonomy__categories(self):                                   # Test categories in taxonomy
        taxonomy   = generate_taxonomy()
        categories = taxonomy['categories']

        assert len(categories) == 4                                                  # code_element, container, callable, reference

        # Verify all have required fields
        for cat_id, cat in categories.items():
            assert 'category_id'  in cat
            assert 'category_ref' in cat
            assert 'parent_id'    in cat
            assert 'child_ids'    in cat

        # Verify expected refs exist
        refs = [c['category_ref'] for c in categories.values()]
        assert 'code_element' in refs
        assert 'container'    in refs
        assert 'callable'     in refs
        assert 'reference'    in refs

    def test__generate_taxonomy__hierarchy(self):                                    # Test taxonomy hierarchy
        taxonomy   = generate_taxonomy()
        categories = taxonomy['categories']

        # Find root (code_element)
        root_id   = taxonomy['root_id']
        root      = categories[root_id]
        child_ids = root['child_ids']

        assert root['parent_id']  is None                                            # Root has no parent
        assert len(child_ids)     == 3                                               # 3 children

        # Verify children reference root as parent
        for child_id in child_ids:
            child = categories[child_id]
            assert child['parent_id'] == root_id

    def test__generate_taxonomy__deterministic(self):                                # Test taxonomy is deterministic
        taxonomy_1 = generate_taxonomy()
        taxonomy_2 = generate_taxonomy()

        assert taxonomy_1['taxonomy_id'] == taxonomy_2['taxonomy_id']
        assert taxonomy_1['root_id']     == taxonomy_2['root_id']

    def test__generate_data_files(self):                                             # Test file generation
        with tempfile.TemporaryDirectory() as tmpdir:
            ontology_path, taxonomy_path = generate_data_files(tmpdir)

            assert Path(ontology_path).exists()
            assert Path(taxonomy_path).exists()
            assert 'ontology__call_flow.json' in ontology_path
            assert 'taxonomy__call_flow.json' in taxonomy_path

    def test__generate_data_files__content(self):                                    # Test generated file content
        import json

        with tempfile.TemporaryDirectory() as tmpdir:
            ontology_path, taxonomy_path = generate_data_files(tmpdir)

            with open(ontology_path) as f:
                ontology = json.load(f)

            with open(taxonomy_path) as f:
                taxonomy = json.load(f)

            assert 'ontology_id' in ontology
            assert 'taxonomy_id' in taxonomy
            assert ontology['taxonomy_id'] == taxonomy['taxonomy_id']                # Cross-reference matches
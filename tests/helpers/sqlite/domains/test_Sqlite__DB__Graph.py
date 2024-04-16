from unittest import TestCase

from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Graph import Sqlite__DB__Graph
from osbot_utils.utils.Files import parent_folder, current_temp_folder, file_name
from osbot_utils.utils.Misc import random_text

TEST_DB_GRAPH__DB_NAME   = 'test_db_graph.sqlite'

class test_Sqlite__DB__Graph(TestCase):
    db_name  : str               = TEST_DB_GRAPH__DB_NAME
    db_graph : Sqlite__DB__Graph

    @classmethod
    def setUpClass(cls):
        cls.db_graph = Sqlite__DB__Graph(db_name=cls.db_name)
        cls.db_graph.setup()
        cls.db_graph.table_nodes().set_timestamp = False
        cls.db_graph.table_edges().set_timestamp = False

    @classmethod
    def tearDownClass(cls):
        assert cls.db_graph.delete() is True

    def tearDown(self):
        self.db_graph.clear()

    def test__init__(self):
        with self.db_graph as _:
            assert _.exists()               is True
            assert _.in_memory              is False
            assert parent_folder(_.db_path) == current_temp_folder()
            assert file_name    (_.db_path) == TEST_DB_GRAPH__DB_NAME
            assert _.tables_names()         == ['nodes' , 'idx__nodes__key'      ,
                                                'edges' ,'idx__edges__source_key', 'idx__edges__target_key']

    def test_add_edge(self):
        with self.db_graph as _:
            source_key    = random_text('source_key'   )
            target_key    = random_text('target_key'   )
            edge_value    = random_text('edge_value'   )
            edge_property = random_text('edge_property')
            _.add_edge(source_key, target_key, edge_value, edge_property)
            assert _.nodes()      == [{'id': 1, 'key': source_key, 'properties': None, 'timestamp': 0, 'value': None},
                                      {'id': 2, 'key': target_key, 'properties': None, 'timestamp': 0, 'value': None}]
            assert _.nodes_keys() == [source_key, target_key]
            assert _.edges()      == [{'id': 1, 'properties': edge_property, 'source_key': source_key, 'target_key': target_key, 'timestamp': 0, 'value': edge_value}]


    def test_add_node(self):
        with self.db_graph as _:
            _.add_node('key', 'value', 'property')
            assert _.nodes() == [{'id': 1, 'key': 'key', 'properties': 'property', 'timestamp': 0, 'value': 'value'}]

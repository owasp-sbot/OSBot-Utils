from unittest import TestCase

from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Graph import Sqlite__DB__Graph
from osbot_utils.utils.Files import parent_folder, current_temp_folder, file_name

TEST_DB_GRAPH__DB_NAME   = 'test_db_graph.sqlite'

class test_Sqlite__DB__Graph(TestCase):
    db_name  : str               = TEST_DB_GRAPH__DB_NAME
    db_graph : Sqlite__DB__Graph

    @classmethod
    def setUpClass(cls):
        cls.db_graph = Sqlite__DB__Graph(db_name=cls.db_name)
        cls.db_graph.setup()

    @classmethod
    def tearDownClass(cls):
        assert cls.db_graph.delete() is True

    def test__init__(self):
        with self.db_graph as _:
            assert _.exists()               is True
            assert _.in_memory              is False
            assert parent_folder(_.db_path) == current_temp_folder()
            assert file_name    (_.db_path) == TEST_DB_GRAPH__DB_NAME
            assert _.tables_names()         == ['config', 'idx__config__key',
                                                'nodes', 'idx__nodes__key']


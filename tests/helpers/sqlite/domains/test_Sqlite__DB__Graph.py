from unittest import TestCase

from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Graph import Sqlite__DB__Graph
from osbot_utils.utils.Files import parent_folder, current_temp_folder, file_name


class test_Sqlite__DB__Graph(TestCase):
    db_graph : Sqlite__DB__Graph

    @classmethod
    def setUpClass(cls):
        cls.db_graph = Sqlite__DB__Graph()#.setup()

    @classmethod
    def tearDownClass(cls):
        assert cls.db_graph.delete() is True

    def test__init__(self):
        with self.db_graph as _:
            assert _.exists()               is False                                        # Bug
            assert _.in_memory              is False
            assert parent_folder(_.db_path) == current_temp_folder()
            assert file_name    (_.db_path) is None                                         # Bug

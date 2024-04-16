from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.tables.Sqlite__Table__Files import Sqlite__Table__Files
from osbot_utils.utils.Dev import pprint


class test_test_Sqlite__Table__Nodes(TestCase):
    table_files: Sqlite__Table__Files
    database   : Sqlite__Database

    @classmethod
    def setUpClass(cls):
        cls.table_files = Sqlite__Table__Files()
        cls.database     = cls.table_files.database
        cls.table_files.setup()
        cls.table_files.set_timestamp = False

    def tearDown(self):
        self.table_files.clear()                     # remove any nodes created during test

    def test__init__(self):
        with self.table_files.database as _:
            assert _.exists()  is True
            assert _.in_memory is True
            assert _.db_path   is None

    def test_add_file(self):
        with self.table_files as _:
            assert _.set_timestamp        is False
            assert _.rows () == []
            assert _.files() == []
            new_row  = _.add_file('file/path/file.text', 'some contents', {'a': 42})
            assert new_row.__dict__ == { 'contents' : b'\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00\x8c\rsome contents\x94.',
                                         'metadata' : b'\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00}\x94\x8c\x01a\x94K*s.',
                                         'path'     : 'file/path/file.text'     ,
                                         'timestamp': 0                         }

            assert _.files() == [{'contents': 'some contents', 'id': 1, 'metadata': {'a': 42}, 'path': 'file/path/file.text', 'timestamp': 0}]
            assert _.add_file('file/path/file.text')  is None
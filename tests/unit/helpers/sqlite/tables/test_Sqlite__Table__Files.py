import sys
import pytest
from unittest                                                   import TestCase
from osbot_utils.helpers.sqlite.Sqlite__Database                import Sqlite__Database
from osbot_utils.helpers.sqlite.tables.Sqlite__Table__Files     import Sqlite__Table__Files

class test_Sqlite__Table__Files(TestCase):
    table_files: Sqlite__Table__Files
    database   : Sqlite__Database

    @classmethod
    def setUpClass(cls):
        if sys.version_info < (3, 8):
            pytest.skip("Skipping tests that don't work on 3.7 or lower")

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
            file_path                     = 'file/path/file.text'
            file_contents_metadata        =  {'hash'     : 'b9e6fc6474139fd230ff8a7a9699484c015cb585e1537efad21ae5edf7f79832',
                                              'is_binary': False,
                                              'size'     : 13}
            expected_file_row_no_contents = { 'id': 1, 'metadata': {'a': 42, 'file_contents': file_contents_metadata}, 'path': file_path, 'timestamp': 0}
            expected_file_row             = {'contents': 'some contents', **expected_file_row_no_contents}
            assert _.set_timestamp        is False
            assert _.rows () == []
            assert _.files() == []
            result      = _.add_file(file_path, 'some contents', {'a': 42})
            status      = result.get('status')
            new_row_obj = result.get('data')
            assert new_row_obj.__dict__ == { 'contents' : b'\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00\x8c\rsome contents\x94.',
                                             'metadata' : b'\x80\x04\x95\x7f\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x01'
                                                          b'a\x94K*\x8c\rfile_contents\x94}\x94(\x8c\x04hash\x94\x8c@b9e6'
                                                          b'fc6474139fd230ff8a7a9699484c015cb585e1537efad21ae5edf7f79832'
                                                          b'\x94\x8c\tis_binary\x94\x89\x8c\x04size\x94K\ruu.',
                                             'path'     : 'file/path/file.text'     ,
                                            'timestamp': 0                         }

            assert _.files(include_contents=True ) == [expected_file_row            ]
            assert _.files(include_contents=False) == [expected_file_row_no_contents]
            assert _.files(                      ) == [expected_file_row_no_contents]
            assert _.add_file('file/path/file.text')   == {'data'   : None      ,
                                                           'error'  : None      ,
                                                           'message': "File not added, since file with path 'file/path/file.text' "
                                                                      'already exists in the database',
                                                           'status' : 'warning' }

            assert _.rows       ()                                   == _.files(include_contents=True)
            assert _.file_exists(file_path                        )  is True
            assert _.file       (file_path                        )  == expected_file_row
            assert _.file       (file_path, include_contents=False)  == expected_file_row_no_contents
            assert _.file_without_contents(file_path              )  == expected_file_row_no_contents

            assert _.delete_file(file_path) == {'data': None, 'error': None, 'message': 'file deleted', 'status': 'ok'}
            assert _.files      ()          == []
            assert _.rows       ()          == []
            assert _.file       (file_path) is None
            assert _.file_exists(file_path) is False

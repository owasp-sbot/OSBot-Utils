from unittest import TestCase

from osbot_utils.testing.Temp_File import Temp_File
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import Files, file_exists, folder_exists, file_not_exists, folder_not_exists, \
    file_extension, file_name, parent_folder


class test_Temp_File(TestCase):

    def test__init__(self):
        temp_file = Temp_File()
        assert temp_file.tmp_folder               is None
        assert temp_file.file_path                is None
        assert type(temp_file.tmp_file)           is str
        assert file_extension(temp_file.tmp_file) == '.tmp'
        assert temp_file.original_contents        == '...'
        assert temp_file.exists()                 is False
        assert temp_file.contents()               is None

    def test__confirm_file_and_folder_creation_and_deletion(self):
        with Temp_File() as _:
            assert _.exists()                    is True
            assert _.contents()                  == '...'
            assert file_exists   (_.file_path )  is True
            assert folder_exists (_.tmp_folder)  is True
        assert file_not_exists   (_.file_path )  is True
        assert folder_not_exists (_.tmp_folder)  is True

    def test__using_with__no_params(self):
        with Temp_File() as temp_file:
            assert Files.file_extension(temp_file.file_path) == '.tmp'
            assert Files.exists  (temp_file.file_path)
            assert Files.contents(temp_file.file_path) == '...'
        assert Files.not_exists(temp_file.file_path)

        with Temp_File('abc','txt') as temp_file:
            assert Files.file_extension(temp_file.file_path) == '.txt'
            assert Files.exists  (temp_file.file_path)
            assert Files.contents(temp_file.file_path) == 'abc'
        assert Files.not_exists(temp_file.file_path)

    def test_file_name(self):
        with Temp_File() as _:
            assert _.file_name().endswith('.tmp')
            files =  _.files_in_folder()
            assert len(files) == 1
            assert file_name(files[0]) == _.file_name()
            assert parent_folder(files[0]) == _.folder()


    def test_write(self):
        with Temp_File() as _:
            assert _.contents(     ) == '...'
            assert _.write   ('abc') == _
            assert _.contents(     ) == 'abc'
            assert _.delete  (     ) is True
            assert _.exists  (     ) is False
            assert _.contents(     ) is None
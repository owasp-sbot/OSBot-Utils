from unittest import TestCase

from osbot_utils.testing.Temp_File import Temp_File
from osbot_utils.utils.Files import Files, file_exists, folder_exists, file_not_exists, folder_not_exists, \
    file_extension


class test_Temp_File(TestCase):

    def test__init__(self):
        temp_file = Temp_File()
        assert temp_file.tmp_folder               is None
        assert temp_file.file_path                is None
        assert type(temp_file.tmp_file)           is str
        assert file_extension(temp_file.tmp_file) == '.tmp'
        assert temp_file.contents                 == '...'

    def test__confirm_file_and_folder_creation_and_deletion(self):
        with Temp_File() as _:
            assert file_exists   (_.file_path)
            assert folder_exists (_.tmp_folder)
        assert file_not_exists   (_.file_path)
        assert folder_not_exists (_.tmp_folder)

    def test__using_with__no_params(self):
        with Temp_File() as temp:
            assert Files.file_extension(temp.file_path) == '.tmp'
            assert Files.exists  (temp.file_path)
            assert Files.contents(temp.file_path) == '...'
        assert Files.not_exists(temp.file_path)

        with Temp_File('abc','txt') as temp:
            assert Files.file_extension(temp.file_path) == '.txt'
            assert Files.exists  (temp.file_path)
            assert Files.contents(temp.file_path) == 'abc'
        assert Files.not_exists(temp.file_path)

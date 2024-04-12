from unittest import TestCase

import pytest

from osbot_utils.testing.Unzip_File import Unzip_File
from osbot_utils.utils.Misc import random_text, list_set, in_github_action

from osbot_utils.testing.Temp_File import Temp_File
from osbot_utils.utils.Files import file_exists, file_delete, file_extension, file_contents
from osbot_utils.testing.Temp_Folder import Temp_Folder
from osbot_utils.testing.Temp_Zip_In_Memory import Temp_Zip_In_Memory
from osbot_utils.utils.Zip import zip_files_to_bytes, zip_file_list, zip_bytes_file_list, zip_bytes_to_file, \
    zip_bytes_get_file


class test_Temp_Zip_In_Memory(TestCase):

    def test__with__default_params(self):
        with Temp_Zip_In_Memory() as _:
            assert _.targets == []

    def test_add_file_from_content(self):
        with Temp_Zip_In_Memory() as _:
            assert _.zip_bytes_files() == []
            _.add_file_from_content('file_1.txt', 'file_1 contents')
            assert _.zip_bytes_files() == ['file_1.txt']
            assert _.zip_bytes_file_content('file_1.txt') == b'file_1 contents'

    def test_all_source_files(self):
        if in_github_action():
            pytest.skip("every now and then this test fails in github actions")

        with Temp_Folder() as temp_folder:
            max_total_files = 3 #30                                                 # was taking 100ms with 30 files . with 3 it takes about 16ms
            temp_folder.add_temp_files_and_folders(max_total_files=max_total_files)
            assert len(temp_folder.files()) == max_total_files
            with Temp_Zip_In_Memory() as _:
                _.add_folder(temp_folder)
                _.set_root_folder(temp_folder)
                assert temp_folder.files(show_parent_folder=True) == _.target_files()
                zip_bytes = _.zip_bytes()
                assert len(zip_bytes) > 256

                assert _.zip_bytes_files() == temp_folder.files()

    def test_target_files_with_root_folder(self):
        with Temp_File() as temp_file:
            with Temp_Folder() as temp_folder:
                max_total_files = 10
                temp_folder.add_temp_files_and_folders(max_total_files=max_total_files)
                assert len(temp_folder.files()) == max_total_files
                with Temp_Zip_In_Memory() as _:
                    _.add_folder(temp_folder)
                    _.add_file(temp_file)
                    assert _.targets == [{'target': temp_folder.path(), 'root_folder': None},
                                         {'target': temp_file.path()  , 'root_folder': None}]
                    target_files = _.target_files_with_root_folder()
                    assert len(target_files) == max_total_files + 1
                    for entry in target_files:
                        assert list_set(entry.keys()) == ['file', 'root_folder']

    def test_zip_bytes_file(self):
        with Temp_File() as temp_file:
            with Temp_Zip_In_Memory() as _:
                _.add_file(temp_file, root_folder=temp_file.folder())
                assert _.zip_bytes_files() == [temp_file.file_name()]
                new_file_name     = 'an_path/an_file.txt'
                new_file_contents = random_text('some contents')
                # todo: add native support for in memory files
                #new_zip_bytes = _.zip_bytes_add_file_from_bytes(new_file_name, new_file_contents)
                _.add_file_from_content(new_file_name, new_file_contents)
                assert _.zip_bytes_files() == sorted([new_file_name, temp_file.file_name()])

                with Temp_File() as temp_file_zip:
                    zip_bytes_to_file(_.zip_bytes(), temp_file_zip.path())
                    assert file_exists(temp_file_zip.path()) is True
                    with Unzip_File(temp_file_zip.path()) as unzipped_folder:
                        path_test_file = unzipped_folder.path() + '/' + new_file_name
                        assert path_test_file in unzipped_folder.files()
                        assert file_contents(path_test_file) == new_file_contents

                file_contents_from_bytes = zip_bytes_get_file(_.zip_bytes(), new_file_name)
                assert file_contents_from_bytes.decode() == new_file_contents

    def test_create_zip_file(self):
        with Temp_Folder(temp_files_to_add=3) as temp_folder:
            with Temp_Zip_In_Memory() as _:
                _.add_folder(temp_folder)
                _.set_root_folder(temp_folder)
                assert _.root_folder == temp_folder.path()

                assert _.targets == [{'target': temp_folder.path(), 'root_folder': None}]
                for target in _.target_files_with_root_folder():
                    assert list_set(target) == ['file', 'root_folder']          # make sure the target_files_with_root_folder() returns the expected data
                    assert file_exists(target.get('file')) is True              # make sure the file exists
                    assert target.get('root_folder') == _.root_folder
                target_zip_file = _.create_zip_file()  # save in memory zip into disk
                assert file_exists(target_zip_file)                             # make sure it exists
                assert file_extension(target_zip_file) == '.zip'                # make sure it has the right extension
                assert temp_folder.files() == zip_file_list(target_zip_file)    # confirm that all files inside temp_folder are inside the in memory zip file

        assert file_delete(target_zip_file) is True                             # delete the zip file


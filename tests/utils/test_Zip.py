from unittest import TestCase

from osbot_utils.testing.Temp_Zip import Temp_Zip
from osbot_utils.utils.Dev import pprint

from osbot_utils.testing.Temp_Folder import Temp_Folder
from osbot_utils.utils.Misc import random_string

from osbot_utils.utils.Files import file_contents, folder_files, temp_folder_with_temp_file, file_exists, \
    file_extension, folder_exists, file_name
from osbot_utils.utils.Zip import zip_file_list, unzip_file, folder_zip


class test_Zip(TestCase):

    def test_folder_zip(self):
        folder = temp_folder_with_temp_file(file_contents=random_string())
        print()

        zip_file = folder_zip(folder)

        assert file_exists   (zip_file) is True
        assert file_extension(zip_file) == '.zip'

        unziped_folder = unzip_file(zip_file)

        source_files  = folder_files(folder)
        target_files  = folder_files(unziped_folder)

        assert len(source_files) == 1
        assert len(target_files) == 1
        assert source_files[0]   != target_files[0]

        assert file_contents(source_files[0]) == file_contents(target_files[0])

        assert zip_file_list(zip_file)        == ['temp_file.txt']

    def test_zip_file_list(self):
        with Temp_Folder() as temp_folder:
            file_1_name     = 'file_1.txt'
            file_1_contents = 'file 1 contents'
            file_2_name     = 'file_2.txt'
            file_2_contents = 'file 2 contents'
            temp_file_1 = temp_folder.add_file(file_1_name, file_1_contents)
            temp_file_2 = temp_folder.add_file(file_2_name, file_2_contents)
            target_folder = temp_folder.path()
            assert temp_folder.files(show_parent_folder=True) == [temp_file_1, temp_file_2]
            with Temp_Zip(target_folder) as temp_zip:
                assert temp_zip.zip_file_exists() is True
                assert temp_zip.target_zipped     is True

                assert temp_zip.files() == ['file_1.txt', 'file_2.txt']
            assert temp_folder.exists()  is True

        assert temp_folder.exists()         is False
        assert folder_exists(target_folder) is False
        assert file_exists  (temp_file_1  ) is False
        assert file_exists  (temp_file_2  ) is False

    def test_zip_file_list__nested_folders(self):
        # root folder
        with Temp_Folder() as temp_folder_1:
            file_1_path = temp_folder_1.add_file('file_1.txt')
            # root folder / nested folder 1
            with Temp_Folder(parent_folder=temp_folder_1) as temp_folder_2:
                file_2_path = temp_folder_2.add_file('file_2.txt')
                assert temp_folder_1.files  (show_parent_folder=True) == [file_1_path, file_2_path]
                assert temp_folder_2.files  (show_parent_folder=True) == [file_2_path]
                assert temp_folder_1.folders(show_parent_folder=True) == [temp_folder_2.path()]
                assert temp_folder_1.files() == [file_name(file_1_path), f'{temp_folder_2.folder_name}/{file_name(file_2_path)}']
                assert temp_folder_2.files() == [file_name(file_2_path)]
                assert temp_folder_1.folders() == [temp_folder_2.folder_name]
                # root folder / nested folder 1 / nested folder 2
                with Temp_Folder(parent_folder=temp_folder_2) as temp_folder_3:
                    file_3_path = temp_folder_3.add_file('file_3.txt')
                    assert temp_folder_1.files  (show_parent_folder=True) == [file_1_path, file_2_path, file_3_path     ]
                    assert temp_folder_2.files  (show_parent_folder=True) == [file_2_path, file_3_path                  ]
                    assert temp_folder_3.files  (show_parent_folder=True) == [file_3_path                               ]
                    assert temp_folder_1.folders(show_parent_folder=True) == [temp_folder_2.path(), temp_folder_3.path()]
                    assert temp_folder_2.folders(show_parent_folder=True) == [temp_folder_3.path()                      ]
                    assert temp_folder_1.files()   == [file_name(file_1_path), f'{temp_folder_2.folder_name}/{file_name(file_2_path)}', f'{temp_folder_2.folder_name}/{temp_folder_3.folder_name}/{file_name(file_3_path)}']
                    assert temp_folder_2.files()   == [file_name(file_2_path), f'{temp_folder_3.folder_name}/{file_name(file_3_path)}']
                    assert temp_folder_1.folders() == [temp_folder_2.folder_name, f'{temp_folder_2.folder_name}/{temp_folder_3.folder_name}']
                    assert temp_folder_1.files(include_folders=True) == [   file_name(file_1_path),
                                                                         f'{temp_folder_2.folder_name}/',
                                                                         f'{temp_folder_2.folder_name}/{file_name(file_2_path)}',
                                                                         f'{temp_folder_2.folder_name}/{temp_folder_3.folder_name}/',
                                                                         f'{temp_folder_2.folder_name}/{temp_folder_3.folder_name}/{file_name(file_3_path)}']
                    with Temp_Zip(temp_folder_1) as temp_zip:
                        assert temp_zip.files() == temp_folder_1.files(include_folders=True)

        assert temp_folder_1.exists() is False
        assert temp_folder_2.exists() is False
        assert temp_folder_3.exists() is False

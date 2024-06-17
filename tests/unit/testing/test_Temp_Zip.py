import json
from unittest import TestCase

from osbot_utils.testing.Temp_Folder import Temp_Folder
from osbot_utils.testing.Temp_Zip    import Temp_Zip
from osbot_utils.utils.Files import is_file, file_exists, is_folder, folder_exists, file_name
from osbot_utils.utils.Objects import obj_data


class test_Zip_Folder(TestCase):

    def test__with__default_params(self):
        with Temp_Zip() as _:
            assert type(_)     is Temp_Zip
            assert obj_data(_) == dict(delete_zip_file = True  ,
                                       target          = None  ,
                                       target_zip_file = None  ,
                                       target_zipped   = False ,
                                       zip_bytes       = None  ,
                                       zip_file        = None  )


    def test_files(self):
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

    def test__using_folder(self):
        with Temp_Folder() as temp_folder:
            target = temp_folder.path()
            with Temp_Zip(temp_folder) as temp_zip:
                zip_file = temp_zip.path()
                assert is_folder(target  )    is True
                assert is_file  (target  )    is False
                assert is_file  (zip_file)    is True
                assert is_folder(zip_file)    is False
                assert temp_zip.target_zipped is True

                assert temp_zip.files() == []

        assert file_exists  (zip_file) is False
        assert is_file      (zip_file) is False
        assert is_folder    (target  ) is False
        assert folder_exists(target  ) is False




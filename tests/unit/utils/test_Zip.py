from unittest import TestCase

import osbot_utils
from osbot_utils.helpers.Zip_Bytes import Zip_Bytes
from osbot_utils.testing.Temp_File import Temp_File
from osbot_utils.testing.Temp_Zip import Temp_Zip
from osbot_utils.testing.Temp_Folder import Temp_Folder
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import random_string, str_to_bytes, list_set

from osbot_utils.utils.Files import file_contents, folder_files, temp_folder_with_temp_file, file_exists, \
    file_extension, folder_exists, file_name, parent_folder, files_list, is_file, is_folder
from osbot_utils.utils.Zip import zip_file__list, unzip_file, folder_zip, zip_bytes_empty, zip_bytes__file_list, \
    zip_bytes__add_file, zip_bytes__file, zip_bytes__files, zip_bytes__remove_file, zip_bytes__file_contents, \
    zip_bytes__replace_file


# todo: add missing unit tests (lots missing from this class)

class test_Zip(TestCase):

    # actions on zipped bytes

    def test_zip_bytes__add_file(self):

        new_file_1__path      = 'new_file_1.txt'
        new_file_1__contents  = b'some content 1'
        new_file_2__contents  = b'some content 2'
        zip_bytes_1           = zip_bytes__add_file(zip_bytes_empty() , new_file_1__path, new_file_1__contents)
        zip_bytes_2           = zip_bytes__add_file(zip_bytes_1       , new_file_1__path, new_file_2__contents)

        assert zip_bytes__file_list    (zip_bytes_1                     ) == [ new_file_1__path ]
        assert zip_bytes__file_list    (zip_bytes_2                     ) == [ new_file_1__path , new_file_1__path]
        assert zip_bytes__file_contents(zip_bytes_1, new_file_1__path   ) == new_file_1__contents
        assert zip_bytes__file_contents(zip_bytes_2, new_file_1__path   ) == new_file_2__contents
        assert zip_bytes__file_contents(zip_bytes_2, zip_file_path=None ) is None
        assert zip_bytes__file_contents(zip_bytes_2, zip_file_path='aaa') is None

    def test_zip_bytes__add_file__from_disk(self):
        with Zip_Bytes() as _:
            base_folder = parent_folder(osbot_utils.path)
            target_file = __file__
            assert _.files              (                               ) == {}
            assert _.add_file__from_disk(base_folder, target_file       ) == _
            assert _.files_list         (                               ) == ['tests/unit/utils/test_Zip.py']
            assert _.file               ('tests/unit/utils/test_Zip.py') == str_to_bytes(file_contents(target_file))

    def test_zip_bytes__add_files__from_disk(self):
        with Zip_Bytes() as _:
            base_folder  = osbot_utils.path
            files_to_add = files_list(base_folder, pattern="decorators/**/*.py")
            _.add_files__from_disk(base_folder, files_to_add)
            assert 15 < _.size()  ==  len(files_to_add) < 30
            assert 'decorators/methods/cache_on_self.py' in _.files_list()


    def test_zip_bytes__remove_files(self):
        zip_bytes_1           = zip_bytes_empty()
        new_file_1__path      = 'new_file_1.txt'
        new_file_1__contents  = b'some content 1'
        new_file_2__path      = 'new_file_2.txt'
        new_file_2__contents  = b'some content 2'
        zip_bytes_2           = zip_bytes__add_file(zip_bytes_1   , new_file_1__path, new_file_1__contents)
        zip_bytes_3           = zip_bytes__add_file(zip_bytes_2   , new_file_2__path, new_file_2__contents)
        zip_bytes_4           = zip_bytes__remove_file(zip_bytes_3, new_file_1__path                      )
        zip_bytes_5           = zip_bytes__remove_file(zip_bytes_4, new_file_2__path                      )

        assert zip_bytes__file_list(zip_bytes_1                  ) == []

        assert zip_bytes__file_list(zip_bytes_2                  ) == [ new_file_1__path ]
        assert zip_bytes__file     (zip_bytes_2, new_file_1__path) == new_file_1__contents
        assert zip_bytes__file     (zip_bytes_2, new_file_2__path) is None
        assert zip_bytes__files    (zip_bytes_2                  ) == { new_file_1__path: new_file_1__contents}

        assert zip_bytes__file_list(zip_bytes_3                  ) == [ new_file_1__path , new_file_2__path]
        assert zip_bytes__file     (zip_bytes_3, new_file_1__path) == new_file_1__contents
        assert zip_bytes__file     (zip_bytes_3, new_file_2__path) == new_file_2__contents
        assert zip_bytes__files    (zip_bytes_3                  ) == { new_file_1__path: new_file_1__contents, new_file_2__path: new_file_2__contents}

        assert zip_bytes__file_list(zip_bytes_4                  ) == [ new_file_2__path ]
        assert zip_bytes__files    (zip_bytes_4                  ) == { new_file_2__path: new_file_2__contents}

        assert zip_bytes__file_list(zip_bytes_5                  ) == [  ]

    def test_zip_bytes__replace_file(self):

        new_file_1__path      = 'new_file_1.txt'
        new_file_3__path      = 'new_file_3.txt'
        new_file_1__contents  = b'some content 1'
        new_file_2__contents  = b'some content 2'
        new_file_3__contents  = b'some content 3'

        zip_bytes_1           = zip_bytes__add_file    (zip_bytes_empty() , new_file_1__path, new_file_1__contents)
        zip_bytes_2           = zip_bytes__replace_file(zip_bytes_1       , new_file_1__path, new_file_2__contents)
        zip_bytes_3           = zip_bytes__replace_file(zip_bytes_2       , new_file_3__path, new_file_3__contents)

        assert zip_bytes__file_list    (zip_bytes_1                  ) == [ new_file_1__path ]
        assert zip_bytes__file_contents(zip_bytes_1, new_file_1__path) == new_file_1__contents

        assert zip_bytes__file_list    (zip_bytes_2                  ) == [ new_file_1__path ]
        assert zip_bytes__file_contents(zip_bytes_2, new_file_1__path) == new_file_2__contents

        assert zip_bytes__file_list    (zip_bytes_3                  ) == [ new_file_1__path , new_file_3__path]
        assert zip_bytes__file_contents(zip_bytes_3, new_file_1__path) == new_file_2__contents
        assert zip_bytes__file_contents(zip_bytes_3, new_file_3__path) == new_file_3__contents

    def test_zip_bytes__replace_files(self):
        file_1           = 'path_a/path_b/file_1.txt'
        contents_1       = b'file 1 contents'
        contents_2       = b'file 2 contents'
        add_files_1      = {'y.txt': b'y'    , 'z.txt': b'z'       }
        replace_files_1  = {'y.txt': b'y_new', 'z.txt': b'z_new'   }
        expected_files_1 = { file_1:contents_1                     }
        expected_files_2 = { file_1:contents_1, **add_files_1      }
        expected_files_3 = { file_1: contents_1, **replace_files_1 }
        expected_files_4 = { file_1: contents_2, **replace_files_1 }

        with Zip_Bytes() as _:
            assert _.files() == {}

            assert _.add_file     (file_1, contents_1) == _
            assert _.file         (file_1            ) == contents_1
            assert _.files        (                  ) == expected_files_1
            assert _.files_list   (                  ) == list_set(expected_files_1)

            assert _.add_files    (add_files_1       ) == _
            assert _.file         (file_1            ) == contents_1
            assert _.file         ('y.txt'           ) == b'y'
            assert _.file         ('z.txt'           ) == b'z'
            assert _.files        (                  ) == expected_files_2
            assert _.files_list   (                  ) == list_set(expected_files_2)

            assert _.replace_files(replace_files_1   ) == _
            assert _.file         (file_1            ) == contents_1
            assert _.file         ('y.txt'           ) == b'y_new'
            assert _.file         ('z.txt'           ) == b'z_new'
            assert _.files        (                  ) == expected_files_3
            assert _.files_list   (                  ) == list_set(expected_files_3)

            assert _.replace_file (file_1, contents_2) == _
            assert _.file         (file_1            ) == contents_2
            assert _.file         ('y.txt'           ) == b'y_new'
            assert _.file         ('z.txt'           ) == b'z_new'
            assert _.files        (                  ) == expected_files_4
            assert _.files_list   (                  ) == list_set(expected_files_4)

    # actions on zipped files

    def test_zip__file_list(self):
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

    # zip creation actions

    def test_folder_zip(self):
        folder = temp_folder_with_temp_file(file_contents=random_string())
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

        assert zip_file__list(zip_file) == ['temp_file.txt']


    # performance tests

    #def test__performance__zip_bytes__osbot_utils(self):



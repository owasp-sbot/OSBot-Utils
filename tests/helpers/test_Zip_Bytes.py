from unittest import TestCase

import osbot_utils
from osbot_utils.helpers.Zip_Bytes import Zip_Bytes
from osbot_utils.testing.Temp_Folder import Temp_Folder
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import path_combine, files_list, file_delete, file_not_exists, file_exists, file_bytes
from osbot_utils.utils.Zip import zip_file__list


class test_Zip_Bytes(TestCase):

    def test_add_folder(self):
        with Zip_Bytes() as _:
            assert _.empty() is True
            base_folder   = osbot_utils.path
            target_folder = path_combine(base_folder, 'decorators')
            _.add_folder__from_disk(base_folder, target_folder, pattern="*.py")
            assert _.empty() is False
            assert _.size() == len(files_list(base_folder, pattern="decorators/**/*.py"))
            assert 'decorators/methods/cache_on_self.py' in _.files_list()
            assert '__init__.py' not in _.files_list()

    def test_save(self):
        with Zip_Bytes() as _:
            _.add_file('aaaa', 'bbbb')
            saved_zip_file = _.save()
            assert zip_file__list(saved_zip_file) == ['aaaa']
            with Temp_Folder() as temp_folder:
                new_zip_file  = path_combine(temp_folder.full_path, 'bbbb.zip')
                assert file_not_exists(new_zip_file)    is True
                assert _.save_to(new_zip_file)          == new_zip_file
                assert file_exists(new_zip_file)        is True
                assert zip_file__list(new_zip_file)     == ['aaaa']
                assert file_bytes(new_zip_file)         == file_bytes(saved_zip_file)

                assert file_delete(new_zip_file  )      is True
                assert file_delete(saved_zip_file)      is True




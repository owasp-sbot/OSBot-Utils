from unittest import TestCase

import osbot_utils
from osbot_utils.helpers.Zip_Bytes import Zip_Bytes
from osbot_utils.utils.Files import path_combine, files_list


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

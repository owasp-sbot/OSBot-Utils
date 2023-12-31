import json
from unittest import TestCase

from osbot_utils.testing.Temp_Folder import Temp_Folder
from osbot_utils.utils.Misc import obj_data, print_obj_data_as_dict

from osbot_utils.utils.Dev import pprint

from osbot_utils.testing.Temp_Zip    import Temp_Zip
from osbot_utils.utils.Files import Files, parent_folder, is_file, file_exists, is_folder, folder_exists


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

                pprint(temp_zip.files())

        assert file_exists  (zip_file) is False
        assert is_file      (zip_file) is False
        assert is_folder    (target  ) is False
        assert folder_exists(target  ) is False




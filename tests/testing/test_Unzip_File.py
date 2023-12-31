from pprint import pprint
from unittest import TestCase

from osbot_utils.utils.Misc import obj_info, print_obj_data_as_dict, obj_data

from osbot_utils.testing.Temp_Folder import Temp_Folder
from osbot_utils.testing.Temp_Zip import Temp_Zip
from osbot_utils.testing.Unzip_File import Unzip_File
from osbot_utils.utils.Files import Files, parent_folder, folder_exists, file_name, files_list, path_combine


class test_Unzip_File(TestCase):

    def test__using_with__no_params(self):
        with Unzip_File() as unzip_file:
            assert type(unzip_file) is Unzip_File
        assert obj_data(unzip_file) == dict(delete_target_folder  = True ,
                                            files_unzipped        = False,
                                            target_folder         = None ,
                                            target_folder_deleted = False,
                                            zip_file              = None )

    def test__using_with_valid_zip_and_target_folder(self):
        with Temp_Folder() as source_folder:
            temp_file = source_folder.add_file()
            with Temp_Folder() as target_folder:
                with Temp_Zip(source_folder) as temp_zip:
                    zip_file = temp_zip.path()
                    with Unzip_File(zip_file,target_folder.path(),True) as unzip_file:
                        assert obj_data(unzip_file) == dict(delete_target_folder  = True                 ,
                                                            files_unzipped        = True                 ,
                                                            target_folder         = target_folder.path() ,
                                                            target_folder_deleted = False                ,
                                                            zip_file              = zip_file             )
                        assert unzip_file.path()  == target_folder.path()
                        assert temp_zip.files() == [file_name(temp_file)]

        assert obj_data(unzip_file) == dict(delete_target_folder  = True                 ,
                                            files_unzipped        = True                 ,
                                            target_folder         = target_folder.path() ,
                                            target_folder_deleted = True                 ,      # this value should now be true because we are outside the with block
                                            zip_file              = zip_file             )

    def test__using_with_valid_zip_no_target_folder(self):
        with Temp_Folder() as temp_folder:
            temp_file = temp_folder.add_file()
            with Temp_Zip(temp_folder) as temp_zip:
                assert temp_zip.target_zipped is True
                assert temp_zip.files() == [file_name(temp_file)]
                zip_file = temp_zip.path()
                with Unzip_File(zip_file,target_folder=None,delete_target_folder=True) as unzip_file:
                    assert folder_exists(unzip_file.path()) is True
                    assert unzip_file.files() == [path_combine(unzip_file.path(), file_name(temp_file))]
        assert folder_exists(temp_folder) is False




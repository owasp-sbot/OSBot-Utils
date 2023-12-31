from osbot_utils.utils.Files import Files, folder_exists, folder_delete_all, temp_folder, files_recursive
from osbot_utils.utils.Zip import unzip_file


class Unzip_File:
    def __init__(self, zip_file=None, target_folder=None, delete_target_folder=True):
        self.target_folder          = target_folder
        self.zip_file               = zip_file
        self.delete_target_folder   = delete_target_folder
        self.files_unzipped         = False
        self.target_folder_deleted  = False

    def __enter__(self):
        if Files.exists(self.zip_file):
            if self.target_folder is None:
                self.target_folder = temp_folder("unzipped_")
            unzip_file(self.zip_file, self.target_folder)
            self.files_unzipped = True
        return self

    def __exit__(self, type, value, traceback):
        if folder_exists(self.target_folder) and self.delete_target_folder:
            self.target_folder_deleted = folder_delete_all(self.target_folder)
            #print("\n\ndeleting", self.target_folder)

    def path(self):
        return self.target_folder

    def files(self):
        return files_recursive(self.target_folder)
from osbot_utils.testing.Temp_Folder import Temp_Folder
from osbot_utils.utils.Files import Files, is_folder, file_exists, file_name, file_move_to_folder, file_move, \
    file_move_to
from osbot_utils.utils.Zip import zip_folder, zip_file__list


class Temp_Zip():
    def __init__(self, target=None, target_zip_file=None, delete_zip_file=True):
        if type(target) is Temp_Folder:
            target = target.path()
        self.target          = target
        self.delete_zip_file = delete_zip_file
        self.target_zip_file = target_zip_file
        self.zip_file        = None
        self.zip_bytes       = None
        self.target_zipped   = False

    def __enter__(self):
        if is_folder(self.target):
            self.zip_file = zip_folder(self.target)
            self.target_zipped = True
        return self

    def __exit__(self, type, value, traceback):
        if Files.exists(self.zip_file) and self.delete_zip_file:
            Files.delete(self.zip_file)

    def __repr__(self):
        return f"<Temp_Zip: {self.path()}>"

    def file_name(self):
        return file_name(self.zip_file)

    def path(self):
        return self.zip_file

    def files(self):
        return zip_file__list(self.zip_file)

    def print_path(self):
        print()
        print(self.path())
        return self

    def zip_file_exists(self):
        return file_exists(self.zip_file)

    def move_to(self, target_file):
        file_move_to(self.zip_file, target_file)
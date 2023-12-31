from osbot_utils.utils.Files import Files, file_delete, folder_delete_all, files_list, file_create, file_name, \
    parent_folder
from osbot_utils.utils.Misc import random_filename


class Temp_File:
    def __init__(self, contents='...', extension='tmp'):
        self.tmp_file   = random_filename(extension)
        self.tmp_folder = None
        self.file_path  = None
        self.contents   = contents

    def __enter__(self):
        self.tmp_folder = Files.temp_folder()
        self.file_path = Files.path_combine(self.tmp_folder, self.tmp_file)
        file_create(self.file_path, self.contents)
        return self

    def __exit__(self, type, value, traceback):
        file_delete      (self.file_path)
        folder_delete_all(self.tmp_folder)

    def file_name(self):
        return file_name(self.path())

    def files_in_folder(self):
        return files_list(self.tmp_folder)

    def folder(self):
        return parent_folder(self.path())

    def path(self):
        return self.file_path

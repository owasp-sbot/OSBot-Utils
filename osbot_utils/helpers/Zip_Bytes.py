from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import files_list, file_create_from_bytes, temp_file, parent_folder, parent_folder_create
from osbot_utils.utils.Misc import random_text
from osbot_utils.utils.Zip import zip_bytes_empty, zip_bytes__files, zip_bytes__add_file, zip_bytes__add_files, \
    zip_bytes__replace_files, zip_bytes__replace_file, zip_bytes__file_list, zip_bytes__file, \
    zip_bytes__add_file__from_disk, zip_bytes__add_files__from_disk


class Zip_Bytes(Type_Safe):
    zip_bytes : bytes

    def __enter__(self):
        self.zip_bytes = zip_bytes_empty()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_file(self, file_path, file_contents):
        self.zip_bytes = zip_bytes__add_file(self.zip_bytes, file_path, file_contents)
        return self

    def add_file__from_disk(self, base_path, file_to_add):
        self.zip_bytes = zip_bytes__add_file__from_disk(self.zip_bytes, base_path, file_to_add)
        return self

    def add_files(self, files_to_add):
        self.zip_bytes = zip_bytes__add_files(self.zip_bytes, files_to_add)
        return self

    def add_files__from_disk(self, base_path, files_to_add):
        self.zip_bytes = zip_bytes__add_files__from_disk(self.zip_bytes, base_path, files_to_add)
        return self

    def add_folder__from_disk(self, base_path, folder_to_add, pattern="*"):
        files_to_add = files_list(folder_to_add, pattern=pattern)
        return self.add_files__from_disk(base_path, files_to_add)

    def add_random_file(self):
        random_file_name     = random_text('file_name'    )
        random_file_contents = random_text('file_contents')
        self.add_file(random_file_name, random_file_contents)
        return self

    def empty(self):
        return self.size() == 0

    def file(self, file_path):
        return zip_bytes__file(self.zip_bytes, file_path)

    def files(self):
        return zip_bytes__files(self.zip_bytes)

    def files_list(self):
        return zip_bytes__file_list(self.zip_bytes)

    def print_files_list(self):
        pprint(self.files_list())
        return self
    def replace_files(self, files_to_replace):
        self.zip_bytes = zip_bytes__replace_files(self.zip_bytes, files_to_replace)
        return self

    def replace_file(self, file_path, file_contents):
        self.zip_bytes = zip_bytes__replace_file(self.zip_bytes, file_path, file_contents)
        return self

    def save(self, path=None):
        if path is None:
            path = temp_file(extension='.zip')
        zip_file = file_create_from_bytes(bytes=self.zip_bytes, path=path)
        return zip_file

    def save_to(self, path):
        parent_folder_create(path)           # make sure the parent folder exists
        return self.save(path)


    def size(self):
        return len(self.files_list())
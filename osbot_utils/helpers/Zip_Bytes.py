from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import files_list
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

    def size(self):
        return len(self.files_list())
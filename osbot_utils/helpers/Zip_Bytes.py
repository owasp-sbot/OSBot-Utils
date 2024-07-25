from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import files_list, file_create_from_bytes, temp_file, parent_folder, parent_folder_create
from osbot_utils.utils.Misc import random_text
from osbot_utils.utils.Regex import list__match_regex, list__match_regexes
from osbot_utils.utils.Zip import zip_bytes_empty, zip_bytes__files, zip_bytes__add_file, zip_bytes__add_files, \
    zip_bytes__replace_files, zip_bytes__replace_file, zip_bytes__file_list, zip_bytes__file, \
    zip_bytes__add_file__from_disk, zip_bytes__add_files__from_disk, zip_files, zip_file__files, zip_bytes__remove_files


class Zip_Bytes(Type_Safe):
    zip_bytes : bytes = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zip_bytes = zip_bytes_empty()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_file(self, file_path, file_contents):
        self.zip_bytes = zip_bytes__add_file(self.zip_bytes, file_path, file_contents)
        return self

    def add_file__from_disk(self, file_to_add, base_path=None):
        if base_path is None:
            base_path = parent_folder(file_to_add)
        self.zip_bytes = zip_bytes__add_file__from_disk(self.zip_bytes, base_path, file_to_add)
        return self

    def add_files(self, files_to_add):
        self.zip_bytes = zip_bytes__add_files(self.zip_bytes, files_to_add)
        return self

    def add_files__from_disk(self, base_path, files_to_add, path_prefix=None):
        self.zip_bytes = zip_bytes__add_files__from_disk(self.zip_bytes, base_path, files_to_add, path_prefix=path_prefix)
        return self

    def add_folder__from_disk(self, folder_to_add, *patterns):
        base_path           = folder_to_add
        all_files_in_folder = files_list(folder_to_add)
        files_to_add        = list__match_regexes(all_files_in_folder, *patterns)
        return self.add_files__from_disk(base_path, files_to_add)

    def add_random_file(self):
        random_file_name     = random_text('file_name'    )
        random_file_contents = random_text('file_contents')
        self.add_file(random_file_name, random_file_contents)
        return self

    def add_folder__from_disk__with_prefix(self, folder_to_add, path_prefix, *patterns):
        base_path           = folder_to_add
        all_files_in_folder = files_list(folder_to_add)
        files_to_add        = list__match_regexes(all_files_in_folder, *patterns)
        return self.add_files__from_disk(base_path, files_to_add, path_prefix=path_prefix)

    def add_from_zip_file(self, path_zip_file):
        files_to_add = zip_file__files(path_zip_file)
        self.add_files(files_to_add)
        return self

    def empty(self):
        return self.size() == 0

    def file(self, file_path):
        return zip_bytes__file(self.zip_bytes, file_path)

    def file_paths(self):
        return self.files_list()

    def files(self):
        return zip_bytes__files(self.zip_bytes)

    def files_list(self):
        return zip_bytes__file_list(self.zip_bytes)

    def list(self):
        return self.files_list()

    def print_files_list(self):
        pprint(self.files_list())
        return self

    def remove_files(self, *patterns):
        files_to_remove = list__match_regexes(self.files_list(), *patterns)
        self.zip_bytes = zip_bytes__remove_files(self.zip_bytes, files_to_remove)
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
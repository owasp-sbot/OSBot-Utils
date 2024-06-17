import io

from osbot_utils.testing.Temp_File import Temp_File
from osbot_utils.testing.Temp_Folder import Temp_Folder
from osbot_utils.utils.Files import is_file, is_folder, files_recursive, filter_parent_folder, temp_file
from osbot_utils.utils.Zip import zip_files_to_bytes, zip_bytes__file_list, zip_bytes__add_file, zip_bytes__get_file


class Temp_Zip_In_Memory:

    def __init__(self, targets=None, targets_as_bytes=None):
        self.targets            = targets          or []
        self.targets_as_content = targets_as_bytes or []
        self.root_folder = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def add_file(self, file, root_folder=None):
        if type(file) is Temp_File:
            file = file.path()
        if is_file(file):
            self.add_target(file, root_folder)
        return self

    def add_file_from_content(self, file_path, file_contents):
        self.targets_as_content.append({'file_path': file_path, 'file_contents': file_contents})
        return self

    def add_folder(self, folder, root_folder=None):
        if type(folder) is Temp_Folder:
            folder = folder.path()
        if is_folder(folder):
            self.add_target(folder, root_folder)
        return self

    def add_target(self, target, root_folder=None):
        if target:
            self.targets.append({'target': target, 'root_folder': root_folder})
        return self

    def create_zip_file(self, target_zip_file=None):
        if target_zip_file is None:
            target_zip_file = temp_file(extension='.zip')
        with open(target_zip_file, 'wb') as f:
            f.write(self.zip_bytes())
        return target_zip_file

    def set_root_folder(self, root_folder):
        if type(root_folder) is Temp_Folder:
            self.root_folder = root_folder.path()
        else:
            self.root_folder = root_folder
        return self

    def target_files(self):
        return [entry.get('file') for entry in self.target_files_with_root_folder()]

    def target_files_with_root_folder(self):
        all_files = []
        for entry in self.targets:
            target      = entry.get('target')
            root_folder = entry.get('root_folder') or self.root_folder
            if is_file(target):
                all_files.append({'file': target, 'root_folder': root_folder})
            elif is_folder(target):
                for file in files_recursive(target):
                    all_files.append({'file': file, 'root_folder': root_folder})
        return all_files

    def zip_bytes(self):
        zip_bytes = self.zip_buffer().getvalue()
        for items in self.targets_as_content:
            file_path     = items.get('file_path')
            file_contents = items.get('file_contents')
            zip_bytes = zip_bytes__add_file(zip_bytes, file_path, file_contents)
        return zip_bytes

    def zip_bytes_file_content(self, file_path):
        return zip_bytes__get_file(self.zip_bytes(), file_path)

    def zip_bytes_files(self):
        return zip_bytes__file_list(self.zip_bytes())

    def zip_buffer(self):
        targets = self.target_files_with_root_folder()
        return zip_files_to_bytes(targets, root_folder=self.root_folder)

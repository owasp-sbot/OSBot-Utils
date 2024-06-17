import random

from osbot_utils.utils.Misc import random_string

from osbot_utils.utils.Files import path_combine, temp_folder_current, safe_file_name, folder_exists, folder_create, \
    folder_delete_recursively, files_list, file_create, folder_files, folders_recursive, files_find, files_recursive, \
    temp_file_in_folder, create_folder, filter_parent_folder, file_contents
from osbot_utils.utils.Zip import zip_folder


class Temp_Folder:

    def __init__(self, folder_name=None, parent_folder=None, temp_prefix='', delete_on_exit=True, temp_files_to_add=0):
        if type(parent_folder) is Temp_Folder:
            parent_folder = parent_folder.path()
        self.folder_name         = folder_name or f"temp_folder_{random_string(prefix=temp_prefix)}"
        self.parent_folder       = parent_folder or temp_folder_current()
        self.full_path           = path_combine(self.parent_folder, safe_file_name(self.folder_name))
        self.delete_on_exit      = delete_on_exit
        self.temp_files_to_add   = temp_files_to_add


    def __enter__(self):
        folder_create(self.full_path)
        self.add_temp_files_and_folders(max_total_files=self.temp_files_to_add)
        return self

    def __exit__(self, type, value, traceback):
        if self.delete_on_exit:
            folder_delete_recursively(self.full_path)

    def __repr__(self):
        return f"<Temp_Folder: {self.full_path}>"

    def __str__(self):
        return self.full_path

    def add_temp_files(self, count=0):
        if count is None: count = 1
        for i in range(count):
            self.add_file()

    def add_temp_files_and_folders(self, target_folder=None, max_depth_param=5, max_files_per_folder=4, max_total_files=20, current_depth=0):
        if max_total_files <=0: return max_total_files
        if target_folder is None: target_folder = self.full_path

        # Base case: if max_depth_param is 0 or we've reached max_total_files, we stop
        if max_depth_param == 0 or max_total_files <= 0:
            return max_total_files

        # Randomly decide the number of subfolders and files for this folder
        num_subfolders = random.randint(1, max_depth_param)
        num_files      = random.randint(1, min(max_files_per_folder, max_total_files))
        #print(f'Creating {num_subfolders} subfolders and {num_files} files in {target_folder}')
        # Create the random files
        for _ in range(num_files):
            temp_file_in_folder(target_folder,prefix= f'temp_file__{max_total_files}')
            max_total_files -= 1
            if max_total_files <= 0:
                return max_total_files

        current_depth +=1
        # Recursively create subfolders and their contents
        for _ in range(0, num_subfolders):
            subfolder_name = f"_[{current_depth}]_temp_folder_{str(random.randint(0, 512))}_"
            subfolder_path = path_combine(target_folder, subfolder_name)
            create_folder(subfolder_path)

            # Recursive call with decremented depth and updated max_total_files
            max_total_files = self.add_temp_files_and_folders(subfolder_path, max_depth_param - 1, max_files_per_folder, max_total_files, current_depth=current_depth)

            if max_total_files <= 0:
                break

        return max_total_files

    def add_file(self, file_name=None, contents=None):
        if file_name is None: file_name = f"temp_file_{random_string()}.txt"
        if contents  is None: contents  = random_string()
        file_path = path_combine(self.full_path, safe_file_name(file_name))
        return file_create(file_path, contents)

    def add_folder(self, name=None):
        if name is None: name = f"temp_folder_{random_string()}"
        new_folder = path_combine(self.path(), safe_file_name(name))
        return folder_create(new_folder)


    def exists(self):
        return folder_exists(self.full_path)

    def path(self):
        return self.full_path

    def file_contents(self, target_file):
        file_path = path_combine(self.full_path, target_file)
        return file_contents(file_path)

    def files_contents(self):
        result = {}
        for file_path in self.files():
            full_path         = path_combine(self.full_path, file_path)
            result[file_path] = file_contents(full_path)
        return result

    def files(self, show_parent_folder=False, include_folders=False):
        all_files = files_recursive(self.path(), include_folders=include_folders)
        if show_parent_folder:
            return all_files
        return filter_parent_folder(all_files, self.path())

    def files_and_folders(self, show_parent_folder=False):
        all_files_and_folders = files_recursive(self.path(), include_folders=True)
        if show_parent_folder:
            return all_files_and_folders
        return filter_parent_folder(all_files_and_folders, self.path())

    def folders(self, show_parent_folder=False):
        all_folders = folders_recursive(self.path())
        if show_parent_folder:
            return all_folders
        return filter_parent_folder(all_folders, self.path())

    def zip(self):
        return zip_folder(self.path())
import os
from typing import Union

class Files:
    @staticmethod
    def bytes(path):
        with open(path, 'rb') as file:
            return file.read()

    @staticmethod
    def copy(source:str, destination:str) -> str:
        import shutil
        if file_exists(source):                                     # make sure source file exists
            destination_parent_folder = parent_folder(destination)  # get target parent folder
            folder_create(destination_parent_folder)                # ensure target folder exists       # todo: check if this is still needed (we should be using a copy method that creates the required fodlers)
            return shutil.copy(source, destination)                 # copy file and returns file destination

    @staticmethod
    def contains(path, content):
        text = Files.contents(path)
        if isinstance(content, list):
            for item in content:
                if item not in text:
                    return False
            return True
        return content in text

    @staticmethod
    def contents(path, mode='rt'):
        if file_exists(path):
            with file_open(path, mode) as file:
                return file.read()

    @staticmethod
    def contents_gz(path, mode='rt'):
        if file_exists(path):
            with file_open_gz(path, mode) as file:
                return file.read()

    @staticmethod
    def contents_md5(path):
        from osbot_utils.utils.Misc import bytes_md5
        return bytes_md5(file_contents_as_bytes(path))

    @staticmethod
    def contents_sha256(path):
        from osbot_utils.utils.Misc import bytes_sha256
        return bytes_sha256(file_contents_as_bytes(path))

    @staticmethod
    def current_folder():
        return Files.path_combine(".","")

    @staticmethod
    def delete(path):
        if Files.exists(path):
            os.remove(path)
            return Files.exists(path) is False
        return False

    @staticmethod
    def exists(path):
        return is_file(str(path))
        # if path and is_file(path):
        #     return os.path.exists(path)
        # return False

    @staticmethod
    def find(path_pattern, recursive=True):
        import glob

        return glob.glob(path_pattern, recursive=recursive)

    @staticmethod
    def files(path, pattern= '*', only_files=True):
        from pathlib import Path

        result = []
        for file in Path(path).rglob(pattern):
            if only_files and is_not_file(file):
                continue
            result.append(str(file))                                  # todo: see if there is a better way to do this conversion to string
        return sorted(result)

    @staticmethod
    def files_names(files : list, check_if_exists=True):
        result = []
        for file in files:
            if is_file(file):
                result.append(file_name(file, check_if_exists=check_if_exists))
        return result

    @staticmethod
    def file_create_all_parent_folders(file_path):
        from pathlib import Path

        if file_path:
            parent_path = parent_folder(file_path)
            if parent_path:
                path        = Path(parent_path)
                path.mkdir(parents=True, exist_ok=True)
                return parent_path

    @staticmethod
    def file_name(path, check_if_exists=True):
        if is_file(path) or check_if_exists is False:
            return os.path.basename(path)

    @staticmethod
    def file_name_without_extension(path, check_if_exists=False):
        if path:
            path_file_name = file_name(path,check_if_exists=check_if_exists)
            extension = file_extension(path_file_name)
            if extension:
                return path_file_name.replace(extension, '')


    @staticmethod
    def file_extension(path):
        if path and '.' in path:
            return os.path.splitext(path)[1]
        return ''

    @staticmethod
    def file_extension_fix(extension):
        if extension is None or len(extension) == 0:        # if it None or empty return default .tmp extension
            return '.tmp'
        if extension[0] != '.':                             # make sure that the extension starts with a dot
            return '.' + extension
        return extension

    @staticmethod
    def file_to_base64(path):
        from osbot_utils.utils.Misc import bytes_to_base64

        return bytes_to_base64(file_bytes(path))

    @staticmethod
    def file_from_base64(bytes_base64, path=None, extension=None):
        from osbot_utils.utils.Misc import base64_to_bytes

        bytes_ = base64_to_bytes(bytes_base64)
        return file_create_bytes(bytes=bytes_, path=path, extension=None)

    @staticmethod
    def file_size(path):
        return file_stats(path).st_size

    @staticmethod
    def file_stats(path):
        return os.stat(path)

    @staticmethod
    def filter_parent_folder(items, folder):
        all_relative_items = []
        for item in items:
            all_relative_items.append(item.replace(folder, '')[1:])
        return sorted(all_relative_items)

    @staticmethod
    def files_recursive(parent_dir, include_folders=False):
        all_files = []
        if os.path.isdir(parent_dir):
            for item in os.listdir(parent_dir):
                item_path = os.path.join(parent_dir, item)
                if os.path.isfile(item_path):
                    all_files.append(item_path)
                elif os.path.isdir(item_path):
                    if include_folders:
                        all_files.append(item_path + '/')
                    all_files.extend(files_recursive(item_path,include_folders=include_folders))


        return sorted(all_files)


    @staticmethod
    def folder_exists(path):
        return is_folder(path)

    @staticmethod
    def folder_copy(source, destination, ignore_pattern=None):
        import shutil

        if ignore_pattern:
            if isinstance(ignore_pattern, str):
                ignore_pattern = [ignore_pattern]
            ignore = shutil.ignore_patterns(*ignore_pattern)            # for example ignore_pattern = ['*.pyc','.DS_Store']
        else:
            ignore = None
        return shutil.copytree(src=source, dst=destination, ignore=ignore)

    @staticmethod
    def folder_create(path):
        if folder_exists(path):
            return path

        os.makedirs(path)
        return path

    @staticmethod
    def folder_create_in_parent(path, name):                # todo: revise the naming of this method, since it really doesn't have to do with 'parent' (it will depend on value of name)
        folder_path = path_combine(path, name)
        return folder_create(folder_path)

    @staticmethod
    def folder_delete(target_folder):
        if folder_exists(target_folder):
            try:
                os.rmdir(target_folder)
                return True
            except OSError:
                pass
        return False

    @staticmethod
    def folder_delete_all(path):                # this will remove recursively
        import shutil

        if folder_exists(path):
            shutil.rmtree(path)
            return folder_exists(path) is False
        return False

    @staticmethod
    def folder_name(path):
        if path:
            return os.path.basename(path)

    @staticmethod
    def folder_not_exists(path):
        return folder_exists(path) is False

    @staticmethod
    def folder_sub_folders(path):
        result = []
        item: os.DirEntry
        if Files.is_folder(path):
            for item in os.scandir(path):
                if item.is_dir():
                    result.append(item.path)
        return result

    @staticmethod
    def folders_names(folders : list):
        result = []
        for folder in folders:
            if folder:
                result.append(folder_name(folder))
        return sorted(result)

    @staticmethod
    def folders_sub_folders(folders : list):
        result = []
        for folder in folders:
            result.extend(Files.folder_sub_folders(folder))
        return result

    @staticmethod
    def folders_recursive(parent_dir):
        subdirectories = []
        for item in os.listdir(parent_dir):
            item_path = os.path.join(parent_dir, item)
            if os.path.isdir(item_path):
                subdirectories.append(item_path)
                subdirectories.extend(folders_recursive(item_path))

        return sorted(subdirectories)


    @staticmethod
    def is_file(target):
        from pathlib import Path

        if isinstance(target, Path):
            return target.is_file()
        if isinstance(target, str):
            if len(target) < 4096:                          # max file size in Linux (handle the cases when the file contents was used as target)
                return os.path.isfile(target)
        return False

    @staticmethod
    def is_folder(target):
        from pathlib import Path

        if isinstance(target, Path):
            return target.is_dir()
        if isinstance(target, str):
            return os.path.isdir(target)
        return False

    @staticmethod
    def lines(path):
        with open(path, "rt") as file:
            for line in file:
                yield line

    @staticmethod
    def lines_gz(path):
        import gzip

        with gzip.open(path, "rt") as file:
            for line in file:
                yield line

    @staticmethod
    def not_exists(path):
        return os.path.exists(str(path)) is False

    @staticmethod
    def open(path, mode='r'):
        return open(path, mode=mode)

    @staticmethod
    def open_gz(path, mode='r'):
        import gzip

        return gzip.open(path, mode=mode)

    @staticmethod
    def open_bytes(path):
        return Files.open(path, mode='rb')

    @staticmethod
    # def path_combine(path1, path2):
    #     if type(path1) in [str, Path] and type(path2) in [str, Path]:
    #         parent_path = str(path1)
    #         sub_path    = str(path2)
    #         if sub_path.startswith('/'):
    #             sub_path = sub_path[1:]
    #         return abspath(join(parent_path,sub_path))

    def path_combine(path1: Union[str, os.PathLike], path2: Union[str, os.PathLike]) -> str:
        from os.path import abspath, join

        if path1 is None or path2 is None:
            raise ValueError("Both paths must be provided")

        parent_path = str(path1)
        sub_path = str(path2)

        sub_path = sub_path.lstrip('/')     # Remove leading slashes from sub_path

        return abspath(join(parent_path, sub_path))

    @staticmethod
    def parent_folder(path, use_full_path=False):
        if path:
            if use_full_path:
                path = file_full_path(path)
            return os.path.dirname(path)

    @staticmethod
    def parent_folder_combine(file, path):
        return Files.path_combine(os.path.dirname(file),path)



    @staticmethod
    def pickle_save_to_file(object_to_save, path=None):
        import pickle

        path = path or temp_file(extension=".pickle")
        file_to_store = open(path, "wb")
        pickle.dump(object_to_save, file_to_store)
        file_to_store.close()
        return path

    @staticmethod
    def pickle_load_from_file(path=None):
        import pickle

        file_to_read = open(path, "rb")
        loaded_object = pickle.load(file_to_read)
        file_to_read.close()
        return loaded_object

    @staticmethod
    def safe_file_name(file_name):
        import re

        if type(file_name) is not str:
            file_name = f"{file_name}"
        return re.sub(r'[^a-zA-Z0-9_.-]', '_',file_name or '')

    @staticmethod
    def save(contents, path=None, extension=None):
        path = path or temp_file(extension=extension)
        file_create(path, contents)
        return path

    @staticmethod
    def sub_folders(target):
        if isinstance(target, list):
            return Files.folders_sub_folders(target)
        if isinstance(target, str):
            return Files.folder_sub_folders(target)
        return []

    @staticmethod
    def save_bytes_as_file(bytes_to_save, path=None, extension=None):
        if path is None:
            path = Files.temp_file(extension)
        with open(path, 'wb') as fp:
            fp.write(bytes_to_save)
        return path

    @staticmethod
    def temp_file(extension = '.tmp', contents=None, target_folder=None):
        import tempfile

        extension = file_extension_fix(extension)
        if target_folder is None:
            (fd, tmp_file) = tempfile.mkstemp(extension)
            file_delete(tmp_file)
        else:
            tmp_file = path_combine(target_folder, temp_filename(extension))

        if contents:
            file_create(tmp_file, contents)
        return tmp_file

    @staticmethod
    def temp_file_in_folder(target_folder, prefix="temp_file_", postfix='.txt'):
        from osbot_utils.utils.Misc import random_string

        if is_folder(target_folder):
            path_to_file = path_combine(target_folder, random_string(prefix=prefix, postfix=postfix))
            file_create(path_to_file, random_string())
            return path_to_file

        

    @staticmethod
    def temp_filename(extension='.tmp'):
        return file_name(temp_file(extension), check_if_exists=False)

    @staticmethod
    def temp_folder(prefix=None, suffix=None,target_folder=None):
        import tempfile

        return tempfile.mkdtemp(suffix, prefix, target_folder)

    @staticmethod
    def temp_folder_current():
        import tempfile

        return tempfile.gettempdir()

    @staticmethod
    def temp_folder_with_temp_file(prefix=None, suffix=None,parent_folder=None, file_name='temp_file.txt', file_contents='temp_file'):
        folder = temp_folder(prefix,suffix,parent_folder)
        file_create(path_combine(folder,file_name), file_contents)
        return folder

    @staticmethod
    def write(path = None,contents=None, extension=None, mode='w'):
        path     = path or temp_file(extension)
        contents = contents or ''
        with open(file=path, mode=mode) as file:
            file.write(contents)
        return path

    @staticmethod
    def write_bytes(path=None, bytes=None, extension=None):
        return Files.write(path=path, contents=bytes, extension=extension, mode='wb')

    @staticmethod
    def write_gz(path=None, contents=None):
        import gzip

        path = path or temp_file(extension='.gz')
        contents = contents or ''
        if isinstance(contents, str):
            contents = contents.encode()
        with gzip.open(path, "w") as file:
            file.write(contents)
        return path

# todo: refactor the methods above into static methods (as bellow)
def absolute_path(path):
    from os.path import abspath

    return abspath(path)

def all_parent_folders(path=None, include_path=False):
    if path is None:
        path = os.getcwd()
    parent_directories = []

    # Optionally include the starting path
    if include_path:
        parent_directories.append(path)

    while True:                                         # Split the path into parts
        path, tail = os.path.split(path)
        if tail:
            parent_directories.append(path)
        else:
            if path and path not in parent_directories:  # to handle the root path case
                parent_directories.append(path)
            break
    return parent_directories

def is_not_file(target):
    return is_file(target) is False

def file_move(source_file, target_file):
    if file_exists(source_file):
        file_copy(source_file, target_file)
        if file_exists(target_file):
            if file_delete(source_file):
                return True
    return False

def file_move_to_folder(source_file, target_folder):
    if file_exists(source_file):
        if folder_exists(target_folder):
            target_file = path_combine(target_folder, file_name(source_file))
            if file_move(source_file, target_file):
                return target_file

def files_names_without_extension(files, check_if_exists=False):
    return [file_name_without_extension(file, check_if_exists) for file in files]

def files_names_in_folder(target, with_extension=False):
    if with_extension:
        return files_names(files_in_folder(target))
    else:
        return files_names_without_extension(files_in_folder(target))

def files_in_folder(path,pattern='*', only_files=True):
    from pathlib import Path

    result = []
    for file in Path(path).glob(pattern):
        if only_files and is_not_file(file):
            continue
        result.append(str(file))                                  # todo: see if there is a better way to do this conversion to string
    return sorted(result)

def folders_names_in_folder(target):
    folders = folders_in_folder(target)
    return folders_names(folders)

def path_combine_safe(base_path, file_location, raise_exception=False):                                  # handle possible directory transversal attacks
    full_path            = os.path.join(base_path, file_location)                                       # Combine and normalize paths
    normalised_base_path = os.path.normpath(base_path)
    normalised_full_path = os.path.normpath(full_path)

    if os.path.commonpath([normalised_base_path, normalised_full_path]) == normalised_base_path:        # Check for directory traversal
        return normalised_full_path
    if raise_exception:
        raise ValueError("Invalid file location: directory traversal attempt detected.")
    return None

def parent_folder_create(target):
    return folder_create(parent_folder(target))

def parent_folder_exists(target):
    return folder_exists(parent_folder(target))

def parent_folder_name(target):
    return folder_name(parent_folder(target))

def parent_folder_not_exists(target):
    return parent_folder_exists(target) is False

def stream_to_bytes(stream):
    return stream.read()

def stream_to_file(stream, path=None):
    if path is None:                        # if path is not defined
        path = Files.temp_file()            # save it to a temp file
    with open(path, 'wb') as file:          # Write the content to the file
        file.write(stream.read())
    return path

# helper methods
# todo: all all methods above (including the duplicated mappings at the top)

bytes_to_file                  = Files.write_bytes
create_folder                  = Files.folder_create
create_folder_in_parent        = Files.folder_create_in_parent
create_temp_file               = Files.write
current_folder                 = Files.current_folder
current_temp_folder            = Files.temp_folder_current

file_bytes                     = Files.bytes
file_contains                  = Files.contains
file_contents                  = Files.contents
file_contents_gz               = Files.contents_gz
file_contents_md5              = Files.contents_md5
file_contents_sha256           = Files.contents_sha256
file_contents_as_bytes         = Files.bytes
file_create_all_parent_folders = Files.file_create_all_parent_folders
file_copy                      = Files.copy
file_delete                    = Files.delete
file_create                    = Files.write
file_create_bytes              = Files.write_bytes
file_create_from_bytes         = Files.write_bytes
file_create_gz                 = Files.write_gz
file_exists                    = Files.exists
file_extension                 = Files.file_extension
file_extension_fix             = Files.file_extension_fix
file_full_path                 = absolute_path
file_lines                     = Files.lines
file_lines_gz                  = Files.lines_gz
file_md5                       = Files.contents_md5
file_move_to                   = file_move
file_name                      = Files.file_name
file_name_without_extension    = Files.file_name_without_extension
file_not_exists                = Files.not_exists
file_open                      = Files.open
file_open_gz                   = Files.open_gz
file_open_bytes                = Files.open_bytes
file_to_base64                 = Files.file_to_base64
file_from_base64               = Files.file_from_base64
file_from_bytes                = Files.write_bytes
file_save                      = Files.save
file_sha256                    = Files.contents_sha256
file_size                      = Files.file_size
file_stats                     = Files.file_stats
file_write                     = Files.write
file_write_bytes               = Files.write_bytes
file_write_gz                  = Files.write_gz
filter_parent_folder           = Files.filter_parent_folder
files_find                     = Files.find
files_recursive                = Files.files_recursive
files_list                     = Files.files
files_names                    = Files.files_names

find_files                     = Files.files

folder_create                  = Files.folder_create
folder_create_in_parent        = Files.folder_create_in_parent
folder_create_temp             = Files.temp_folder
folder_copy                    = Files.folder_copy
folder_copy_except             = Files.folder_copy
folder_delete                  = Files.folder_delete
folder_delete_all              = Files.folder_delete_all
folder_delete_recursively      = Files.folder_delete_all
folder_exists                  = Files.folder_exists
folder_not_exists              = Files.folder_not_exists
folder_name                    = Files.folder_name
folder_temp                    = Files.temp_folder
folder_files                   = Files.files
folder_sub_folders             = Files.folder_sub_folders

folders_in_folder              = Files.folder_sub_folders
folders_names                  = Files.folders_names
folders_recursive              = Files.folders_recursive
folders_sub_folders            = Files.folders_sub_folders

is_file                     = Files.is_file
is_folder                   = Files.is_folder

load_file                   = Files.contents
load_file_gz                = Files.contents_gz

path_append                 = Files.path_combine
path_combine                = Files.path_combine
path_current                = Files.current_folder
parent_folder               = Files.parent_folder
parent_folder_combine       = Files.parent_folder_combine
pickle_load_from_file       = Files.pickle_load_from_file
pickle_save_to_file         = Files.pickle_save_to_file

safe_file_name              = Files.safe_file_name
save_bytes_as_file          = Files.save_bytes_as_file
save_string_as_file         = Files.save
sub_folders                 = Files.sub_folders

temp_file                   = Files.temp_file
temp_file_in_folder         = Files.temp_file_in_folder
temp_filename               = Files.temp_filename
temp_folder                 = Files.temp_folder
temp_folder_current         = Files.temp_folder_current
temp_folder_with_temp_file  = Files.temp_folder_with_temp_file


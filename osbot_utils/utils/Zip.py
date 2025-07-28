import gzip
import io
import os
import shutil
import tarfile
import zipfile
from os.path                 import abspath
from osbot_utils.utils.Misc  import list_set
from osbot_utils.utils.Files import temp_folder, folder_files, temp_file, is_file, file_copy, file_move, file_exists, \
    file_contents_as_bytes

#########################
# actions on gz_tar_bytes

def gz_tar_bytes__file_list(gz_bytes):
    gz_buffer_from_bytes = io.BytesIO(gz_bytes)
    with gzip.GzipFile(fileobj=gz_buffer_from_bytes, mode='rb') as gz:
        decompressed_data = gz.read()
        tar_buffer_from_bytes = io.BytesIO(decompressed_data)                       # Assuming the decompressed data is a tag file, process it
        with tarfile.open(fileobj=tar_buffer_from_bytes, mode='r:') as tar:
            return sorted(tar.getnames())

def gz_tar_bytes__get_file(gz_bytes, tar_file_path):
    gz_buffer_from_bytes = io.BytesIO(gz_bytes)
    with gzip.GzipFile(fileobj=gz_buffer_from_bytes, mode='rb') as gz:
        decompressed_data = gz.read()
        tar_buffer_from_bytes = io.BytesIO(decompressed_data)
        with tarfile.open(fileobj=tar_buffer_from_bytes, mode='r:') as tar:
            extracted_file = tar.extractfile(tar_file_path)
            if extracted_file:
                return extracted_file.read()
            else:
                raise FileNotFoundError(f"The file {tar_file_path} was not found in the tar archive.")

#########################
# actions on gz_zip_bytes

def gz_zip_bytes__file_list(gz_bytes):
    gz_buffer_from_bytes = io.BytesIO(gz_bytes)
    with gzip.GzipFile(fileobj=gz_buffer_from_bytes, mode='rb') as gz:
        decompressed_data = gz.read()
        zip_buffer_from_bytes = io.BytesIO(decompressed_data)                   # Assuming the decompressed data is a zip file, process it
        with zipfile.ZipFile(zip_buffer_from_bytes, 'r') as zf:
            return sorted(zf.namelist())

#########################
# actions on zipped bytes

def zip_bytes__add_file(zip_bytes, zip_file_path, file_contents):                                       # todo: see if this is actually a valid use case (or if we should be using replace in all scenarios)
    return zip_bytes__add_files(zip_bytes, {zip_file_path: file_contents})

def zip_bytes__add_file__from_disk(zip_bytes, base_path, file_to_add):
    return zip_bytes__add_files__from_disk(zip_bytes, base_path, files_to_add=[file_to_add])

def zip_bytes__add_files__from_disk(zip_bytes, base_path, files_to_add, replace_files=True, path_prefix=None):
    zip_files_to_add = {}
    if base_path[:-1] != '/':
        base_path += "/"

    for file_to_add in files_to_add:
        if file_exists(file_to_add):
            file_contents = file_contents_as_bytes(file_to_add)
            zip_file_path = file_to_add.replace(base_path, '')
            if path_prefix:
                zip_file_path = path_prefix + zip_file_path
            zip_files_to_add[zip_file_path] = file_contents

    if replace_files:
        return zip_bytes__replace_files(zip_bytes, zip_files_to_add)
    else:
        return zip_bytes__add_files(zip_bytes, zip_files_to_add)                        # todo: see if this is actually a valid use case (or if we should be using replace in all scenarios)

def zip_bytes__add_files(zip_bytes, files_to_add):                                      # todo: see if this is actually a valid use case (or if we should be using replace in all scenarios)
    zip_buffer = io.BytesIO(zip_bytes)                                                  # Create a BytesIO buffer from the input zip bytes

    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zf:
        for file_path, file_contents in files_to_add.items():
            if isinstance(file_contents, str):
                file_contents = file_contents.encode('utf-8')
            elif not isinstance(file_contents, bytes):
                continue
            if file_path.startswith(('/', '\\')):                                       # Strip leading slash or backslash to make the path relative
                file_path = file_path.lstrip('/\\')
            zf.writestr(file_path, file_contents)

    return zip_buffer.getvalue()

def zip_bytes__file(zip_bytes, zip_file_path):
    zip_buffer = io.BytesIO(zip_bytes)
    with zipfile.ZipFile(zip_buffer, 'r') as zf:
        if zip_file_path in zf.namelist():
            return zf.read(zip_file_path)

def zip_bytes__files(zip_bytes):
    zip_buffer = io.BytesIO(zip_bytes)                      # Create a BytesIO buffer from the input zip bytes
    files_dict = {}                                         # Create a dictionary to store file contents

    with zipfile.ZipFile(zip_buffer, 'r') as zf:      # Open the zip file in read mode
        for file_name in zf.namelist():                     # Iterate over each file in the zip archive
            files_dict[file_name] = zf.read(file_name)      # Read the content of the file

    return files_dict                                       # Return the dictionary with file contents

def zip_bytes__files_paths(zip_bytes):
    return list_set(zip_bytes__files(zip_bytes))

def zip_bytes__file_list(zip_bytes):
    zip_buffer_from_bytes = io.BytesIO(zip_bytes)
    with zipfile.ZipFile(zip_buffer_from_bytes, 'r') as zf:
        return sorted(zf.namelist())

def zip_bytes__remove_file(zip_bytes, file_to_remove):
    return zip_bytes__remove_files(zip_bytes, [file_to_remove])

def zip_bytes__remove_files(zip_bytes, files_to_remove):
    files_to_remove = set(files_to_remove)                                      # Convert files_to_remove to a set for faster lookup
    zip_buffer      = io.BytesIO(zip_bytes)                                     # Create a BytesIO buffer from the input zip bytes
    new_zip_buffer  = io.BytesIO()                                              # Create a new BytesIO buffer for the updated zip

    with zipfile.ZipFile(zip_buffer, 'r') as original_zip:
        with zipfile.ZipFile(new_zip_buffer, 'w') as new_zip:
            for item in original_zip.infolist():                                # Iterate over each item in the original zip file
                if item.filename not in files_to_remove:                        # Read the original content and write it to the new zip file
                    new_zip.writestr(item, original_zip.read(item.filename))
    return new_zip_buffer.getvalue()                                            # Get the updated zip content as bytes

def zip_bytes__replace_file(zip_bytes, zip_file_path, file_contents):
    files_to_replace = {zip_file_path: file_contents }
    return zip_bytes__replace_files(zip_bytes, files_to_replace)

def zip_bytes__replace_files(zip_bytes, files_to_replace):
    zip_bytes__without_files       = zip_bytes__remove_files(zip_bytes               , set(files_to_replace))
    zip_bytes__with_replaced_files = zip_bytes__add_files   (zip_bytes__without_files, files_to_replace     )
    return zip_bytes__with_replaced_files


def zip_bytes__unzip(zip_bytes, target_folder=None):
    target_folder = target_folder or temp_folder()              # Use the provided target folder or create a temporary one
    zip_buffer = io.BytesIO(zip_bytes)                          # Create a BytesIO buffer from the zip bytes
    with zipfile.ZipFile(zip_buffer, 'r') as zf:                # Open the zip file from the buffer
        zf.extractall(target_folder)                            # Extract all files to the target folder
    return target_folder                                        # Return the path of the target folder


########################
# actions on zipped file

def zip_file__list(path_zip_file):
    if is_file(path_zip_file):
        with zipfile.ZipFile(path_zip_file) as zip_file:
            return sorted(zip_file.namelist())
    return []

def zip_file__files(path_zip_file):
    if is_file(path_zip_file):
        zip_bytes = file_contents_as_bytes(path_zip_file)
        return zip_bytes__files(zip_bytes)
    return []

def zip_file__unzip(path_zip_file, target_folder=None, format='zip'):
    target_folder = target_folder or temp_folder()
    shutil.unpack_archive(path_zip_file, extract_dir=target_folder, format=format)
    return target_folder

# zip creation actions
def zip_bytes_empty():

    zip_buffer = io.BytesIO()                                               # Create a BytesIO buffer to hold the zip file
    with zipfile.ZipFile(zip_buffer, mode='w') as _:                        # Use the zipfile.ZipFile class to create an empty zip file
        pass                                                                # No files to add, so we just create the zip structure
    return zip_buffer.getvalue()                                            # Get the zip file content as bytes

def zip_bytes_to_file(zip_bytes, target_file=None):
    if target_file is None:
        target_file = temp_file(extension='.zip')
    with open(target_file, 'wb') as f:
        f.write(zip_bytes)
    return target_file

def zip_files_to_bytes(target_files, root_folder=None):
    zip_buffer = io.BytesIO()                                                   # Create a BytesIO buffer to hold the zipped file
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:          # Create a ZipFile object with the buffer as the target
        for entry in target_files:
            if type(entry) is str:                                              # if entry is a string, assume it's a file path
                file_path = entry
                file_root_folder = root_folder
            else:
                file_path = entry.get('file')
                file_root_folder = entry.get('root_folder') or root_folder
            if file_root_folder:
                arcname = file_path.replace(file_root_folder,'')                      # Define the arcname, which is the name inside the zip file
            else:
                arcname = file_path                                                 # if root_path is not provided, use the full file path
            zf.write(file_path, arcname)                                            # Add the file to the zip file
    zip_buffer.seek(0)
    return zip_buffer

def zip_folder(root_dir, format='zip'):
    return shutil.make_archive(base_name=root_dir, format=format, root_dir=root_dir)

def zip_folder_to_file (root_dir, target_file):
    zip_file = zip_folder(root_dir)
    return file_move(zip_file, target_file)

def zip_folder_to_bytes(root_dir, files_to_ignore:list=None):      # todo add unit test
    zip_buffer = io.BytesIO()                                                   # Create a BytesIO buffer to hold the zipped file
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:          # Create a ZipFile object with the buffer as the target
        for foldername, subfolders, filenames in os.walk(root_dir):             # Walk the root_dir and add all files and folders to the zip file
            for filename in filenames:
                if files_to_ignore and filename in files_to_ignore:
                    continue
                absolute_path = os.path.join(foldername, filename)              # Create the complete filepath
                arcname = os.path.relpath(absolute_path, root_dir)              # Define the arcname, which is the name inside the zip file
                zf.write(absolute_path, arcname)                                # Add the file to the zip file
    zip_buffer.seek(0)                                                          # Reset buffer position
    return zip_buffer.getvalue()

def zip_files(base_folder, file_pattern="*.*", target_file=None):
    base_folder = abspath(base_folder)
    file_list   = folder_files(base_folder, file_pattern)

    if len(file_list):                                                  # if there were files found
        target_file = target_file or temp_file(extension='zip')
        with zipfile.ZipFile(target_file,'w') as zip:
            for file_name in file_list:
                zip_file_path = file_name.replace(base_folder,'')
                zip.write(file_name, zip_file_path)

        return target_file

# actions on strings

def bytes_to_gz(input_bytes):
    buf = io.BytesIO()                                          # Create an in-memory bytes buffer
    with gzip.GzipFile(fileobj=buf, mode='wb') as gz_file:      # Create a gzip file object that writes to the buffer
        gz_file.write(input_bytes)                              # Write the input bytes to the gzip file object
    return buf.getvalue()                                       # Get the compressed data from the buffer

def str_to_gz(value):
    buf = io.BytesIO()                                          # Create an in-memory bytes buffer
    with gzip.GzipFile(fileobj=buf, mode='wb') as gz_file:      # Create a gzip file object that writes to the buffer
        gz_file.write(value.encode('utf-8'))                    # Write the input string to the gzip file object
    return buf.getvalue()                                       # Get the compressed data from the buffer

def gz_to_bytes(gz_data):
    buf = io.BytesIO(gz_data)                                   # Create an in-memory bytes buffer with the gzip data
    with gzip.GzipFile(fileobj=buf, mode='rb') as gz_file:      # Create a gzip file object that reads from the buffer
        return gz_file.read()                                   # Read the decompressed data as bytes

def gz_to_str(gz_data):
    buf = io.BytesIO(gz_data)                                   # Create an in-memory bytes buffer with the gzip data
    with gzip.GzipFile(fileobj=buf, mode='rb') as gz_file:      # Create a gzip file object that reads from the buffer
        return gz_file.read().decode('utf-8')                   # Read the decompressed data and decode it to a string

###########################
# extra function's mappings

file_unzip                   = zip_file__unzip
folder_zip                   = zip_folder

unzip_file                   = zip_file__unzip

zip_bytes__extract_to_folder = zip_bytes__unzip
zip_bytes__file_contents     = zip_bytes__file
zip_bytes__get_file          = zip_bytes__file
zip_bytes__unzip_to_folder   = zip_bytes__unzip

zip_list_files               = zip_file__list
zip_file__file_list          = zip_file__list
zip_file__files_list         = zip_file__list
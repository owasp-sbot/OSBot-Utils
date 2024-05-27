import gzip
import io
import os
import shutil
import tarfile
import zipfile
from os.path import abspath

from osbot_utils.utils.Files import temp_folder, folder_files, temp_file, is_file, file_copy, file_move


def gz_tar_bytes_file_list(gz_bytes):
    gz_buffer_from_bytes = io.BytesIO(gz_bytes)
    with gzip.GzipFile(fileobj=gz_buffer_from_bytes, mode='rb') as gz:
        decompressed_data = gz.read()
        tar_buffer_from_bytes = io.BytesIO(decompressed_data)                       # Assuming the decompressed data is a tag file, process it
        with tarfile.open(fileobj=tar_buffer_from_bytes, mode='r:') as tar:
            return sorted(tar.getnames())

def gz_tar_bytes_get_file(gz_bytes, tar_file_path):
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

def gz_zip_bytes_file_list(gz_bytes):
    gz_buffer_from_bytes = io.BytesIO(gz_bytes)
    with gzip.GzipFile(fileobj=gz_buffer_from_bytes, mode='rb') as gz:
        decompressed_data = gz.read()
        zip_buffer_from_bytes = io.BytesIO(decompressed_data)                   # Assuming the decompressed data is a zip file, process it
        with zipfile.ZipFile(zip_buffer_from_bytes, 'r') as zf:
            return sorted(zf.namelist())

def unzip_file(zip_file, target_folder=None, format='zip'):
    target_folder = target_folder or temp_folder()
    shutil.unpack_archive(zip_file, extract_dir=target_folder, format=format)
    return target_folder

def zip_bytes_add_file(zip_bytes, zip_file_path, file_contents):
    if type(file_contents) is str:
        file_contents = file_contents.encode('utf-8')
    elif type(file_contents) is not bytes:
        return None
    zip_buffer = io.BytesIO(zip_bytes)
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(zip_file_path, file_contents)

    return zip_buffer.getvalue()

def zip_bytes_get_file(zip_bytes, zip_file_path):
    zip_buffer = io.BytesIO(zip_bytes)
    with zipfile.ZipFile(zip_buffer, 'r') as zf:
        return zf.read(zip_file_path)

def zip_bytes_extract_to_folder(zip_bytes, target_folder=None):
    target_folder = target_folder or temp_folder()              # Use the provided target folder or create a temporary one
    zip_buffer = io.BytesIO(zip_bytes)                          # Create a BytesIO buffer from the zip bytes
    with zipfile.ZipFile(zip_buffer, 'r') as zf:          # Open the zip file from the buffer
        zf.extractall(target_folder)                            # Extract all files to the target folder
    return target_folder                                        # Return the path of the target folder


def zip_bytes_file_list(zip_bytes):
    zip_buffer_from_bytes = io.BytesIO(zip_bytes)
    with zipfile.ZipFile(zip_buffer_from_bytes, 'r') as zf:
        return sorted(zf.namelist())

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


def zip_folder_to_bytes(root_dir):      # todo add unit test
    zip_buffer = io.BytesIO()                                                   # Create a BytesIO buffer to hold the zipped file
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:          # Create a ZipFile object with the buffer as the target
        for foldername, subfolders, filenames in os.walk(root_dir):             # Walk the root_dir and add all files and folders to the zip file
            for filename in filenames:
                absolute_path = os.path.join(foldername, filename)              # Create the complete filepath
                arcname = os.path.relpath(absolute_path, root_dir)              # Define the arcname, which is the name inside the zip file
                zf.write(absolute_path, arcname)                                # Add the file to the zip file
    zip_buffer.seek(0)                                                          # Reset buffer position
    return zip_buffer

def zip_file_list(path):
    if is_file(path):
        with zipfile.ZipFile(path) as zip_file:
            return sorted(zip_file.namelist())
    return []

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


# extra function's mappings
file_unzip  = unzip_file
folder_zip  = zip_folder
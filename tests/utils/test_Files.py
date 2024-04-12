from unittest                import TestCase

from osbot_utils.testing.Temp_File import Temp_File
from osbot_utils.testing.Temp_Folder import Temp_Folder
from osbot_utils.utils.Files import Files, path_combine, parent_folder, path_current, save_bytes_as_file, file_bytes, \
    temp_file, file_create, file_delete, file_exists, file_contents, file_copy, file_contents_as_bytes, file_name, \
    folder_name, folder_files, file_not_exists, temp_folder, folder_copy, path_append, folder_exists, folder_create, \
    folder_delete_all, folder_not_exists, file_extension, \
    save_string_as_file, file_write_gz, file_contents_gz, file_size, file_write, \
    file_lines, file_create_gz, file_lines_gz, parent_folder_combine, file_write_bytes, file_open_bytes, \
    file_contents_md5, \
    file_contents_sha256, create_folder_in_parent, sub_folders, safe_file_name, files_find, is_file, is_folder, \
    temp_filename, current_folder, folder_delete
from osbot_utils.utils.Misc   import random_bytes, random_string, remove, bytes_md5, str_to_bytes, bytes_sha256
from osbot_utils.utils.Zip import zip_files, zip_file_list, unzip_file


class test_Files(TestCase):

    def test_file_bytes(self):
        bytes     = random_bytes()
        temp_file = save_bytes_as_file(bytes)
        assert file_bytes            (temp_file) == bytes
        assert file_contents_as_bytes(temp_file) == bytes

    def test_contents_gz(self):
        size      = 1024
        temp_text = random_string(size)

        file    = file_write    (contents=temp_text)
        gz_file = file_write_gz (contents=temp_text)

        assert file_contents_gz (gz_file) == temp_text
        assert file_size        (file   ) == size
        assert file_size        (gz_file) < size

    def test_file_copy(self):
        text_a = random_string()
        text_b = random_string()
        file_a = temp_file   (contents=text_a)
        file_b = temp_file   (contents=text_b)
        assert file_exists   (file_a) is True
        assert file_exists   (file_b) is True
        assert file_contents (file_a) == text_a
        assert file_contents (file_b) == text_b
        assert file_delete   (file_b) is True
        assert file_exists   (file_b) is False

        file_copy(file_a, file_b)

        assert file_exists   (file_b) is True
        assert file_contents (file_b) == text_a

    def test_file_create(self):
        target    = temp_file()
        text      = random_string()

        assert file_delete(target) is False
        assert file_exists(target) is False
        assert file_create(target, text) == target

        assert file_exists(target) is True
        assert file_contents(target) == text

        empty_file = file_create()

        assert file_exists(empty_file) is True
        assert file_contents(empty_file) == ''

    def test_file_extension(self):
        assert Files.file_extension('/path/to/somefile.ext') == '.ext'
        assert Files.file_extension('/path/to/somefile.'   ) == '.'
        assert Files.file_extension('/path/to/somefile..'  ) == '.'
        assert Files.file_extension('/path/to/somefile'    ) == ''
        assert Files.file_extension('/a/b.c/d'             ) == ''
        assert Files.file_extension('/a/b.c/.git'          ) == ''
        assert Files.file_extension('/a/b.c/a.git'         ) == '.git'
        assert Files.file_extension('/a/b.c/a.git.abc'     ) == '.abc'
        assert Files.file_extension(None)                    == ''

    def test_exists(self):
        assert file_exists(random_string()) == False
        assert file_exists({}             ) == False
        assert file_exists(None           ) == False
        with Temp_File() as _:
            assert file_exists  (_.path()) is True
            assert is_file      (_.path()) is True
            assert folder_exists(_.path()) is False
            assert is_folder    (_.path()) is False

    def test_file_lines(self):
        contents = """1st line
        2nd line
        3rd line        
        """
        file_path = file_create(contents=contents)
        lines = list(file_lines(file_path))
        assert len(lines) == 4
        assert lines[0].strip() == '1st line'
        assert lines[1].strip() == '2nd line'
        assert lines[2].strip() == '3rd line'
        assert lines[3].strip() == ''

        file_path_gz = file_create_gz(contents=contents)
        lines_gz = list(file_lines_gz(file_path_gz))
        assert lines == lines_gz


    def test_file_name(self):
        target = temp_file()
        assert path_combine(parent_folder(target) , file_name(target,check_if_exists=False)) == target
        assert file_not_exists(target)

    def test_file_not_exists(self):
        target = temp_file()
        assert file_not_exists(target) is True
        file_create(target,'asd')
        assert file_not_exists(target) is False

    def test_file_write(self):
        target = temp_file()
        text   = "this is a string"
        assert file_contents(file_write(target, text)) == text
        assert file_bytes   (file_write(target, text)) == text.encode()

        assert file_contents(file_write(target, text.encode(), mode='wb')) == text
        assert file_bytes   (file_write(target, b"\x89PNG___", mode='wb')) == b"\x89PNG___"

    def test_file_write_bytes(self):
        target = temp_file()
        bytes  = b"\x89PNG___"
        assert file_bytes(file_write_bytes(target, bytes=bytes)) == bytes
        assert file_open_bytes(target).read() == b'\x89PNG___'


    def test_folder_copy(self):
        folder_a = temp_folder(prefix='folder_a_')
        folder_b = temp_folder(prefix='folder_b_', target_folder=folder_a)
        folder_c = temp_folder(prefix='folder_c_', target_folder=folder_a)
        file_a   = temp_file  (contents='abc'    , target_folder=folder_a)
        file_b   = temp_file  (contents='abc'    , target_folder=folder_b)
        file_c   = temp_file  (contents='abc'    , target_folder=folder_c)

        target_a = path_combine(folder_a, 'target_a')

        assert parent_folder(target_a) == folder_a
        assert parent_folder_combine(target_a, 'target_a') == target_a

        assert folder_copy(source=folder_a, destination=target_a) == target_a
        assert(len(folder_files(target_a)) == 3)

        assert folder_files(target_a) == sorted([ path_append(target_a, remove(file_a, folder_a +'/')) ,
                                                  path_append(target_a, remove(file_b, folder_a + '/')),
                                                  path_append(target_a, remove(file_c, folder_a + '/'))])

        # test with ignore_pattern
        target_b = path_combine(folder_a, 'target_b')
        assert folder_copy(source=target_a, destination=target_b, ignore_pattern='folder_b_*') == target_b
        assert(len(folder_files(target_b)) == 2)

        zipped_files = zip_files(target_a)
        assert zip_file_list(zipped_files) == sorted([remove(file_a, folder_a + '/'),
                                                      remove(file_b, folder_a + '/'),
                                                      remove(file_c, folder_a + '/')])

        path_pattern = f'{folder_a}/**/*.*'
        assert len(files_find(path_pattern)) == 8

    def test_folder_create(self):
        tmp_folder = '_tmp_folder'
        assert folder_exists(tmp_folder) is False
        assert folder_create(tmp_folder) == tmp_folder
        assert folder_create(tmp_folder) == tmp_folder
        assert folder_exists(tmp_folder) is True
        assert folder_not_exists(tmp_folder) is False
        assert folder_delete_all(tmp_folder) is True
        assert folder_not_exists(tmp_folder) is True

    def test_folder_files(self):
        folder = parent_folder(__file__)
        assert path_combine(folder, 'test_Files.py') in folder_files(folder)
        assert path_combine(folder, 'test_Json.py' ) in folder_files(folder)


    def test_path_combine(self):
        assert path_combine('a', 'b') == f"{path_current()}/a/b"       # todo: add more use cases


    def test_pickle_save_to_file__pickle_load_from_file(self):
        an_object = {"answer" : 42 }
        pickled_file = Files.pickle_save_to_file(an_object)
        pickle_data = Files.pickle_load_from_file(pickled_file)
        assert pickle_data == an_object

    def test_safe_file_name(self):
        assert safe_file_name('aaaabbb') == 'aaaabbb'
        assert safe_file_name('aaa_bbb') == 'aaa_bbb'
        assert safe_file_name('aaa.bbb') == 'aaa.bbb'
        assert safe_file_name('AAA.bbb') == 'AAA.bbb'
        assert safe_file_name('Abb.123') == 'Abb.123'
        assert safe_file_name('aaa bbb') == 'aaa_bbb'
        assert safe_file_name('a!@£$b' ) == 'a____b'
        assert safe_file_name('aaa/../') == 'aaa_.._'
        assert safe_file_name('a\n\t\r') == 'a___'


    def test_save_string_as_file(self):
        data      = random_string()
        temp_file = save_string_as_file(data)

        assert file_contents(temp_file) == data

    def test_sub_folders(self):
        assert '/usr/bin' in sub_folders('/usr')

    def test_temp_filename(self):
        path_file = temp_filename()
        assert path_file.startswith('tmp')
        assert file_extension(path_file) == '.tmp'
        assert len(path_file) == 15

    def test_temp_folder(self):
        folder = temp_folder()
        assert folder_exists(folder) is True
        assert folder_delete(folder) is True
        with Temp_Folder() as folder_2:
            kwargs = dict(prefix        = '_bb'          ,
                          suffix        = 'aa_'          ,
                          target_folder = folder_2.path())
            folder_3 = temp_folder(**kwargs)
            folder_name(folder_3).startswith('_bb')
            folder_name(folder_3).endswith('aa_')
            assert 'aa_'  in folder_3
            assert folder_delete(folder_3) is True

    def test_file_content_md5(self):
        contents  = random_string()
        file_path = file_create(contents=contents)

        assert file_contents_md5(file_path) == bytes_md5(str_to_bytes(contents))

    def test_file_content_sha256(self):
        contents  = random_string()
        file_path = file_create(contents=contents)

        assert file_contents_sha256(file_path) == bytes_sha256(str_to_bytes(contents))

    def test_file_exists(self):
        assert file_exists(current_folder()) is False
        assert file_exists('aaaa_bbb_ccc'  ) is False
        assert file_exists(None            ) is False

    def test_folder_create_in_parent(self):
        tmp_folder   = '_tmp_folder'
        child_folder = '_child_folder'

        assert folder_exists(tmp_folder                                ) == False
        assert folder_create(tmp_folder                                ) == tmp_folder
        assert create_folder_in_parent(tmp_folder, child_folder        ) == path_combine(tmp_folder, child_folder)
        assert folder_exists(path_combine(tmp_folder, child_folder)    ) == True
        assert folder_delete_all(tmp_folder                            ) == True
        assert folder_not_exists(path_combine(tmp_folder, child_folder)) == True

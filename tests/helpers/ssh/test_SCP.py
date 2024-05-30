import os
from os import environ
from unittest import TestCase

import pytest

from osbot_utils.helpers.ssh.SCP        import SCP
from osbot_utils.helpers.ssh.TestCase__SSH import TestCase__SSH
from osbot_utils.testing.Temp_File      import Temp_File
from osbot_utils.testing.Temp_Folder    import Temp_Folder
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env              import load_dotenv
from osbot_utils.utils.Files import file_name, file_exists, file_contents, file_delete, path_combine
from osbot_utils.utils.Misc             import random_text

ENV_VAR_TEST_OSBOT__SSH_HOST      = 'SSH__HOST'
ENV_VAR_TEST_OSBOT__SSH_KEY_FILE  = 'SSH__KEY_FILE__FILE'
ENV_VAR_TEST_OSBOT__SSH_KEY_USER  = 'SSH__KEY_FILE__USER'



class test_SCP(TestCase__SSH):
    scp           : SCP
    ssh_host      : str
    ssh_key_file  : str
    ssh_key_user  : str

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ssh_host     = environ.get(ENV_VAR_TEST_OSBOT__SSH_HOST    )
        cls.ssh_key_file = environ.get(ENV_VAR_TEST_OSBOT__SSH_KEY_FILE)
        cls.ssh_key_user = environ.get(ENV_VAR_TEST_OSBOT__SSH_KEY_USER)
        if not cls.ssh_host:
            pytest.skip("SSH host not set")
        cls.scp = SCP(ssh_host=cls.ssh_host, ssh_key_file=cls.ssh_key_file, ssh_key_user=cls.ssh_key_user)

    def test__init__(self):
        with self.scp as _:
            assert _.__locals__() == {'ssh_host'          : self.ssh_host     ,
                                      'ssh_key_file'      : self.ssh_key_file ,
                                      'ssh_key_user'      : self.ssh_key_user ,
                                      'strict_host_check' : False             }

    def test_copy_file_to_host(self):
        temp_contents = random_text('some text')
        with Temp_File(contents=temp_contents) as temp_file:
            temp_file_path_1 = temp_file.file_path
            temp_file_path_2 = temp_file_path_1 + '.from-scp'
            temp_file_name   = file_name(temp_file_path_1)

            assert file_contents(temp_file_path_1) == temp_contents
            #assert self.scp.cat(temp_file_name)  == ''
            self.scp.copy_file_to_host(temp_file_path_1)
            #assert self.scp.cat(temp_file_name) == temp_contents
            self.scp.copy_file_from_host(temp_file_name, temp_file_path_2)
            assert file_contents(temp_file_path_2) == temp_contents
            file_delete(temp_file_path_1)

    def test_copy_folder_as_zip_to_host(self):
        with Temp_Folder(temp_files_to_add=10) as temp_folder:
            unzip_to_folder = random_text('_unzipped/',lowercase=True)
            self.scp.copy_folder_as_zip_to_host(temp_folder, unzip_to_folder)
            print()
            scp_files = self.scp.exec(f'cd {unzip_to_folder}; find . -type f | sed "s|^\./||"')
            assert sorted(temp_folder.files()) == sorted(scp_files.splitlines())

            self.scp.print_ls()
            self.scp.print_ls('_unzipped')
            self.scp.print_exec(f'ls -la {unzip_to_folder}')


import sys
from http import server
from http.server import SimpleHTTPRequestHandler
from unittest import TestCase
from unittest.mock import call

from osbot_utils.testing.Patch_Print import Patch_Print
from osbot_utils.testing.Temp_File import Temp_File
from osbot_utils.testing.Temp_Web_Server import Temp_Web_Server
from osbot_utils.utils.Files import file_contents, file_contains, file_name, file_exists, parent_folder, folder_exists, \
    file_not_exists, folder_not_exists, current_temp_folder, temp_filename, file_extension
from osbot_utils.utils.Misc import random_text, in_github_action
from osbot_utils.utils.Dev import pprint


class test_Temp_Web_Server(TestCase):

    def setUp(self):
        pass

    def test__enter__leave__(self):
        if not in_github_action():              # skipp locally since this now takes 500ms which is 30% of the total test time (and since we will still execute this in the CI pipeline it is ok to skip locally)
            return
        host        = "127.0.0.1"
        port        = 20002
        root_folder = current_temp_folder()
        kwargs      = {  "host"         : host        ,
                         "port"         : port        ,
                         "root_folder"  : root_folder ,
                         'wait_for_stop': True        }                                 # this is why it takes 500ms, since it wait for the port to be fully closed
        expected_content = ['<h1>Directory listing for /</h1>']
        temp_web_server = Temp_Web_Server(**kwargs)
        with temp_web_server as web_server:
            assert web_server.server_port_open()             is True
            assert web_server.GET_contains(expected_content) is True
            assert web_server.GET_contains('<html>\n'      ) is True
            assert web_server.GET_contains('aaaaaa__bbbbbb') is False

        assert web_server.server_port_open() is False
        assert web_server.GET()              is None

    def test_add_file(self):
        with Temp_File() as temp_file:
            temp_folder = temp_file.tmp_folder
            with Temp_Web_Server(root_folder=temp_folder) as web_server:
                assert len(temp_file.files_in_folder()) == 1
                new_file = web_server.add_file()
                assert len(temp_file.files_in_folder()) == 2
                assert new_file in temp_file.files_in_folder()

                another_file_name = 'aaaa.txt'
                another_contents  = 'some content'
                another_file_path = web_server.add_file(relative_file_path= another_file_name, file_contents=another_contents)
                assert len(temp_file.files_in_folder()) == 3
                assert another_file_path in temp_file.files_in_folder()
                assert file_name(another_file_path    ) == another_file_name
                assert file_contents(another_file_path) == another_contents
                assert web_server.GET(another_file_name) == another_contents

                virtual_folder         = 'some_folder/some_subfolder'
                filename_in_folder     = 'bbbb.txt'
                relative_file_path     = f'{virtual_folder}/{filename_in_folder}'
                some_random_text       = random_text()
                file_in_virtual_folder = web_server.add_file(relative_file_path=relative_file_path, file_contents=some_random_text)
                path_new_folder        = parent_folder(file_in_virtual_folder)

                assert file_in_virtual_folder == f"{temp_folder}/{virtual_folder}/{filename_in_folder}"
                assert file_exists(file_in_virtual_folder)
                assert web_server.GET(relative_file_path) == some_random_text

            assert file_exists  (new_file)
            assert folder_exists(temp_folder)
            assert folder_exists(path_new_folder)
        assert file_not_exists(new_file)
        assert folder_not_exists(temp_folder)
        assert folder_not_exists(path_new_folder)


    def test__defaults(self):
        web_server = Temp_Web_Server()
        assert web_server.host         == "127.0.0.1"
        assert type(web_server.port)   is int
        assert web_server.root_folder  == "."
        assert web_server.server_name  == "Temp_Web_Server"
        assert web_server.http_handler == SimpleHTTPRequestHandler

    def test__in_temp_folder(self):
        temp_content = random_text()
        with Temp_File(contents=temp_content) as temp_file:
            with Temp_Web_Server(root_folder=temp_file.tmp_folder) as web_server:
                temp_file_name = temp_file.tmp_file
                assert web_server.GET_contains(temp_file_name)
                assert file_contains(temp_file.file_path, temp_content)
                assert web_server.GET(temp_file_name) == temp_content

    def test__with_custom_http_handler(self):
        class MyHandler(server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = "<html><p>hello world</p></html>"

                self.wfile.write(html.encode())

            def log_message(self, msg_format, *args):
                print("%s - - %s\n" % (self.address_string(), msg_format % args))

        with Temp_Web_Server(http_handler=MyHandler) as web_server:
            with Patch_Print() as _:
                assert web_server.GET()   == '<html><p>hello world</p></html>'
                assert _.call_args_list() == [call('127.0.0.1 - - "GET / HTTP/1.1" 200 -\n')]

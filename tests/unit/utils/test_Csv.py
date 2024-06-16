import textwrap
from unittest import TestCase

import pytest

from osbot_utils.testing.Stderr import Stderr
from osbot_utils.testing.Stdout import Stdout
from osbot_utils.testing.Temp_File import Temp_File
from osbot_utils.testing.Temp_Folder import Temp_Folder
from osbot_utils.testing.Temp_Web_Server import Temp_Web_Server
from osbot_utils.utils.Csv import load_csv_from_file, load_csv_from_str, load_csv_from_url
from osbot_utils.utils.Files import file_create, file_delete, file_exists, folder_exists
from osbot_utils.utils.Http import GET
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Str import str_dedent

csv_string = """a,b,c\n1,2,3\nx,y,z"""
class Test_Csv(TestCase):

    def setUp(self) -> None:
        self.file_path = file_create(contents=csv_string)

    def tearDown(self) -> None:
        file_delete(self.file_path)

    def test_load_csv_from_file(self):
        csv_content = load_csv_from_file(self.file_path)

        assert len(csv_content) == 2
        assert csv_content.__getitem__(0).get('a') == '1'
        assert csv_content.__getitem__(1).get('b') == 'y'

    def test_load_csv_from_string(self):
        csv_content = load_csv_from_str(csv_string)

        assert len(csv_content) == 2
        assert csv_content.__getitem__(0).get('a') == '1'
        assert csv_content.__getitem__(1).get('b') == 'y'

    #@pytest.mark.skip("todo: figure out why this tests started failing intermittently (on Oct 2023)")
    def test_load_csv_from_url(self):
        with Stderr() as stderr:
            csv_file_name   = 'sample_csv_data.csv'
            sample_csv_data = str_dedent("""
                "Month", "Average", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015"
                "May",  0.1,  0,  0, 1, 1, 0, 0, 0, 2, 0,  0,  0  
                "Jun",  0.5,  2,  1, 1, 0, 0, 1, 1, 2, 2,  0,  1
                "Jul",  0.7,  5,  1, 1, 2, 0, 1, 3, 0, 2,  2,  1 
                """)

            with Temp_Folder() as temp_folder:
                web_server_root = temp_folder.full_path
                temp_csv_file = temp_folder.add_file(file_name=csv_file_name, contents=sample_csv_data)
                assert file_exists(temp_csv_file    ) is True
                assert folder_exists(web_server_root) is True
                with Temp_Web_Server(root_folder= web_server_root) as web_server:
                    url_csv_file = web_server.url(csv_file_name)
                    assert url_csv_file                  == f"http://127.0.0.1:{web_server.port}/{csv_file_name}"
                    assert web_server.GET(csv_file_name) == sample_csv_data
                    assert GET(url_csv_file)             == sample_csv_data
                    headers     = {"User-Agent"     : "Mozilla/5.0"}
                    csv_content = load_csv_from_url(url_csv_file, headers)
                    first_row   = csv_content[0]
                    assert type(csv_content)        is list
                    assert len(csv_content)         == 3
                    assert first_row.get('Month')   == 'May'
                    assert first_row                == {'Month': 'May', ' "Average"': '  0.1', ' "2005"': '  0', ' "2006"': '  0', ' "2007"': ' 1', ' "2008"': ' 1', ' "2009"': ' 0', ' "2010"': ' 0', ' "2011"': ' 0', ' "2012"': ' 2', ' "2013"': ' 0', ' "2014"': '  0', ' "2015"': '  0  '}

            assert file_exists  (temp_csv_file  ) is False
            assert folder_exists(web_server_root) is False
        assert '"GET /sample_csv_data.csv HTTP/1.1" 200 ' in stderr.value()


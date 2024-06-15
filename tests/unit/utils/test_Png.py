from unittest                           import TestCase
from osbot_utils.utils.Files            import temp_file, file_not_exists, file_exists, file_delete
from osbot_utils.testing.Log_To_String  import Log_To_String
from osbot_utils.utils.Png              import save_png_bytes_to_file, logger_png, save_png_base64_to_file
from osbot_utils.utils.Status           import osbot_status

# from 'https://via.placeholder.com/1.png?text=sample-png'
TEST_PNG_BYTES = (b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
                  b'\x02\x03\x00\x00\x00b{,\x1a\x00\x00\x00\tPLTE\xcc\xcc\xcc\x96\x96\x96\xb1'
                  b'\xb1\xb1sR\xafI\x00\x00\x00\tpHYs\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95'
                  b'+\x0e\x1b\x00\x00\x00\nIDAT\x08\x99ch\x00\x00\x00\x82\x00\x81\xcb\x13\xb2'
                  b'a\x00\x00\x00\x00IEND\xaeB`\x82')


class test_Png(TestCase):

    @classmethod
    def setUpClass(cls):
        osbot_status.clear_root_logger_handlers()

    @classmethod
    def tearDownClass(self):
        osbot_status.clear_root_logger_handlers()

    def setUp(self):
        self.path_temp_png = temp_file('.png')          # temp file path

    def tearDown(self):
        file_delete(self.path_temp_png)                 # delete file is created

    def test_save_png_bytes_to_file(self):
        with Log_To_String(logger_png) as log_to_string:
            assert file_not_exists(self.path_temp_png)
            png_file = save_png_bytes_to_file(bytes=TEST_PNG_BYTES, png_file=self.path_temp_png)
            assert png_file == self.path_temp_png
            assert file_exists(self.path_temp_png)
            assert log_to_string.contents() == f'Png data with size 148 saved to {png_file}\n'

        with Log_To_String(logger_png) as log_to_string:
            png_file = save_png_bytes_to_file(bytes=TEST_PNG_BYTES)
            assert file_exists(png_file)
            assert log_to_string.contents() == f'Png data with size 148 saved to {png_file}\n'

    def test_save_png_base64_to_file(self):
        with Log_To_String(logger_png) as log_to_string:
            assert save_png_base64_to_file(png_data={}) is None
            assert log_to_string.contents() == 'Png data was not a string: {}\n'

        with Log_To_String(logger_png) as log_to_string:
            assert save_png_base64_to_file(png_data="aaaaa_bbbbbb") is None
            assert log_to_string.contents() == 'png save error: Incorrect padding\naaaaa_bbbbbb\n'
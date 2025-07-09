from unittest                   import TestCase
from osbot_utils.utils.Files    import folder_exists, folder_name, path_combine, file_contents
from tests                      import _test_data
from tests._test_data           import html_bootstrap_example__lines

class Sample_Test_Files:

    def html_bootstrap_example(self):
        return self.sample_file_contents('html_bootstrap_example.html')

    def html_bootstrap_example__lines(self):
        return html_bootstrap_example__lines.lines

    def html_bootstrap_example__roundtrip(self):
        return self.sample_file_contents('html_bootstrap_example__round_trip.html')

    def html_bootstrap_example__roundtrip_2(self):          # todo: this is caused by a small difference between the .render() and the Parser
        return self.sample_file_contents('html_bootstrap_example__round_trip_2.html')

    def sample_file_contents(self,file_name):
        file_path = path_combine(self.path_test_files(), file_name)
        return file_contents(file_path)

    def path_test_files(self):
        return _test_data.__path__[0]


class test_Sample_Test_Files(TestCase):

    def setUp(self):
        self.sample_test_files = Sample_Test_Files()

    def test_html_bootstrap_exampe(self):
        html = self.sample_test_files.html_bootstrap_example()
        assert '<html lang="en">\n'  in html
        assert '<title>Simple Bootstrap 5 Webpage</title>' in html

    def test_path_test_files(self):
        path_test_files = self.sample_test_files.path_test_files()
        assert folder_exists(path_test_files)
        assert folder_name(path_test_files) == '_test_data'
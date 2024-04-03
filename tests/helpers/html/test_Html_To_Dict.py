from unittest import TestCase

from osbot_utils.helpers.html.Dict_To_Html import Dict_To_Html
from osbot_utils.helpers.html.Html_To_Dict import Html_To_Dict
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set, str_sha384_as_base64
from tests._test_data.Sample_Test_Files import Sample_Test_Files


class test_Html_To_Dict(TestCase):

    def test_convert(self):
        sample_test_files = Sample_Test_Files()
        html              = sample_test_files.html_bootstrap_example()
        html__lines       = sample_test_files.html_bootstrap_example__lines()
        html_parser_1     = Html_To_Dict(html)
        root_1            = html_parser_1.convert()
        lines_1           = html_parser_1.print(just_return_lines=True)
        dict_to_html_1    = Dict_To_Html(root_1)

        html_from_dict_1 = dict_to_html_1.convert()
        html_parser_2    = Html_To_Dict(html_from_dict_1)
        root_2           =  html_parser_2.convert()
        lines_2 = html_parser_2.print(just_return_lines=True)

        assert root_1  == root_2
        assert lines_1 == lines_2
        assert lines_1 == html__lines
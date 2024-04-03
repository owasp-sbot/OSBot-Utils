from unittest import TestCase

from osbot_utils.helpers.html.Dict_To_Html import Dict_To_Html
from osbot_utils.helpers.html.Html_To_Dict import Html_To_Dict
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set, str_sha384_as_base64
from tests._test_data.Sample_Test_Files import Sample_Test_Files


class test_Html_To_Dict(TestCase):

    def test_convert(self):
        sample_test_files = Sample_Test_Files()                                                      # Initialize sample test files
        html              = sample_test_files.html_bootstrap_example()                               # Load HTML sample
        html__lines       = sample_test_files.html_bootstrap_example__lines()                        # Load expected HTML lines
        html__roundtrip   = sample_test_files.html_bootstrap_example__roundtrip()                    # Load expected roundtrip HTML

        html_parser_1     = Html_To_Dict(html)                                                       # Parse HTML to dict
        root_1            = html_parser_1.convert()                                                  # Convert parsed HTML to root dict
        lines_1           = html_parser_1.print(just_return_lines=True)                              # Generate tree lines from root dict
        dict_to_html_1    = Dict_To_Html(root_1)                                                     # Initialize conversion from dict to HTML
        html_from_dict_1  = dict_to_html_1.convert()                                                 # Convert dict back to HTML

        html_parser_2     = Html_To_Dict(html_from_dict_1)                                           # Parse the regenerated HTML to dict
        root_2            = html_parser_2.convert()                                                  # Convert parsed HTML to root dict again
        lines_2           = html_parser_2.print(just_return_lines=True)                              # Generate tree lines from new root dict
        dict_to_html_2    = Dict_To_Html(root_2)                                                     # Initialize second conversion from dict to HTML
        html_from_dict_2  = dict_to_html_2.convert()                                                 # Convert dict back to HTML again

        assert root_1           == root_2                                                            # Assert that both root dicts are equal
        assert lines_1          == lines_2                                                           # Assert that both sets of lines are equal
        assert html_from_dict_1 == html_from_dict_2                                                  # Assert that both HTML conversions are equal

        assert lines_1          == html__lines                                                       # Assert that generated lines match expected lines
        assert html_from_dict_1 == html__roundtrip                                                   # Assert that generated HTML matches expected HTML


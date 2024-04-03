from unittest import TestCase

from osbot_utils.helpers.html.Dict_To_Tags import Dict_To_Tags
from osbot_utils.helpers.html.Html_To_Dict import Html_To_Dict
from osbot_utils.utils.Dev import pprint
from tests._test_data.Sample_Test_Files import Sample_Test_Files


class test_Dict_To_Tags(TestCase):


    def test_convert(self):
        sample_test_files = Sample_Test_Files()
        html              = sample_test_files.html_bootstrap_example()
        html_roundtrip    = sample_test_files.html_bootstrap_example__roundtrip()
        html_to_dict      = Html_To_Dict(html)
        root_1            = html_to_dict.convert()

        dict_to_tags      = Dict_To_Tags(root_1)
        root_tag          = dict_to_tags.convert()

        root_tag_html = root_tag.render()

        html_to_dict = Html_To_Dict(root_tag_html)
        root_2       = html_to_dict.convert()

        #print(root_tag_html)
        #assert root_tag_html == html_roundtrip
        assert root_2==root_1



        #pprint(root)
        #root['children'] = []
        #print()
        #print()
        #html_to_dict.print()
import sys
from unittest import TestCase

import pytest

from osbot_utils.helpers.html.Dict_To_Html import Dict_To_Html
from osbot_utils.helpers.html.Dict_To_Tags import Dict_To_Tags
from osbot_utils.helpers.html.Html_To_Dict import Html_To_Dict
from tests._test_data.Sample_Test_Files    import Sample_Test_Files


class test_Dict_To_Tags(TestCase):

    @classmethod
    def setUpClass(cls):
        if sys.version_info < (3, 9):
            pytest.skip("Skipping tests that doesn't work on 3.8 or lower")

    def test_convert(self):
        sample_test_files = Sample_Test_Files()
        html              = sample_test_files.html_bootstrap_example()
        html_roundtrip    = sample_test_files.html_bootstrap_example__roundtrip()
        html_to_dict      = Html_To_Dict(html)
        root_1            = html_to_dict.convert()
        lines_1           = html_to_dict.print(just_return_lines=True)

        dict_to_tags      = Dict_To_Tags(root_1)
        root_tag          = dict_to_tags.convert()

        root_tag.doc_type = False
        root_tag_html     = root_tag.render()

        html_to_dict      = Html_To_Dict(root_tag_html)
        root_2            = html_to_dict.convert()
        lines_2           = html_to_dict.print(just_return_lines=True)

        assert root_1  == root_2
        assert lines_1 == lines_2
        #assert root_tag_html == html_roundtrip                         # todo: fix little issue with extra space in the attributes

        dict_to_html_2 = Dict_To_Html(root_2)
        assert dict_to_html_2.convert() == html_roundtrip               # confirm that roundstrip is working ok
        #print(html_roundtrip)





        #pprint(root)
        #root['children'] = []
        #print()
        #print()
        #html_to_dict.print()
import sys
import pytest
from unittest                               import TestCase
from osbot_utils.helpers.html.Dict_To_Html  import Dict_To_Html
from osbot_utils.helpers.html.Dict_To_Tags  import Dict_To_Tags
from osbot_utils.helpers.html.Html_To_Dict  import Html_To_Dict
from osbot_utils.helpers.html.Tag__Html     import Tag__Html
from tests._test_data.Sample_Test_Files     import Sample_Test_Files


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

    def convert_html(self, html):
        html_parser_    = Html_To_Dict        (html)
        html_dict       = html_parser_.convert()
        dict_to_tags    = Dict_To_Tags        (html_dict)
        result          = dict_to_tags.convert()
        return result

    def test__convert_attributes(self):
        html_1 = '<html lang="en" class="an-class"></html>'
        with self.convert_html(html_1) as _:
            assert type(_) is Tag__Html


    def test__bug__class_in_xyz(self):


        html_1           = '<html lang="en" class="js-focus-visible js" data-js-focus-visible=""></html>'
        expected_error_1 = "Tag__Html has no attribute 'class' and cannot be assigned the value 'js-focus-visible js'. Use Tag__Html.__default_kwargs__() see what attributes are available"
        #with pytest.raises(ValueError, match=re.escape(expected_error_1)):
        self.convert_html(html_1)       # FIXED

        html_2           = '<html lang="en" data-js-focus-visible=""></html>'
        expected_error_2 = "Tag__Html has no attribute 'data-js-focus-visible' and cannot be assigned the value ''. Use Tag__Html.__default_kwargs__() see what attributes are available"
        #with pytest.raises(ValueError, match=re.escape(expected_error_2)):
        self.convert_html(html_2) #  FIXED


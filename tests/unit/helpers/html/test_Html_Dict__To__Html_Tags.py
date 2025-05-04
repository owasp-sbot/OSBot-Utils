import sys
import pytest
from unittest                                           import TestCase
from osbot_utils.helpers.html.Html_Dict__To__Html       import Html_Dict__To__Html
from osbot_utils.helpers.html.Html_Dict__To__Html_Tags  import Html_Dict__To__Html_Tags
from osbot_utils.helpers.html.Html__To__Html_Dict       import Html__To__Html_Dict
from osbot_utils.helpers.html.Tag__Html                 import Tag__Html
from osbot_utils.helpers.html.Tag__Text                 import Tag__Text
from tests._test_data.Sample_Test_Files                 import Sample_Test_Files


class test_Html_Dict__To__Html_Tags(TestCase):

    @classmethod
    def setUpClass(cls):
        if sys.version_info < (3, 9):
            pytest.skip("Skipping tests that doesn't work on 3.8 or lower")

    def test_convert__simple(self):
        html = """\
<!DOCTYPE html>
<html lang="en">
    <head>
      <meta charset="UTF-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Simple Bootstrap 5 Webpage</title>
    </head>
    <body>
</html>"""

        html_to_dict      = Html__To__Html_Dict(html)
        root_1            = html_to_dict.convert()
        dict_to_tags      = Html_Dict__To__Html_Tags(root_1)
        root_tag          = dict_to_tags.convert()

        root_tag.doc_type = False
        root_tag_html     = root_tag.render()
        html_to_dict      = Html__To__Html_Dict(root_tag_html)
        root_2            = html_to_dict.convert()
        assert root_1     == root_2


    def test_convert(self):
        sample_test_files = Sample_Test_Files()
        html              = sample_test_files.html_bootstrap_example()
        html_roundtrip    = sample_test_files.html_bootstrap_example__roundtrip_2()
        html_to_dict      = Html__To__Html_Dict(html)
        root_1            = html_to_dict.convert()
        lines_1           = html_to_dict.print(just_return_lines=True)

        dict_to_tags      = Html_Dict__To__Html_Tags(root_1)
        root_tag          = dict_to_tags.convert()

        root_tag.doc_type = False
        root_tag_html     = root_tag.render()

        html_to_dict      = Html__To__Html_Dict(root_tag_html)
        root_2            = html_to_dict.convert()
        lines_2           = html_to_dict.print(just_return_lines=True)

        assert root_1  == root_2
        assert lines_1 == lines_2
        assert root_tag_html == html_roundtrip          # misses DOCTYPE HERE


        dict_to_tags_2  = Html_Dict__To__Html_Tags(root_2)
        root_tag_2      = dict_to_tags_2.convert()
        root_tag_html_2 = root_tag_2.render()
        assert root_tag_html_2 == root_tag_html         # we lose the "'<!DOCTYPE html>\n'" here

        #dict_to_html_2 = Dict__To__Html(root_1)
        #print(root_2.render())
        from osbot_utils.utils.Dev import pprint
        #pprint(root_2)
        #print(dict_to_html_2.convert())
        # assert dict_to_html_2.dict_to_html_2() == html_roundtrip               # confirm that roundstrip is working ok
        #print(html_roundtrip)





        #pprint(root)
        #root['children'] = []
        #print()
        #print()
        #html_to_dict.print()

    def convert_html(self, html):
        html_parser_    = Html__To__Html_Dict        (html)
        html_dict       = html_parser_.convert()
        dict_to_tags    = Html_Dict__To__Html_Tags        (html_dict)
        result          = dict_to_tags.convert()
        return result

    def test__convert_attributes(self):
        html_1 = '<html lang="en" class="an-class"></html>'
        with self.convert_html(html_1) as _:
            assert type(_) is Tag__Html


    def test__regression__class_in_xyz(self):


        html_1           = '<html lang="en" class="js-focus-visible js" data-js-focus-visible=""></html>'
        expected_error_1 = "Tag__Html has no attribute 'class' and cannot be assigned the value 'js-focus-visible js'. Use Tag__Html.__default_kwargs__() see what attributes are available"
        #with pytest.raises(ValueError, match=re.escape(expected_error_1)):
        self.convert_html(html_1)       # FIXED

        html_2           = '<html lang="en" data-js-focus-visible=""></html>'
        expected_error_2 = "Tag__Html has no attribute 'data-js-focus-visible' and cannot be assigned the value ''. Use Tag__Html.__default_kwargs__() see what attributes are available"
        #with pytest.raises(ValueError, match=re.escape(expected_error_2)):
        self.convert_html(html_2) #  FIXED


class test_Html_To_Dict(TestCase):

    def test_text_node_render(self):
        text_node = Tag__Text(data="Hello world")
        rendered = text_node.render()
        assert rendered == "Hello world"

    def test_render_with_text_nodes(self):
        from osbot_utils.helpers.html.Tag__Base import Tag__Base

        # Create a paragraph with mixed content
        para = Tag__Base(tag_name="p", indent=0)

        # Add text before
        para.elements.append(Tag__Text(data="Text before "))

        # Add a bold element
        bold = Tag__Base(tag_name="b", indent=1)
        bold.elements.append(Tag__Text(data="Bold text"))
        para.elements.append(bold)

        # Add text after
        para.elements.append(Tag__Text(data=" and text after"))

        # Render the paragraph
        rendered = para.render()

        # Expected: <p>Text before     <b>Bold text</b> and text after</p>
        expected = "<p>Text before     <b>Bold text</b> and text after</p>"

        # Strip newlines for comparison as the newline handling may vary
        rendered_normalized = rendered.replace("\n", "")
        assert rendered_normalized == expected



    def test__bug__convert_with_text_nodes(self):
        # Create a dictionary structure with text nodes
        html_dict = {
            'tag': 'div',
            'attrs': {'class': 'container'},
            'children': [
                {'type': 'text', 'data': 'Text before'},
                {
                    'tag': 'p',
                    'attrs': {},
                    'children': [{'type': 'text', 'data': 'Paragraph content'}]
                },
                {'type': 'text', 'data': 'Text after'}
            ]
        }

        wrong__html_dict = {'attrs': {'class': 'container'},
                             'children': [{'data': 'Text before    ', 'type': 'text'},                      # todo: BUG: extra space here
                                          {'attrs': {},
                                           'children': [{'data': 'Paragraph content', 'type': 'text'}],
                                           'tag': 'p'},
                                          {'data': '\nText after', 'type': 'text'}],                        # todo: BUG: extra 'n' here
                             'tag': 'div'}

        wrong_html = ('<!DOCTYPE html>\n'
 '<div class="container">Text before    <p>Paragraph content</p>\n'
 'Text after</div>\n')

        # Convert to HTML
        dict_to_html = Html_Dict__To__Html(html_dict)
        html = dict_to_html.convert()




        # Parse back to dict to verify structure preservation
        html_dict_2 = Html__To__Html_Dict(html, ).convert()

        # Compare structures
        assert html_dict   != html_dict_2                                           # todo: BUG - these should be equal
        assert html_dict_2 == wrong__html_dict                                      # todo: BUG
        assert html        == wrong_html                                            # todo: BUG

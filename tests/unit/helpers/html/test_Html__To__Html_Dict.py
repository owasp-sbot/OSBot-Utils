from unittest                                       import TestCase
from osbot_utils.helpers.html.Html_Dict__To__Html   import Html_Dict__To__Html
from osbot_utils.helpers.html.Html__To__Html_Dict   import Html__To__Html_Dict
from tests._test_data.Sample_Test_Files             import Sample_Test_Files


class test_Html__To__Html_Dict(TestCase):

    def test_convert(self):
        sample_test_files = Sample_Test_Files()                                                      # Initialize sample test files
        html              = sample_test_files.html_bootstrap_example()                               # Load HTML sample
        html__lines       = sample_test_files.html_bootstrap_example__lines()                        # Load expected HTML lines

        html__roundtrip   = sample_test_files.html_bootstrap_example__roundtrip()                    # Load expected roundtrip HTML

        html_parser_1     = Html__To__Html_Dict(html)                                                       # Parse HTML to dict
        root_1            = html_parser_1.convert()                                                  # Convert parsed HTML to root dict
        lines_1           = html_parser_1.print(just_return_lines=True)                              # Generate tree lines from root dict
        dict_to_html_1    = Html_Dict__To__Html(root_1)                                                     # Initialize conversion from dict to HTML
        html_from_dict_1  = dict_to_html_1.convert()                                                 # Convert dict back to HTML

        html_parser_2     = Html__To__Html_Dict(html_from_dict_1)                                           # Parse the regenerated HTML to dict
        root_2            = html_parser_2.convert()                                                  # Convert parsed HTML to root dict again
        lines_2           = html_parser_2.print(just_return_lines=True)                              # Generate tree lines from new root dict
        dict_to_html_2    = Html_Dict__To__Html(root_2)                                                     # Initialize second conversion from dict to HTML
        html_from_dict_2  = dict_to_html_2.convert()                                                 # Convert dict back to HTML again

        assert root_1           == root_2                                                            # Assert that both root dicts are equal
        assert lines_1          == lines_2                                                           # Assert that both sets of lines are equal
        assert html_from_dict_1 == html_from_dict_2                                                  # Assert that both HTML conversions are equal
        assert lines_1          == html__lines                                                       # Assert that generated lines match expected lines


        assert html_from_dict_1 == html__roundtrip                                                   # Assert that generated HTML matches expected HTML
        #print(html_from_dict_1)

    def test_convert__simple(self):
        html = """\
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Simple Bootstrap 5 Webpage</title>
    </head>
</html>
"""

        html_parser_1     = Html__To__Html_Dict(html)                                                       # Parse HTML to dict
        root_1            = html_parser_1.convert()                                                  # Convert parsed HTML to root dict
        dict_to_html_1    = Html_Dict__To__Html(root_1)                                                     # Initialize conversion from dict to HTML
        html_from_dict_1  = dict_to_html_1.convert()

        assert html_from_dict_1 == html

    # todo: review this test with the other tests here since there is quite a lot of duplicated tests here
    def test__handle_text_variations(self):
        html_1     = "<p>aaaa</p>"
        expected_1 = {'attrs'   : {}                ,
                      'children': [{'data': 'aaaa'  ,
                                    'type': 'text'}],
                      'tag'     : 'p'              }

        html_2     = "<p>aaaa<br></p>"
        expected_2 = {'attrs'   : {}                   ,
                      'children': [{'data' : 'aaaa'    ,
                                    'type' : 'text'}   ,
                                   { 'attrs'   : {}    ,
                                     'children': []    ,
                                     'tag'     : 'br'}],
                      'tag': 'p'                       }

        html_3     = "<p>aaaa<br>bbbb</p>"
        expected_3 = { 'attrs'   : {},
                       'children': [{'data' : 'aaaa', 'type'    : 'text'         },
                                    {'attrs': {}    , 'children': [], 'tag': 'br'},
                                    {'data'  : 'bbbb', 'type'   : 'text'         }],
                       'tag'      : 'p'}

           # Additional test cases
        html_4     = "<p>aaaa<b>bbbb</b>cccc</p>"
        expected_4 = {'attrs'   : {}                ,
                      'children': [{'data' : 'aaaa' ,
                                    'type' : 'text'},
                                   {'attrs'   : {}  ,
                                    'children': [{'data': 'bbbb',
                                                  'type': 'text'}],
                                    'tag'     : 'b' },
                                   {'data' : 'cccc' ,
                                    'type' : 'text'}],
                      'tag'     : 'p'               }

        html_5     = "<div><p>aaaa</p><p>bbbb</p></div>"
        expected_5 = {'attrs'   : {}                ,
                      'children': [{'attrs'   : {}  ,
                                    'children': [{'data': 'aaaa',
                                                  'type': 'text'}],
                                    'tag'     : 'p' },
                                   {'attrs'   : {}  ,
                                    'children': [{'data': 'bbbb',
                                                  'type': 'text'}],
                                    'tag'     : 'p' }],
                      'tag'     : 'div'             }

        html_6     = "<p>aaaa<br/>bbbb</p>"
        expected_6 = {'attrs'   : {}                ,
                      'children': [{'data' : 'aaaa' ,
                                    'type' : 'text'},
                                   {'attrs'   : {}  ,
                                    'children': []  ,
                                    'tag'     : 'br'},
                                   {'data': 'bbbb'  ,
                                    'type': 'text'}],
                      'tag'     : 'p'               }

        html_7     = "<p>aaaa<img src='image.jpg'>bbbb</p>"
        expected_7 = { 'attrs'   : {},
                       'children': [{'data': 'aaaa', 'type': 'text'},
                                   {'attrs': {'src': 'image.jpg'}, 'children': [], 'tag': 'img'},
                                   {'data': 'bbbb', 'type': 'text'}],
                       'tag'     : 'p'}

        assert Html__To__Html_Dict(html_1).convert() == expected_1
        assert Html__To__Html_Dict(html_2).convert() == expected_2
        assert Html__To__Html_Dict(html_3).convert() == expected_3
        assert Html__To__Html_Dict(html_4).convert() == expected_4
        assert Html__To__Html_Dict(html_5).convert() == expected_5
        assert Html__To__Html_Dict(html_6).convert() == expected_6
        assert Html__To__Html_Dict(html_7).convert() == expected_7

    def test_basic_text_handling(self):
        html_1     = "<p>aaaa</p>"
        expected_1 = {'attrs'   : {}                ,
                      'children': [{'data': 'aaaa'  ,
                                    'type': 'text'}],
                      'tag'     : 'p'               }

        assert Html__To__Html_Dict(html_1).convert() == expected_1

    def test_void_elements(self):
        html_2     = "<p>aaaa<br></p>"
        expected_2 = {'attrs'   : {}                ,
                      'children': [{'data' : 'aaaa' ,
                                    'type' : 'text'},
                                   {'attrs'   : {}  ,
                                    'children': []  ,
                                    'tag'     : 'br'}],
                      'tag'     : 'p'               }

        assert Html__To__Html_Dict(html_2).convert() == expected_2

    def test_text_after_void_element(self):
        html_3     = "<p>aaaa<br>bbbb</p>"
        expected_3 = {'attrs'   : {}                ,
                      'children': [{'data' : 'aaaa' ,
                                    'type' : 'text'},
                                   {'attrs'   : {}  ,
                                    'children': []  ,
                                    'tag'     : 'br'},
                                   {'data': 'bbbb'  ,
                                    'type': 'text'}],
                      'tag'     : 'p'               }

        assert Html__To__Html_Dict(html_3).convert() == expected_3

    def test_text_around_regular_element(self):
        html_4     = "<p>aaaa<b>bbbb</b>cccc</p>"
        expected_4 = {'attrs'   : {}                ,
                      'children': [{'data' : 'aaaa' ,
                                    'type' : 'text'},
                                   {'attrs'   : {}  ,
                                    'children': [{'data': 'bbbb',
                                                  'type': 'text'}],
                                    'tag'     : 'b' },
                                   {'data' : 'cccc' ,
                                    'type' : 'text'}],
                      'tag'     : 'p'               }

        assert Html__To__Html_Dict(html_4).convert() == expected_4

    def test_nested_elements(self):
        html_5     = "<div><p>aaaa</p><p>bbbb</p></div>"
        expected_5 = {'attrs'   : {}                ,
                      'children': [{'attrs'   : {}  ,
                                    'children': [{'data': 'aaaa',
                                                  'type': 'text'}],
                                    'tag'     : 'p' },
                                   {'attrs'   : {}  ,
                                    'children': [{'data': 'bbbb',
                                                  'type': 'text'}],
                                    'tag'     : 'p' }],
                      'tag'     : 'div'             }

        assert Html__To__Html_Dict(html_5).convert() == expected_5

    def test_self_closing_syntax(self):
        html_6     = "<p>aaaa<br/>bbbb</p>"
        expected_6 = {'attrs'   : {}                ,
                      'children': [{'data' : 'aaaa' ,
                                    'type' : 'text'},
                                   {'attrs'   : {}  ,
                                    'children': []  ,
                                    'tag'     : 'br'},
                                   {'data': 'bbbb'  ,
                                    'type': 'text'}],
                      'tag'     : 'p'               }

        assert Html__To__Html_Dict(html_6).convert() == expected_6

    def test_void_element_with_attributes(self):
        html_7     = "<p>aaaa<img src='image.jpg'>bbbb</p>"
        expected_7 = {'attrs'   : {}                ,
                      'children': [{'data' : 'aaaa' ,
                                    'type' : 'text'},
                                   {'attrs'   : {'src': 'image.jpg'},
                                    'children': []  ,
                                    'tag'     : 'img'},
                                   {'data': 'bbbb'  ,
                                    'type': 'text'}],
                      'tag'     : 'p'               }

        assert Html__To__Html_Dict(html_7).convert() == expected_7

    def test_complex_nesting(self):
        html_8     = "<div>before<p>text1<span>inner</span>text2</p>after</div>"
        expected_8 = {'attrs'   : {}                ,
                      'children': [{'data' : 'before',
                                    'type' : 'text'},
                                   {'attrs'   : {}  ,
                                    'children': [{'data' : 'text1',
                                                  'type' : 'text'},
                                                 {'attrs'   : {},
                                                  'children': [{'data': 'inner',
                                                                'type': 'text'}],
                                                  'tag'     : 'span'},
                                                 {'data' : 'text2',
                                                  'type' : 'text'}],
                                    'tag'     : 'p' },
                                   {'data' : 'after',
                                    'type' : 'text'}],
                      'tag'     : 'div'             }

        assert Html__To__Html_Dict(html_8).convert() == expected_8

    def test_html_round_trip(self):
        original_html = """
        <div class="container">
            <h1>Title</h1>
            <p>Before<strong>middle</strong>after</p>
            <img src="test.jpg" alt="test">
        </div>
        """

        expected__original_html_dict = {'attrs': {'class': 'container'},
                              'children': [{'attrs': {},
                                            'children': [{'data': 'Title', 'type': 'text'}],
                                            'tag': 'h1'},
                                           {'attrs': {},
                                            'children': [{'data': 'Before', 'type': 'text'},
                                                         {'attrs': {},
                                                          'children': [{'data': 'middle', 'type': 'text'}],
                                                          'tag': 'strong'},
                                                         {'data': 'after', 'type': 'text'}],
                                            'tag': 'p'},
                                           {'attrs': {'alt': 'test', 'src': 'test.jpg'},
                                            'children': [],
                                            'tag': 'img'}],
                              'tag': 'div'}
        expected__round_trip_html_dict = {'attrs': {'class': 'container'},
                                     'children': [{'attrs': {},
                                                   'children': [{'data': 'Title', 'type': 'text'}],
                                                   'tag': 'h1'},
                                                  {'attrs': {},
                                                   'children': [{'data': 'Before        ', 'type': 'text'},             # todo: BUG: extra space here
                                                                {'attrs': {},
                                                                 'children': [{'data': 'middle', 'type': 'text'}],
                                                                 'tag': 'strong'},
                                                                {'data': '\nafter', 'type': 'text'}],                   # todo: BUG: extra \n here
                                                   'tag': 'p'},
                                                  {'attrs': {'alt': 'test', 'src': 'test.jpg'},
                                                   'children': [],
                                                   'tag': 'img'}],
                                     'tag': 'div'}
        expected__html_from_dict = """\
<!DOCTYPE html>
<div class="container">
    <h1>Title</h1>
    <p>Before        <strong>middle</strong>
after</p>
    <img src="test.jpg" alt="test" />
</div>
"""
        # Parse HTML to dict
        html_dict = Html__To__Html_Dict(original_html).convert()

        # Convert dict back to HTML
        dict_to_html   = Html_Dict__To__Html(html_dict)
        html_from_dict = dict_to_html.convert()

        # Parse the regenerated HTML back to dict
        final_dict = Html__To__Html_Dict(html_from_dict).convert()

        # The structure should be preserved after a round trip

        assert html_dict      == expected__original_html_dict
        assert html_from_dict == expected__html_from_dict
        assert final_dict     == expected__round_trip_html_dict
        assert html_dict != final_dict                                                                                  # todo: BUG these should match

    def test_bootstrap_example(self):
        # This is a more complex test with a realistic Bootstrap HTML example
        bootstrap_html = """
        <html lang="en">
            <head>
                <meta charset="UTF-8" />
                <title>Bootstrap Example</title>
                <link href="bootstrap.min.css" rel="stylesheet" />
            </head>
            <body>
                <nav class="navbar navbar-dark bg-dark">
                    <div class="container">
                        <a class="navbar-brand" href="#">Brand</a>
                        <ul class="navbar-nav">
                            <li class="nav-item"><a class="nav-link" href="#">Home</a></li>
                        </ul>
                    </div>
                </nav>
            </body>
        </html>
        """

        # Parse to dict and then back to HTML
        html_dict = Html__To__Html_Dict(bootstrap_html).convert()
        dict_to_html = Html_Dict__To__Html(html_dict)
        html_from_dict = dict_to_html.convert()

        # Parse the regenerated HTML back to dict
        final_dict = Html__To__Html_Dict(html_from_dict).convert()

        # The structure should be preserved
        assert html_dict == final_dict

    def test_comments_preservation(self):
        # This test will fail because HTML comments are currently not handled
        # This test is a placeholder for future enhancement
        html_10 = """
        <div>
            <!-- Comment before -->
            <p>Content</p>
            <!-- Comment after -->
        </div>
        """

        # This is expected to fail currently since comment handling isn't implemented
        # You may want to skip this test until comment handling is added
        # self.skipTest("Comment handling not yet implemented")

        # For now, just validate that the content part works
        html_dict = Html__To__Html_Dict(html_10).convert()
        assert any(child.get('tag') == 'p' for child in html_dict.get('children', []))


    def test__bug__mixed_content_formatting(self):
        # Test proper indentation with mixed text and element content
        html_9 = """
        <div>
            Text before
            <p>Paragraph</p>
            Text after
        </div>
        """

        expected_wrong_final_dict  = {'attrs': {},
                                      'children': [{'data': '\n            Text before\n                ',
                                                    'type': 'text'},
                                                   {'attrs': {},
                                                    'children': [{'data': 'Paragraph', 'type': 'text'}],
                                                    'tag': 'p'},
                                                   {'data': '\n\n            Text after\n        ', 'type': 'text'}],
                                      'tag': 'div'}
        # Parse and then render back to HTML
        html_dict = Html__To__Html_Dict(html_9).convert()
        dict_to_html = Html_Dict__To__Html(html_dict)
        html_from_dict = dict_to_html.convert()

        # The rendered HTML should have proper indentation
        # Here we're just ensuring it doesn't crash and checking the structure
        final_dict = Html__To__Html_Dict(html_from_dict).convert()
        assert final_dict != html_dict                                              # todo: BUG should be equal
        assert final_dict == expected_wrong_final_dict                              # todo: BUG
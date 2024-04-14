from html.parser import HTMLParser
from unittest import TestCase

from osbot_utils.helpers.html.Html_To_Dict import Html_To_Dict
from osbot_utils.helpers.html.Tag__Html import Tag__Html
from osbot_utils.helpers.html.Tag__Link import Tag__Link
from osbot_utils.utils.Dev import pprint


class test_Tag__Html(TestCase):

    def setUp(self):
        self.html = Tag__Html()

    def test_render(self):
        #self.html.print()
        assert self.html.render()  == """<!DOCTYPE html>
<html>
    <head></head>
    <body></body>
</html>"""

    def test_render__without_doc_type(self):
        self.html.doc_type = False
        assert self.html.render() == """<html>
    <head></head>
    <body></body>
</html>"""

    def test_render__with_lang(self):
        self.html.doc_type = False
        self.html.lang     = 'en'
        assert self.html.render() == """<html lang="en">
    <head></head>
    <body></body>
</html>"""

    def test_render__with_title(self):
        self.html.doc_type   = False
        self.html.lang       = 'en'
        self.html.head.title = 'an title'
        assert self.html.render() == """<html lang="en">
    <head>
        <title>an title</title>
    </head>
    <body></body>
</html>"""

    def test_render__with_title_and_empty_link(self):
        self.html.doc_type   = False
        self.html.lang       = 'en'
        self.html.head.title = 'an title'
        link = Tag__Link()
        self.html.head.links.append(link)
        assert self.html.render() == """<html lang="en">
    <head>
        <title>an title</title>
        <link/>
    </head>
    <body></body>
</html>"""

    def test__html_with_title(self):
        with self.html as _:
            _.lang       = 'en'
            _.head.title = 'an title'
            _.head.links.append(Tag__Link())
            html = _.render()
            assert html == """<!DOCTYPE html>
<html lang="en">
    <head>
        <title>an title</title>
        <link/>
    </head>
    <body></body>
</html>"""

        html_to_dict = Html_To_Dict(html)
        html_to_dict.convert()

        assert html_to_dict.print(just_return_lines=True) == ['html (lang="en")',
                                                              '    ├── head\n'
                                                              '    │   ├── title\n'
                                                              '    │   └── link',
                                                              '    └── body']

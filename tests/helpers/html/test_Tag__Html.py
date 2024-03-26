from unittest import TestCase

from osbot_utils.helpers.html.Tag__Html import Tag__Html
from osbot_utils.helpers.html.Tag__Link import Tag__Link


class test_Tag__Html(TestCase):

    def setUp(self):
        self.html = Tag__Html()

    def test_render(self):
        assert self.html.render()  == """<!DOCTYPE html>
<html>
    <head></head>
</html>"""
        self.html.doc_type = False
        assert self.html.render() == """<html>
    <head></head>
</html>"""
        self.html.lang = 'en'
        assert self.html.render() == """<html lang="en">
    <head></head>
</html>"""

        self.html.head.title = 'an title'
        assert self.html.render() == """<html lang="en">
    <head>
        <title>an title</title>
    </head>
</html>"""

        link = Tag__Link()
        self.html.head.links.append(link)
        assert self.html.render() == """<html lang="en">
    <head>
        <title>an title</title>
        <link/>
    </head>
</html>"""

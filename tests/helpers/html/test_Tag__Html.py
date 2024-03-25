from unittest import TestCase

from osbot_utils.helpers.html.Tag__Html import Tag__Html


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

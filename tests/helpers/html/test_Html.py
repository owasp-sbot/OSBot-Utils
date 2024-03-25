from unittest import TestCase

from osbot_utils.helpers.html.Html import Html


class test_Html(TestCase):

    def setUp(self):
        self.html = Html()

    def test_render(self):
        assert self.html.render()  == """<!DOCTYPE html>
<html></html>"""
        self.html.doc_type = False
        assert self.html.render() == """<html></html>"""
        self.html.lang = 'en'
        assert self.html.render() == """<html lang="en"></html>"""

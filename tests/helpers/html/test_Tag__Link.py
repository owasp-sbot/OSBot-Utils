from unittest import TestCase

from packaging.tags import Tag

from osbot_utils.helpers.html.Tag__Base import Tag__Base
from osbot_utils.helpers.html.Tag__Link import Tag__Link
from osbot_utils.utils.Misc import random_string


class test_Tag__Link(TestCase):

    def setUp(self):
        self.tag_link = Tag__Link()#.locked()

    def test__init__(self):
        base_tag_values = Tag__Base().__locals__()
        expected_values = { **base_tag_values,
                            'end_tag'   : False  ,
                            'href'      : ''     ,
                            'integrity' : ''     ,
                            'rel'       : ''     ,
                            'tag_name'  : 'link' }
        assert self.tag_link.__locals__() == expected_values

    def test_render(self):
        assert self.tag_link.render() == '<link/>'
        href      = random_string(prefix='href')
        integrity = random_string(prefix='integrity')
        rel       = random_string(prefix='ref')

        with self.tag_link as _:
            _.href      = href
            _.integrity = integrity
            _.rel       = rel
            assert _.attributes_values('href', 'integrity', 'rel') == dict(href=href, rel=rel, integrity=integrity)
            assert self.tag_link.render() == f'<link href="{href}" integrity="{integrity}" rel="{rel}"/>'
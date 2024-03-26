from unittest import TestCase

from packaging.tags import Tag

from osbot_utils.helpers.html.Tag__Base import Tag__Base
from osbot_utils.helpers.html.Tag__Link import Tag__Link


class test_Tag__Link(TestCase):

    def setUp(self):
        self.tag_link = Tag__Link()

    def test__init__(self):
        base_tag_values = Tag__Base().__locals__()
        expected_values = { **base_tag_values,
                            'end_tag'   : False  ,
                            'href'      : ''     ,
                            'integrity' : ''     ,
                            'rel'       : ''     ,
                            'tag_name'  : 'link' }
        assert self.tag_link.__locals__() == expected_values
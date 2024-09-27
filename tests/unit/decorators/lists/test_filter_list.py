from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_utils.decorators.lists.filter_list import filter_list


class test_filter_list(TestCase):
    def setUp(self):
        self.data = [{'a': 42, 'b': 43}, {'a': 44, 'b': 45, 'c': 46}]

    @filter_list
    def an_method(self):
        return self.data

    def test__filter_list(self):
        assert self.an_method()                == self.data
        assert self.an_method(only_show=['a']) == [{'a': 42}, {'a': 44}]
        assert self.an_method(only_show=['b']) == [{'b': 43}, {'b': 45}]
        assert self.an_method(only_show=['c']) == [{}       , {'c': 46}]



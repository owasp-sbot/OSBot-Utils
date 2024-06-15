from unittest import TestCase

from osbot_utils.utils.Assert import Assert


class test_Assert(TestCase):

    def setUp(self) -> None:
        pass
        #self.assert = Assert()

    def test_is_class(self):
        Assert(self).is_class('test_Assert')

    def test_contains(self):
        Assert('abcdef').contains('abc')

    def test_field_is_equal(self):
        Assert({'a': 42}).field_is_equal('a', 42)

    def test_is_bigger_than(self):
        Assert([1,2,3,4]).is_bigger_than(3)
        Assert(4        ).is_bigger_than(3)

    def test_is_smaller_than(self):
        Assert([1,2,3,4]).is_smaller_than(5)
        Assert(4        ).is_smaller_than(5)

    def test_is_equal(self):
        Assert({'a': 42}).is_equal({'a': 42})
        Assert("aaaabbb").is_equal("aaaabbb")

    def test_match_regex(self):
        Assert("aaaabbb").match_regex("a*")

    def test_size_is(self):
        Assert([1,2,3,4]).size_is(4)

    def test_regex_not_match(self):
        Assert("aaaabbb").regex_not_match("cc*")



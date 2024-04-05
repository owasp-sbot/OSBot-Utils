from unittest import TestCase

from osbot_utils.fluent.Fluent_List import Fluent_List


class test_Fluent_List(TestCase):

    def setUp(self) -> None:
        self.list        = ['a','c','f','z','b']
        self.fluent_list = Fluent_List(self.list)

    def test_contains(self):
        assert self.fluent_list.contains('' ) is False
        assert self.fluent_list.contains('a') is True

    def test_index(self):
        assert self.fluent_list.index(0) == 'a'
        assert self.fluent_list.index(1) == 'c'
        assert self.fluent_list.index(4) == 'b'
        assert self.fluent_list.index(6) is None

    def test_first(self):
        assert self.fluent_list.first() == 'a'

    def test_last(self):
        assert self.fluent_list.last() == 'b'

    def test_pop(self):
        assert self.fluent_list.pop()  == 'b'
        assert self.fluent_list.size() == 4
        assert self.fluent_list.pop()  == 'z'
        assert self.fluent_list.size() == 3
        assert self.fluent_list.pop()  == 'f'
        assert self.fluent_list.size() == 2
        assert self.fluent_list.pop() == 'c'
        assert self.fluent_list.size() == 1
        assert self.fluent_list.pop() == 'a'
        assert self.fluent_list.size() == 0
        assert self.fluent_list.pop() == None           #
        assert self.fluent_list.size() == 0

    def test_push(self):
        assert self.fluent_list.push(42)
        assert self.fluent_list.size() == 6

    def test_size(self):
        assert self.fluent_list.size() == 5

    def test_sorted(self):
        assert self.fluent_list.sorted() == ['a', 'b', 'c', 'f', 'z']

    def test_type(self):
        assert self.fluent_list.type() == Fluent_List
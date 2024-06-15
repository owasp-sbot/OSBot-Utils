from unittest import TestCase

from osbot_utils.fluent.Fluent_Dict import Fluent_Dict


class test_Fluent_Dict(TestCase):

    def setUp(self) -> None:
        self.dict        = { 'a': 42, 'b': 42}
        self.fluent_dict = Fluent_Dict(self.dict)

    def test_keys(self):
        assert self.fluent_dict.keys() == ['a', 'b']

    def test_size(self):
        assert self.fluent_dict.size() == 2

    def test_type(self):
        assert self.fluent_dict.type() == Fluent_Dict
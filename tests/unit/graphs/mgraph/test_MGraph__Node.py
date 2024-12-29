from unittest                               import TestCase
from osbot_utils.graphs.mgraph.MGraph__Node import MGraph__Node


class test_MGraph__Node(TestCase):

    def setUp(self):
        self.node = MGraph__Node()

    def test__init__(self):
        assert self.node.__attr_names__() == ['attributes', 'key', 'label']

    def test___str__(self):
        assert str(self.node) == f'[Graph Node] {self.node.key}'
        assert self.node.label == self.node.key
        self.node.set_key('new-key')
        assert str(self.node) == f'[Graph Node] new-key'
        assert self.node.label != self.node.key
        self.node.set_label('new-key')
        assert self.node.label == self.node.key
        assert repr(self.node) == f'[Graph Node] new-key'

    def test_data(self):
        assert self.node.data() == {'attributes': {}, 'key': self.node.key, 'label': self.node.label}
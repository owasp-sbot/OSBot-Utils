from unittest import TestCase

import pytest

from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Call_Tree import Call_Tree
from osbot_utils.utils.Dev import pprint


class test_Call_Tree(TestCase):

    def setUp(self):
        self.call_tree = Call_Tree()


    @pytest.mark.skip('todo: finish implementation')
    def test_get_called_methods(self):
        #aaaaaa
        print("*" * 100)
        print("*" * 100)
        target = test_Call_Tree.test_get_called_methods
        result = self.call_tree.get_called_methods(test_Call_Tree.test_get_called_methods)
        print()
        print(result)


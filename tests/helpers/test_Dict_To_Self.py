from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_utils.helpers.Dict_To_Attr import Dict_To_Attr


class test_Dict_To_Attr(TestCase):

    def test___Init__(self):
        source = {'item_1': 1, 'item_2': 2}
        target = Dict_To_Attr(source)
        assert target.item_1 == 1
        assert target.item_2 == 2
        assert hasattr(target, 'item_1') is True
        assert hasattr(target, 'item_2') is True
        assert hasattr(target, 'item_3') is False


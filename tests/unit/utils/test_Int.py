from unittest import TestCase

from osbot_utils.utils.Int import int_is_even


class test_Int(TestCase):

    def test_int_is_even(self):
        assert int_is_even(0) is True
        assert int_is_even(1) is False
        assert int_is_even(2) is True
        assert int_is_even(3) is False

    def test_int_is_odd(self):
        assert int_is_even(0) is True
        assert int_is_even(1) is False
        assert int_is_even(2) is True
        assert int_is_even(3) is False
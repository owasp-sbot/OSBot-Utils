import copy
from unittest import TestCase

from osbot_utils.decorators.methods.remove_return_value import remove_return_value


class test_remove_return_value(TestCase):

    def test_remove_return_value(self):
        data = {'a': 42, 'b': 123}
        def an_function_1():
            return data

        @remove_return_value('a')
        def an_function_2():
            return copy.copy(data)

        @remove_return_value('b')
        def an_function_3():
            return data

        assert an_function_1() == data
        assert an_function_2() == {'b': 123}
        assert an_function_3() == {'a': 42}

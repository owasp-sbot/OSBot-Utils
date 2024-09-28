from unittest                                       import TestCase
from osbot_utils.decorators.methods.obj_as_context  import obj_as_context

class test_obj_as_context(TestCase):

    def test_obj_as_context(self):
        with obj_as_context(42) as value:
            assert value == 42

        with obj_as_context('a string') as value:
            assert value == 'a string'
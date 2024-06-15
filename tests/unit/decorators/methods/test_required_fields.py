from unittest import TestCase

from osbot_utils.decorators.methods.required_fields import required_fields


class test_required_fields(TestCase):

    def test_required_fields(self):

        class An_Class:
            def __init__(self, a=None, b=None):
                self.a = a
                self.b = b

            @required_fields(['a'])
            def an_function(self):
                pass

        An_Class(a=1, b=123).an_function()
        An_Class(a=1).an_function()

        try:
            An_Class().an_function()
        except Exception as exception:
            assert str(exception) == "missing fields in an_function: ['a']"

        try:
            An_Class(b=123).an_function()
        except Exception as exception:
            assert str(exception) == "missing fields in an_function: ['a']"
from unittest                                   import TestCase
from osbot_utils.type_safe.Type_Safe            import Type_Safe
from osbot_utils.type_safe.decorators.type_safe import type_safe

class test__decorator__type_safe__bugs(TestCase):


    def test__bug__kwargs_not_properly_returned_in_type_safe(self):

        class Test_Class(Type_Safe):
            @type_safe
            def method_with_kwargs(self, name: str, **kwargs):          # The bug is caused by the non handling correctly of the **kwargs parameter
                return {"name": name, "kwargs": kwargs}                 # We expect kwargs to contain all extra parameters

        test_obj = Test_Class()
        with self.assertRaises(ValueError) as context:                  # This works as expected - type safety catches the error
            test_obj.method_with_kwargs(name=b'123')                    # Wrong type for 'name'

        assert str(context.exception) == "Parameter 'name' expected type <class 'str'>, but got <class 'bytes'>"

        result   = test_obj.method_with_kwargs(name="test", extra=True, another="value")
        expected = {"kwargs": {"extra": True, "another": "value"},
                    "name"  : "test",}
        current =  {'kwargs': { "kwargs": {"extra": True, "another": "value"}},             # # BUG: there is an extra kwargs added to the return value
                     "name" : "test",}

        assert result != expected  # BUG: This is what we expect
        assert result == current   # BUG: This is what we get




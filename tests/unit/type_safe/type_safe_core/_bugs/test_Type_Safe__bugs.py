import re
import pytest
from typing import Type, List
from unittest                                                         import TestCase
from osbot_utils.type_safe.Type_Safe                                  import Type_Safe


class test_Type_Safe__bugs(TestCase):


    def test__bug__property_descriptor_handling__doesnt_enforce_type_safety(self):

        class Test_Class(Type_Safe):
            def __init__(self):
                super().__init__()
                self._label = "initial_label"

            @property
            def label(self) -> str:
                return self._label

            @label.setter
            def label(self, value: str):
                self._label = value

            @property
            def label_bad_type(self) -> str:
                return 42


        test_obj = Test_Class()                                     # Create instance and try to use property
        test_obj.label = "new_label"                                # this works ok
        test_obj.label = 123                                        # BUG this should have raise a type safeting exception

        assert test_obj.label          == 123                       # BUG this should still be the string value
        assert test_obj.label_bad_type == 42                        # BUG only str should have been returned

        class An_Class(Type_Safe):                                  # this example confirms that we can still have type safety if we use a strongly typed inner var
            inner_label: str

            @property
            def label(self) -> str:
                return self.inner_label

            @label.setter
            def label(self, value: str):
                self.inner_label = value

        an_class = An_Class()
        an_class.label = 'str value'                                # works ok
        with pytest.raises(ValueError, match="On An_Class, invalid type for attribute 'inner_label'. Expected '<class 'str'>' but got '<class 'int'>'"):
            an_class.label = 42                                     # raised expected exception since int is not a str (this is not captured by the label, but by the inner_label)

    # todo: figure out why when this test was runs will all the others tests test_Type_Safe tests, it doesn't hit the lines in __setattr__ (as proven by the lack of code coverage)
    #       but then when run in isolation it does hit the lines in __setattr__
    def test__bug__setattr__with_no_annotations(self):

        # test scenario where: not hasattr(self, '__annotations__') == True
        class An_Class_2(Type_Safe):
            an_str = 'default_value'
            an_bool = None

            def __init__(self):                     # this will make the __annotations__ to not be available
                pass

        an_class = An_Class_2()

        an_class.__setattr__('an_str', 'new_value')
        an_class.__setattr__('an_bool', False)

        assert an_class.an_str == 'new_value'
        assert an_class.an_bool == False

    def test__bug__type_annotation__non_none_parent_default(self):
        # What happens when parent has a non-None default?
        # This combines BOTH bugs:
        # 1. Subclass inherits parent's value (Base_Handler) instead of auto-assigning Extended_Handler
        # 2. Then validation fails because Base_Handler is not a subclass of Extended_Handler

        class Base_Handler(Type_Safe):
            pass

        class Extended_Handler(Base_Handler):
            pass

        class Base_Config(Type_Safe):
            handler_type: Type[Base_Handler] = Base_Handler             # Non-None default

        class Extended_Config(Base_Config):
            handler_type: Type[Extended_Handler]                        # Re-declare with more specific type

        # Parent default is Base_Handler
        with Base_Config() as _:
            assert _.handler_type is Base_Handler                       # Correct

        # BUG: Subclass inherits parent's value (Base_Handler), then validation fails
        #      because Base_Handler is not a subclass of Extended_Handler
        error_message = "On Extended_Config, invalid type for attribute 'handler_type'. Expected 'typing.Type["
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Extended_Config()                                           # BUG: should auto-assign Extended_Handler
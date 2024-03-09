from typing import Optional, Union
from unittest import TestCase
from unittest.mock import patch

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.Misc                  import list_set
from osbot_utils.utils.Objects               import default_value


class test_Kwargs_To_Self__regression(TestCase):

    def test__regression__default_value_is_not_cached(self):                    # FIXED: this is a test that confirms a BUG the currently exists in the default_value method

        class An_Class(Kwargs_To_Self):
            test_case : TestCase
        with patch('osbot_utils.base_classes.Kwargs_To_Self.default_value') as patched_default_value:
            patched_default_value.side_effect = default_value                   # make sure that the main code uses the original method (i.e. not the patched one)
                                                                                #       since all we need is the ability to count how many times the method was called
            an_class = An_Class()                                               # create instance of class (which will call default_value via __default__kwargs__)
            assert patched_default_value.call_count == 1                        # expected result, since we used the default_value to create an instance of TestCase
            test_case = an_class.__locals__().get('test_case')                  # get a reference of that object (which (BUG) will also call default_value)
            assert test_case                         is not None                # make sure var that is set
            assert type(test_case)                   == TestCase                #       and that is the correct type
            assert patched_default_value.call_count  == 1 # was 2               # FIXED - BUG: we shouldn't see another call to default_value
            assert an_class.__locals__().get('test_case') is test_case          # confirm that although there was a call to default_value, it's value was not used
            assert patched_default_value.call_count  == 1 # was 3               # FIXED -BUG: again we should not see a call to default_value
            assert an_class.__locals__().get('test_case') is test_case          # just to double-check the behaviour/bug we are seeing
            assert patched_default_value.call_count  == 1 # was 4               # FIXED -BUG: this should be 1 (since we should only create the object once via default_value)
            assert default_value(TestCase).__class__ is TestCase                # confirm that a direct call to default_value does create an instance of TestCase
            assert default_value(TestCase)           is not test_case           # confirm that default_value object doesn't match the one we got originally
            assert TestCase()                        is not TestCase()          # double check that TestCase() creates a new object every time
            assert test_case                         is test_case               # confirm that the 'is' operator is the one correct one to check equality
            assert test_case                         == test_case               # confirm that we can't use == (i.e. __eq__) for equality
            assert TestCase()                        == TestCase()              #       since this should be False (i.e. two new instances of TestCase)

    def test__regression__type_safety_race_condition_on_overloaded_vars(self):

        class Base_Class                       :  pass                         # a base class
        class Implements_Base_Class(Base_Class): pass                          # is used as a base class here
        class An_Class(Kwargs_To_Self):                                        # now when a new class
            an_var: Base_Class                                                 # creates a var using the base class
        class Extends_An_Class(An_Class):                                      # and another class uses it has a base class
            an_var: Implements_Base_Class                                      # and changes the type to a compatible type
                                                                               #   we will get an exception, because Kwargs_To_Self creates
                                                                               #   a new object of type Base_Class when it should create
                                                                               #   a new object of type Implements_Base_Class

        Base_Class()                                                           # this works ok
        Implements_Base_Class()                                                # this works ok
        An_Class()                                                             # this works ok (with an_var = Base_Class() )
        Extends_An_Class()                                                     # FIXED: this works now (with an_var = Implements_Base_Class() )

        assert type(An_Class()        .an_var) is Base_Class                  # just confirming an_var is Base_Class
        assert type(Extends_An_Class().an_var) is Implements_Base_Class       # just confirming an_var is now Implements_Base_Class

        # with self.assertRaises(Exception) as context:                       # BUG: this now will fail
        #     Extends_An_Class()                                              # BUG: due to a bug in type safety logic Kwargs_To_Self
        #
        # assert str(context.exception) == ("Invalid type for attribute 'an_var'. Expected '<class 'test_Kwargs_To_Self.Test_Kwargs_To_Self.test__bug__type_safety_race_condition_on_overloaded_vars.<locals>."
        #                                     "Implements_Base_Class'>' "
        #                                  "but got '<class 'test_Kwargs_To_Self.Test_Kwargs_To_Self.test__bug__type_safety_race_condition_on_overloaded_vars.<locals>."
        #                                     "Base_Class'>'")

    def test__regression__type_safety_bug__in___cls_kwargs__(self):
        class Base_Class                           : pass                                  # set of classes that replicate the bug
        class Implements_Base_Class(Base_Class    ): pass                                  # which happens when we have a base class
        class An_Class             (Kwargs_To_Self): an_var: Base_Class                    # and a class that uses it as a var
        class Extends_An_Class     (An_Class      ):an_var: Implements_Base_Class          # and another class that extends it and changes the type

        an_class__cls_kwargs__         = An_Class        .__cls_kwargs__()                 # the bug in __cls_kwargs__() so lets get its output for both
        extends_an_class__cls_kwargs__ = Extends_An_Class.__cls_kwargs__()                 # An_Class and Extends_An_Class
        assert list_set(an_class__cls_kwargs__        )           == ['an_var']            # confirm that the only var created and assigned
        assert list_set(extends_an_class__cls_kwargs__)           == ['an_var']            # the 'an_var' one
        assert type(an_class__cls_kwargs__        .get('an_var')) == Base_Class            # this is ok since the an_var in An_Class should be Base_Class
        assert type(extends_an_class__cls_kwargs__.get('an_var')) == Implements_Base_Class # FIXED: BUG: since an_var in Extends_An_Class should be Implements_Base_Class





    def test__regression__cast_issue_with_base_class_mode_a(self):                   # note although this test is still showing the bug, the test__regression__cast_issue_with_base_class_mode_c shows the fix (which is why it has been changed to regression test)
        class Base_Class(Kwargs_To_Self):
            an_int : int = 42

        class Cast_Mode_A(Base_Class):
            an_str : str = 'abc'

            def cast(self, target):
                self.__dict__ = target.__dict__
                return self

        base_class = Base_Class()                                                    # create an object of Base_Class base class
        assert list_set(base_class.__kwargs__())  == ['an_int']                      # confirm that it has the expected vars
        assert base_class.an_int                  == 42                              # confirm that an_int was correct set via Kwargs_To_Self
        cast_mode_a = Cast_Mode_A()                                                  # create an object of Cast_Mode_A class
        assert list_set(cast_mode_a.__kwargs__()) == ['an_int', 'an_str']            # confirm that it has the vars from Base_Class and Cast_Mode_A
        assert cast_mode_a.an_int                 == 42                              # confirm that an_int was correctly set via Kwargs_To_Self
        assert cast_mode_a.an_str                 == 'abc'                           # confirm that an_str was correctly set via Kwargs_To_Self

        base_class.an_int                          = 123                             # now change the value of base_class.an_int
        assert base_class.an_int                  == 123                             # confirm it has been changed correctly
        cast_mode_a_from_base_class                = Cast_Mode_A().cast(base_class)  # now create a new object of Cast_Mode_A and cast it from base_class
        assert cast_mode_a_from_base_class.an_int == 123                             # confirm that an_int was the new object picked up the new value (via cast)

        cast_mode_a_from_base_class.an_int         = 456                             # now change the an_int on the new class
        assert cast_mode_a_from_base_class.an_int == 456                             # and confirm that the value has been changed correctly in the 'casted' object
        assert base_class.an_int                  == 456                             # and confirm that it also was changed in the original object (i.e. base_class)

        # the example above is the exact behaviour which replicates the 'cast' operation in other languages (i.e. C#), where
        #       cast_mode_a_from_base_class = Cast_Mode_A().cast(base_class)
        # is equivalent to
        #       cast_mode_a_from_base_class = (Cast_Mode_A) base_class
        assert cast_mode_a_from_base_class.an_str  == 'abc'
        cast_mode_a_from_base_class.new_str         = 'new_str'
        assert cast_mode_a_from_base_class.new_str == 'new_str'                      # confirm that the new var is set correctly
        assert base_class.new_str                  == 'new_str'                      # confirm that the new var is set correctly
        assert cast_mode_a_from_base_class.__dict__ == base_class.__dict__

        base_class_2  = Base_Class()                                                 # create a clean instance of Base_Class
        cast_mode_a_2 = Cast_Mode_A()                                                # create a clean instance of Cast_Mode_A
        assert list_set(base_class_2 .__dict__) == ['an_int']                        # confirm that it has the expected vars
        assert list_set(cast_mode_a_2.__dict__) == ['an_int', 'an_str']              # confirm that it has the vars from Base_Class and Cast_Mode_A
        cast_mode_a_2.cast(base_class_2)                                             # cast it from base_class_2
        assert list_set(base_class_2.__dict__ ) == ['an_int']                        # re-config that base_class_2 only has the one var
        assert list_set(cast_mode_a_2.__dict__) == ['an_int']                        # BUG: but now cast_mode_a_2 lost the an_str var
        assert cast_mode_a_2.an_str             == 'abc'                             # works because an_str is defined in the Cast_Mode_A class, it's still accessible by instances of that class, even if it's not in their instance __dict__.

        cast_mode_a_3 = Cast_Mode_A()
        cast_mode_a_3.an_str = 'changed'
        assert cast_mode_a_3.an_str == 'changed'
        cast_mode_a_3.cast(base_class_2)
        assert cast_mode_a_3.an_str == 'abc'

    def test__regression__cast_issue_with_base_class_mode_b(self):                         # note although this test is still showing the bug, the test__regression__cast_issue_with_base_class_mode_c shows the fix (which is why it has been changed to regression test)
        class Base_Class(Kwargs_To_Self):
            an_int : int = 42

        class Cast_Mode_B(Base_Class):
            an_str : str = 'abc'

            def cast(self, target):
                for key, value in target.__dict__.items():
                    setattr(self, key, value)
                return self

        base_class  = Base_Class()                                                  # create a new instance of Base_Class

        base_class.an_int = 222
        cast_mode_b = Cast_Mode_B().cast(base_class)                                # 'cast' that Base_Class object into a Cast_Mode_B object

        assert list_set(base_class.__kwargs__())  == ['an_int']                     # Base_Class correctly still only has one var
        assert list_set(cast_mode_b.__kwargs__()) == ['an_int', 'an_str']           # Cast_Mode_B correctly has both vars
        assert base_class.an_int                  == 222                            # confirm that an_int was correctly set via Kwargs_To_Self
        assert cast_mode_b.an_int                 == 222                            # confirm that the value was correctly set via cast
        cast_mode_b.an_int = 123                                                    # now modify the an_int value in the Cast_Mode_B object
        assert cast_mode_b.an_int                 == 123                            # confirm that the value was correctly set in the Cast_Mode_B object
        assert base_class.an_int                  == 222                            # BUG: but the value in the Base_Class object was not changed!

        base_class.an_int = 456                                                     # now modify the an_int value in the Base_Class object
        assert base_class.an_int                  == 456                            # confirm that the value was correctly set in the Base_Class object
        assert cast_mode_b.an_int                 == 123                            # BUG: but the value in the Cast_Mode_B object was not changed!

        # the current hypothesis is that the current cast code
        #                  for key, value in target.__dict__.items():
        #                     setattr(self, key, value)
        # is actually creating a copy of the an_int object, instead of a reference to it (which is what we want)


    def test__regression__cast_issue_with_base_class_mode_c(self):                  # the cast version below is the one that has the correct behaviour
        class Base_Class(Kwargs_To_Self):
            an_int : int = 42

        class Cast_Mode_C(Base_Class):
            an_str : str = 'abc'

            def cast(self, target):
                original_attrs = {k: v for k, v in self.__dict__.items() if k not in target.__dict__}       # Store the original attributes of self that should be retained.
                self.__dict__ = target.__dict__                                                             # Set the target's __dict__ to self, now self and target share the same __dict__.
                self.__dict__.update(original_attrs)                                                        # Reassign the original attributes back to self.
                return self



        base_class  = Base_Class()                                                  # create a new instance of Base_Class

        base_class.an_int = 222
        cast_mode_c = Cast_Mode_C().cast(base_class)                                # 'cast' that Base_Class object into a Cast_Mode_B object

        assert list_set(base_class.__kwargs__())  == ['an_int']                     # Base_Class correctly still only has one var
        assert list_set(cast_mode_c.__kwargs__()) == ['an_int', 'an_str']           # Cast_Mode_B correctly has both vars
        assert base_class.an_int                  == 222                            # confirm that an_int was correctly set via Kwargs_To_Self
        assert cast_mode_c.an_int                 == 222                            # confirm that the value was correctly set via cast
        cast_mode_c.an_int = 123                                                    # now modify the an_int value in the Cast_Mode_B object
        assert cast_mode_c.an_int                 == 123                            # confirm that the value was correctly set in the Cast_Mode_B object
        assert base_class.an_int                  == 123                            # FIXED :BUG: but the value in the Base_Class object was not changed!

        base_class.an_int = 456                                                     # now modify the an_int value in the Base_Class object
        assert base_class.an_int                  == 456                            # confirm that the value was correctly set in the Base_Class object
        assert cast_mode_c.an_int                 == 456                            # FIXED: BUG: but the value in the Cast_Mode_B object was not changed!

    def test__regression__check_type_safety_assignments__on_obj__union(self):
        class An_Class(Kwargs_To_Self):
            an_bool    : Optional[bool            ]
            an_int     : Optional[int             ]
            an_str     : Optional[str             ]
            an_bool_int: Optional[Union[bool, int]]
            an_bool_str: Optional[Union[bool, str]]

        an_bytes_value = b'an_bytes_value'
        an_class       = An_Class()

        def asserts_exception(var_name, var_value, expected_type, got_type):
            with self.assertRaises(Exception) as context:
                an_class.__setattr__(var_name, var_value)
            expected_message = f"Invalid type for attribute '{var_name}'. Expected '{expected_type}' but got '<class '{got_type}'>'"
            assert context.exception.args[0] == expected_message

        asserts_exception('an_bool'     , an_bytes_value, 'typing.Optional[bool]'            , 'bytes')
        asserts_exception('an_int'      , an_bytes_value, 'typing.Optional[int]'             , 'bytes')
        asserts_exception('an_str'      , an_bytes_value, 'typing.Optional[str]'             , 'bytes')
        asserts_exception('an_bool_int' , an_bytes_value, 'typing.Union[bool, int, NoneType]', 'bytes')
        asserts_exception('an_bool_str' , an_bytes_value, 'typing.Union[bool, str, NoneType]', 'bytes')
        asserts_exception('an_bool_int' , an_bytes_value, 'typing.Union[bool, int, NoneType]', 'bytes')
        asserts_exception('an_bool_str' , an_bytes_value, 'typing.Union[bool, str, NoneType]', 'bytes')

        # below is the code that was passing before the fix
        # an_class.an_bool     = an_bytes_value                                   # FIXED: was BUG: none of these should work
        # an_class.an_int      = an_bytes_value                                   # FIXED: was BUG:   since none the types above have bytes
        # an_class.an_str      = an_bytes_value                                   # FIXED: was BUG:   i.e. we are allowing an incorrect assigment
        # an_class.an_bool_int = an_bytes_value
        # an_class.an_bool_str = an_bytes_value
        # an_class.an_bool_int = an_bytes_value
        # an_class.an_bool_str = an_bytes_value
        #
        # assert an_class.__locals__() == {'an_bool'    : an_bytes_value, 'an_bool_int': an_bytes_value,   # BUG confirm incorrect values assignment
        #                                  'an_bool_str': an_bytes_value, 'an_int'     : an_bytes_value,
        #                                  'an_str'     : an_bytes_value                                }



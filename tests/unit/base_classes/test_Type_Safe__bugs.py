from typing import Optional, Union
from unittest import TestCase

import pytest
from osbot_utils.base_classes.Type_Safe import Type_Safe

from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.utils.Dev import pprint


class test_Type_Safe__bugs(TestCase):

    def test__bug__check_type_safety_assignments__on_ctor(self):
        an_bool_value = True
        an_int_value  = 42
        an_str_value  = 'an_str_value'

        class An_Class__With_Correct_Values(Kwargs_To_Self):
            an_bool : bool = an_bool_value
            an_int  : int = an_int_value
            an_str  : str = an_str_value

        class An_Class__With_Bad_Values(Kwargs_To_Self):
            an_bool : bool = an_bool_value
            an_int  : int  = an_bool_value                      # BUG: should have thrown exception here
            an_str  : str  = an_bool_value                      # will throw exception here


        an_class =  An_Class__With_Correct_Values()             # should create ok and values should match the type
        assert an_class.__locals__() == {'an_bool': an_bool_value, 'an_int': an_int_value, 'an_str': an_str_value}

        expected_message = "variable 'an_str' is defined as type '<class 'str'>' but has value 'True' of type '<class 'bool'>'"
        with self.assertRaises(Exception) as context:
            An_Class__With_Bad_Values()
        assert context.exception.args[0] == expected_message

    def test__bug__check_type_safety_assignments____on_ctor__union(self):
        if not hasattr(self, '__annotations__'):
            pytest.skip('skipping test since __annotations__ is not available')

        an_bool_value = True
        an_int_value  = 42
        an_str_value  = 'an_str_value'

        class An_Class__With_Correct_Values(Kwargs_To_Self):
            an_bool     : Optional[bool            ] = an_bool_value
            an_int      : Optional[int             ] = an_int_value
            an_str      : Optional[str             ] = an_str_value
            an_bool_none: Optional[bool            ] = None
            an_int_none : Optional[int             ] = None
            an_str_none : Optional[str             ] = None
            an_bool_int : Optional[Union[bool, int]] = an_bool_value
            an_str_int  : Optional[Union[str , int]] = an_str_value
            an_int_bool : Optional[Union[bool, int]] = an_int_value
            an_int_str  : Optional[Union[str , int]] = an_int_value

        an_class = An_Class__With_Correct_Values()
        assert an_class.__locals__() == { 'an_bool': an_bool_value, 'an_bool_int': True        , 'an_bool_none': None ,
                                          'an_int': an_int_value  , 'an_int_bool': an_int_value,'an_int_none' : None , 'an_int_str': an_int_value,
                                          'an_str': an_str_value  , 'an_str_int': an_str_value, 'an_str_none' : None }

        class An_Class__With_Bad_Values(Kwargs_To_Self):
            an_bool : bool = an_bool_value
            an_int  : int  = an_bool_value                      # BUG: should have thrown exception here (bool should be allowed on int)
            an_str  : str  = an_bool_value                      # will throw exception here

        expected_message = "variable 'an_str' is defined as type '<class 'str'>' but has value 'True' of type '<class 'bool'>'"
        with self.assertRaises(Exception) as context:
            An_Class__With_Bad_Values()
        assert context.exception.args[0] == expected_message

    def test__bug__type_safety_assignments__on_obj__bool_assigned_to_int(self):
        an_bool_value = True
        an_int_value  = 42
        an_str_value  = 'an_str_value'

        class An_Class(Kwargs_To_Self):
            an_bool : bool
            an_int  : int
            an_str  : str

        an_class = An_Class()
        assert an_class.__locals__() == {'an_bool': False, 'an_int': 0, 'an_str': ''}       # confirm default values assignment

        an_class.an_bool = an_bool_value                                                    # these should all work
        an_class.an_int  = an_int_value                                                     # since we are doing the correct type assigment
        an_class.an_str  = an_str_value

        def asserts_exception(var_name, var_value, expected_type, got_type):
            with self.assertRaises(Exception) as context:
                an_class.__setattr__(var_name, var_value)
            expected_message = f"Invalid type for attribute '{var_name}'. Expected '<class '{expected_type}'>' but got '<class '{got_type}'>'"
            assert context.exception.args[0] == expected_message

        asserts_exception('an_bool',an_str_value , 'bool', 'str' )
        asserts_exception('an_bool',an_int_value , 'bool', 'int' )
        asserts_exception('an_str' ,an_bool_value, 'str' , 'bool')
        asserts_exception('an_str' ,an_int_value , 'str' , 'int' )
        asserts_exception('an_int' ,an_str_value , 'int' , 'str' )
        #asserts_exception('an_int' ,an_bool_value , 'int' , 'bool' )                     # BUG: should have raised exception
        an_class.an_int = an_bool_value                                                   # BUG  should have raised exception

    def test__bug__check_type_safety_assignments__allows_bool_to_int(self):
        an_bool_value = True                                        # this is a bool

        class Should_Raise_Exception(Type_Safe):                     # a class that uses Kwargs_To_Self as a base class
            an_int: int = an_bool_value                             # BUG : the an_int variable is defined as an int, but it is assigned a bool

        should_raise_exception = Should_Raise_Exception()                                   # BUG an exception should have been raised
        assert should_raise_exception.__locals__()    == {'an_int': an_bool_value}          # BUG confirming that an_int is a bool
        assert should_raise_exception.an_int          is True                               # BUG in this case the value True
        assert type(an_bool_value                )    is bool                               # confirm an_bool_value is a bool
        assert type(should_raise_exception.an_int)    is bool                               # BUG:  confirming that an_int is a bool
        assert should_raise_exception.__annotations__ == {'an_int': int }                   # confirm that the an_int annotation is int


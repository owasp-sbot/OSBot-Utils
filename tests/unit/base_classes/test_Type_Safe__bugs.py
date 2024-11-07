import pytest
from typing                                     import Optional, Union, Dict
from unittest                                   import TestCase
from osbot_utils.base_classes.Type_Safe         import Type_Safe
from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.helpers.Random_Guid            import Random_Guid


class test_Type_Safe__bugs(TestCase):

    def test__bug__nested_dict_serialisations_dont_work(self):
        class An_Class_1(Type_Safe):
            dict_5: Dict[Random_Guid, dict[Random_Guid, Random_Guid]]
        json_data_1 = { 'dict_5': {Random_Guid(): { Random_Guid():Random_Guid(),
                                                    Random_Guid():Random_Guid(),
                                                    'no-guid-1': 'no-guid-2'}}}
        assert An_Class_1().from_json(json_data_1).json() == json_data_1  # BUG: should had raised exception on 'no-guid-1': 'no-guid-2'



    def test__bug__ctor__does_not_recreate__Dict__objects(self):

        class An_Class_1(Type_Safe):
            an_dict : Dict[str,int]

        json_data_1 = {'an_dict': {'key_1': 42}}
        an_class_1 = An_Class_1.from_json(json_data_1)

        assert type(an_class_1.an_dict) is dict
        assert an_class_1.an_dict == {'key_1': 42}

        class An_Class_2_B(Type_Safe):
            an_str: str

        class An_Class_2_A(Type_Safe):
            an_dict      : Dict[str,An_Class_2_B]
            an_class_2_b : An_Class_2_B

        json_data_2 = {'an_dict'     : {'key_1': {'an_str': 'value_1'}},
                       'an_class_2_b': {'an_str': 'value_1'}}
        print()
        an_class_2  = An_Class_2_A.from_json(json_data_2)

        assert an_class_2.json() == json_data_2
        assert type(an_class_2.an_dict                          ) is dict

        assert type(an_class_2.an_dict['key_1']                 ) is An_Class_2_B       # Fixed: BUG: this should be An_Class_2_B not an dict

        # todo fix the scenario where we try to create a new object from a dict value using the ctor instead of the from_json method
        assert type(An_Class_2_A(**json_data_2).an_dict['key_1']) is dict               # BUG: this should be An_Class_2_B
        assert type(An_Class_2_A(**json_data_2).an_class_2_b    ) is An_Class_2_B       # when not using Dict[str,An_Class_2_B] the object is created correctly




    # todo: figure out why when this test was runs will all the others tests test_Type_Safe tests, it doesn't hit the lines in __setattr__ (as proven by the lack of code coverage)
    #       but then when run in isolation it does hit the lines in __setattr__
    def test__bug__setattr___with_no_annotations(self):

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

    def test__bug__type_safe_is_not_enforced_on_dict_and_Dict(self):
        class An_Class(Type_Safe):
            an_dict : Dict[str,int]

        an_class = An_Class()

        assert An_Class.__annotations__ == {'an_dict': Dict[str, int]}
        assert an_class.__locals__() == {'an_dict': {}}
        assert type(an_class.an_dict) is dict               # BUG: this should be Type_Safe__Dict # todo: see if there is a better way to do this, without needing to replace the Dict object with Type_Safe__Dict (although this technique worked ok for Type_Safe__List)
        an_class.an_dict[42] = 'an_str'                     # BUG: this should not be allowed
                                                            #       - using key 42 should have raised exception (it is an int instead of a str)
                                                            #       - using value 'an_str' should have raised exception (it is a str instead of an int)






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


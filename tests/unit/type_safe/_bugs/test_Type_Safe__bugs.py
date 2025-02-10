import sys
import pytest
from typing                                             import Optional, Union, Dict
from unittest                                           import TestCase
from osbot_utils.type_safe.Type_Safe                    import Type_Safe
from osbot_utils.base_classes.Kwargs_To_Self            import Kwargs_To_Self
from osbot_utils.type_safe.Type_Safe__Dict              import Type_Safe__Dict
from osbot_utils.type_safe.shared.Type_Safe__Convert    import type_safe_convert


class test_Type_Safe__bugs(TestCase):

    def test__bug__roundtrip_tuple_support(self):
        class Inner_Data(Type_Safe):
            tuple_1  : tuple[str, str]
            node_ids: Dict[str, tuple[str, str]]
            edge_ids: Dict[str, set[str]]

        class An_Class(Type_Safe):
            data: Inner_Data

        an_class = An_Class()
        an_class.data = Inner_Data()
        an_class.data.node_ids = {"a": ("id1", "id2")}
        an_class.data.edge_ids = {"b": {"id3"}}
        an_class.data.tuple_1  = ("id1", "id2")

        expected_error = "In tuple at index 0: Expected 'str', but got 'int'"
        with pytest.raises(TypeError, match=expected_error):
            an_class.data.node_ids = {"b": (123, '123')}                    # confirm type safety in tuples
        # with pytest.raises(TypeError, match=expected_error):
        #     an_class.data.tuple_1 = (123, '123')                          # BUG should have raised

        assert type(an_class.data.tuple_1) is tuple                         # BUG this should be Type_Safe__Tuple
        an_class.data.tuple_1 = (123, '123')                                     # BUG should have raised
        assert type(an_class.data.tuple_1) is tuple

        assert type(an_class.data.node_ids) is Type_Safe__Dict              # this should not be a dict
        assert type(an_class.data.edge_ids) is Type_Safe__Dict              # correct this should be a dict


        # expected_error = "Type <class 'tuple'> not serializable"
        # with pytest.raises(TypeError, match=expected_error):                # BUG, should have worked
        #     an_class.json()
        assert an_class.json() == {'data': {'edge_ids': {'b': ['id3']},
                                            'node_ids': {'a': ['id1', 'id2']},
                                            'tuple_1': [123, '123']}}       # BUG: this should have not happened

        roundtrip_obj = An_Class.from_json(an_class.json())

        assert roundtrip_obj.json()             == an_class.json()
        assert roundtrip_obj.data.node_ids      == {"a": ("id1", "id2")}
        assert roundtrip_obj.data.edge_ids      == {"b": {"id3"}}
        assert roundtrip_obj.data.tuple_1       == (123, "123")
        assert type(roundtrip_obj.data.tuple_1) is tuple


        # These assertions will help verify the fix once implemented
        # assert json_data == {'data': {'node_ids': {'a': ['id1', 'id2']},
        #                              'edge_ids': {'b': ['id3', 'id4']}}}
        #
        # an_class_round_trip = An_Class.from_json(json_data)
        # assert type(an_class_round_trip.data.node_ids['a']) is tuple
        # assert type(an_class_round_trip.data.edge_ids['b']) is Type_Safe__Set
        # assert an_class_round_trip.data.node_ids['a'] == ('id1', 'id2')
        # assert an_class_round_trip.data.edge_ids['b'] == {'id3', 'id4'}
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
        with pytest.raises(ValueError, match="Invalid type for attribute 'inner_label'. Expected '<class 'str'>' but got '<class 'int'>'"):
            an_class.label = 42                                     # raised expected exception since int is not a str (this is not captured by the label, but by the inner_label)



    def test__bug__type_annotation_json_serialization__roundtrip(self):
        from typing import Type

        class Parent_Class(Type_Safe):
            class_type: Type[int]

        class Child_Class(Parent_Class):
            an_type: Type[int]

        Parent_Class.from_json(Parent_Class().json())

        # current working workflows
        assert Parent_Class().json() == {'class_type': 'builtins.int'                           }  # Create instance and serialize to JSON
        assert Child_Class ().json() == {'an_type': 'builtins.int', 'class_type': 'builtins.int'}  # Create instance and serialize to JSON
        assert Parent_Class().json() == Parent_Class.from_json(Parent_Class().json()).json()       # Round trip of Parent_Class works

        # current buggy workflow
        # with pytest.raises(ValueError, match=re.escape("Invalid type for attribute 'class_type'. Expected 'typing.Type[int]' but got '<class 'str'>'")):
        #     assert Child_Class .from_json(Child_Class().json())                                 # BUG should not have raised an exception

        assert Child_Class.from_json(Child_Class().json()).json() == Child_Class().json()        # Fixed : works now :BUG this should work














    def test__bug__in__convert_dict_to_value_from_obj_annotation(self):
        class An_Class_2_B(Type_Safe):
            an_str: str

        class An_Class_2_A(Type_Safe):
            an_dict      : Dict[str,An_Class_2_B]

        an_class = An_Class_2_A()

        target    = an_class
        attr_name = 'an_dict'
        value    = {'key_1': {'an_str': 'value_1'}}
        converted_value = type_safe_convert.convert_dict_to_value_from_obj_annotation(target, attr_name, value)

        assert converted_value == value
        assert type(converted_value['key_1']) is dict             # BUG: this should be An_Class_2_B


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




    def test__bug__check_type_safety_assignments__on_ctor__on_bool_to_int_conversion(self):
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

        expected_message = "Invalid type for attribute 'an_str'. Expected '<class 'str'>' but got '<class 'bool'>'"
        with self.assertRaises(Exception) as context:
            An_Class__With_Bad_Values()
        assert context.exception.args[0] == expected_message

    def test__bug__check_type_safety_assignments____on_ctor__union(self):
        if sys.version_info < (3, 10):
            pytest.skip("Skipping test that doesn't work on 3.9 or lower")
        # if not hasattr(self, '__annotations__'):
        #     pytest.skip('skipping test since __annotations__ is not available')

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

        expected_message = "Invalid type for attribute 'an_str'. Expected '<class 'str'>' but got '<class 'bool'>'"
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


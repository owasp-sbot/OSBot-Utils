import pytest
import sys
from decimal                                        import Decimal
from typing                                         import Optional, Union, List
from unittest                                       import TestCase
from unittest.mock                                  import patch
from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.base_classes.Type_Safe             import Type_Safe
from osbot_utils.base_classes.Type_Safe__List       import Type_Safe__List
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.graphs.mermaid.Mermaid             import Mermaid
from osbot_utils.graphs.mermaid.Mermaid__Graph      import Mermaid__Graph
from osbot_utils.graphs.mermaid.Mermaid__Node       import Mermaid__Node
from osbot_utils.graphs.mgraph.MGraph__Node         import MGraph__Node
from osbot_utils.helpers.Random_Guid                import Random_Guid
from osbot_utils.utils.Json                         import json_to_str, str_to_json
from osbot_utils.utils.Misc                         import list_set, is_guid
from osbot_utils.utils.Objects                      import default_value, obj_attribute_annotation, __


class test_Type_Safe__regression(TestCase):

    def test__regression__from_json__allows_new_fields(self):
        class An_Class(Type_Safe):
            an_str: str

        json_data_1 = {'an_str': 'value_2'}
        assert An_Class.from_json(json_data_1).json() == json_data_1

        json_data_2 = {'an_str': 'value_2', 'new_field': 'new_value'}
        with pytest.raises(ValueError) as exception:
            An_Class.from_json(json_data_2).json()        # Fixed:   BUG: should have raised exception because of new_field
        assert exception.value.args[0] == "Attribute 'new_field' not found in 'An_Class'"

    def test__regression___classes_with_str_base_class_dont_round_trip(self):
        class An_Class(Type_Safe):
            an_str      : str = '42'
            random_guid : Random_Guid

        an_class                           = An_Class()
        an_class_obj                       = an_class.obj()
        an_class__via_from_json            = An_Class.from_json(an_class.json())        # works
        an_class__via_ctor                 = An_Class(**an_class.json())                # works
        an_class__via_set_attr             = An_Class()                                 # works
        an_class__via_set_attr.an_str      = an_class.json().get('an_str'     )


        assert an_class__via_from_json.obj() == an_class_obj
        assert an_class               .obj() == an_class_obj
        assert an_class__via_ctor     .obj() == an_class_obj

        class An_Class__using__None(Type_Safe):
            an_str      : str           = None
            random_guid : Random_Guid   = None

        an_class_using_none               = An_Class__using__None.from_json(an_class.json())  # works
        assert an_class_using_none.obj() == an_class_obj


        # these are the exceptions that should happen when we try to assign non GUID value

        bad_guids = ['aaaa'                                 ,  # clearly not a guid :)
                     '1e1a9d4d-cc16-4c59-a593-1f1fcaabebd'  ,  # missing one value at the end
                     'Ge1a9d4d-cc16-4c59-a593-1f1fcaabebdb' ,  # has a G at the start (GUID should only be A-G and 0-9)
                     '1e1a9d4d-cc16-4c59-a593-1f1fcaabebdb1' ,  # has extra char at the end
                     ]
        for bad_guid in bad_guids:
            expected_error = f"in Random_Guid: value provided was not a Guid: {bad_guid}"
            with pytest.raises(ValueError,match=expected_error):
                an_class.random_guid = bad_guid


        # FIXED: these statements now don't throw an exception and assign the correct values

        # use case 1: assign the str representation of an_class.random_guid
        assert is_guid(an_class__via_set_attr.random_guid) is True
        an_class__via_set_attr.random_guid = "1e1a9d4d-cc16-4c59-a593-1f1fcaabebdb"
        assert an_class__via_set_attr .obj() == __(an_str='42', random_guid='1e1a9d4d-cc16-4c59-a593-1f1fcaabebdb')

        # assert an_class_using_none__via_set_attr.obj() == an_class_obj
        # use case 2:  assign the str representation of an_class.random_guid
        assert is_guid(an_class__via_set_attr.random_guid) is True
        an_class__via_set_attr.random_guid = str.__str__((an_class.json().get('random_guid')))
        assert an_class__via_set_attr.obj() == an_class_obj

        # use-case 3: assign the guid when there is a null value
        an_class_using_none__via_set_attr = An_Class__using__None()
        assert an_class_using_none__via_set_attr.random_guid is None
        an_class_using_none__via_set_attr.random_guid = "1e1a9d4d-cc16-4c59-a593-1f1fcaabebdb"
        assert an_class_using_none__via_set_attr.obj() == __(an_str=None, random_guid='1e1a9d4d-cc16-4c59-a593-1f1fcaabebdb')

        # FIXED: below are the tests that were failing when the bug existed
        # #BUG: these three use cases fail the assigment of a valid GUID into the random_guid attribute
        #
        # # use-case 1: assign a valid GUID to the random_guid attribute
        # with pytest.raises(ValueError, match="Invalid type for attribute 'random_guid'. Expected '<class 'osbot_utils.helpers.Random_Guid.Random_Guid'>' but got '<class 'str'>'"):
        #     assert is_guid(an_class__via_set_attr.random_guid) is True
        #     an_class__via_set_attr.random_guid = "1e1a9d4d-cc16-4c59-a593-1f1fcaabebdb"
        #
        # # use-case 2: assign the str representation of an_class.random_guid
        # with pytest.raises(ValueError, match="Invalid type for attribute 'random_guid'. Expected '<class 'osbot_utils.helpers.Random_Guid.Random_Guid'>' but got '<class 'str'>'"):
        #     assert is_guid(an_class__via_set_attr.random_guid) is True
        #     an_class__via_set_attr.random_guid = str.__str__((an_class.json().get('random_guid')))
        #
        # # use-case 3: assign the guid when there is a null value
        # an_class_using_none__via_set_attr = An_Class__using__None()
        # with pytest.raises(ValueError, match="Invalid type for attribute 'random_guid'. Expected '<class 'osbot_utils.helpers.Random_Guid.Random_Guid'>' but got '<class 'str'>'"):
        #     assert an_class_using_none__via_set_attr.random_guid is None
        #     an_class_using_none__via_set_attr.random_guid =  "1e1a9d4d-cc16-4c59-a593-1f1fcaabebdb"

        # assert an_class__via_set_attr .obj() == an_class_obj
        # assert an_class_using_none__via_set_attr.obj() == an_class_obj


        #assert type(str(an_class.json().get('random_guid')))



    def test_regression_base_class_attributes_set_to_null_when_super_is_used(self):

        if sys.version_info < (3, 9):
            pytest.skip("Skipping test that doesn't work on 3.8 or lower")

        class Base_Class(Kwargs_To_Self):
            an_int : int
            an_str : str

            def __init__(self):
                self.an_int = 42
                self.an_str = '42'
                super().__init__()

        class An_Class(Base_Class):
            an_int : int
            an_str : str

            def __init__(self):
                super().__init__()
                self.an_int = 43


        an_class   = An_Class()
        base_class = Base_Class()

        assert an_class.__dict__       == {'an_int': 43, 'an_str': '42' }       # FIXED: BUG lost value assigned in Base_Class
        assert an_class.__locals__()   == {'an_int': 43, 'an_str': '42' }       # FIXED: BUG lost value assigned in Base_Class
        assert base_class.__dict__     == {'an_int': 42, 'an_str': '42' }       # FIXED: BUG lost value assigned in Base_Class
        assert base_class.__locals__() == {'an_int': 42, 'an_str': '42' }       # FIXED: BUG lost value assigned in Base_Class

    def test__regression__default_value_is_not_cached(self):                    # FIXED: this is a test that confirms a BUG the currently exists in the default_value method

        class An_Class(Kwargs_To_Self):
            test_case : TestCase
        with patch('osbot_utils.base_classes.Type_Safe.default_value') as patched_default_value:
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

        if sys.version_info < (3, 9):
            pytest.skip("Skipping test that doesn't work on 3.8 or lower")

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

    def test__regression__check_type_safety_assignments__on_list(self):
        if sys.version_info < (3, 9):
            pytest.skip("Skipping test that needs FIXING on 3.8 or lower")

        class An_Class(Kwargs_To_Self):
            an_str     : str
            an_str_list: list[str]
            an_int_list: list[int]

        an_class = An_Class()

        def asserts_exception(var_name, var_value, expected_type, got_type):
            with self.assertRaises(Exception) as context:
                an_class.__setattr__(var_name, var_value)
            expected_message = (f"Invalid type for attribute '{var_name}'. Expected '<class '{expected_type}'>' "
                                f"but got '<class '{got_type}'>'")
            assert context.exception.args[0] == expected_message

        asserts_exception('an_str', 42, 'str','int')

        an_class.an_str_list.append('should work')
        an_class.an_int_list.append(42            )

        with self.assertRaises(Exception) as context:
            an_class.an_str_list.append(42)                                 # FIXED was: BUG should have not worked
        assert context.exception.args[0] == "In Type_Safe__List: Invalid type for item: Expected 'str', but got 'int'"

        with self.assertRaises(Exception) as context:
            an_class.an_int_list.append('should not work')                  # FIXED was: BUG should have not worked
        assert context.exception.args[0] == "In Type_Safe__List: Invalid type for item: Expected 'int', but got 'str'"


    def test__regression__mermaid__list_allows_wrong_type(self):
        mermaid_graph = Mermaid__Graph()
        mermaid_node  = Mermaid__Node()
        graph_nodes   = mermaid_graph.nodes
        bad_node      = 'an str'

        assert obj_attribute_annotation(mermaid_graph, 'nodes') == List[Mermaid__Node]       # confirm nodes is list[Mermaid__Node]
        #assert type(graph_nodes) is list                                                              # FIXED was BUG: confirm that we lose type in graph_nodes
        assert type(graph_nodes) is Type_Safe__List                                                    # FIXED now graph_nodes is a typed list
        assert repr(graph_nodes) == 'list[Mermaid__Node] with 0 elements'                              # FIXED confirm graph_nodes is list[Mermaid__Node]

        mermaid_graph.nodes.append(mermaid_node)                                        # adding Mermaid__Node directly
        graph_nodes        .append(mermaid_node)                                        # which should be appended ok
        assert graph_nodes == mermaid_graph.nodes == [mermaid_node, mermaid_node]       # and should be in list[Mermaid__Node] nodes var

        with self.assertRaises(Exception) as context_1:
            mermaid_graph.nodes.append(bad_node)                                        # FIXED was BUG: type issue
        with self.assertRaises(Exception) as context_2:
            mermaid_graph.nodes.append(1)                                               # FIXED was BUG: str and ints
        with self.assertRaises(Exception) as context_3:
            graph_nodes        .append(bad_node)                                        # FIXED was BUG: are not of type Mermaid__Node
        with self.assertRaises(Exception) as context_4:
            graph_nodes        .append(2)                                               # FIXED was BUG: and break nodes type safety list[Mermaid__Node]

        #assert graph_nodes == [mermaid_node, mermaid_node, bad_node, 1, bad_node, 2]   # FIXED was BUG: graph_nodes should not have the bad values
        assert graph_nodes == mermaid_graph.nodes == [mermaid_node, mermaid_node]       # FIXED bad values have not been added to graph_nodes

        exception_template = "In Type_Safe__List: Invalid type for item: Expected 'Mermaid__Node', but got '{type_name}'"
        assert context_1.exception.args[0] == exception_template.format(type_name='str')
        assert context_2.exception.args[0] == exception_template.format(type_name='int')
        assert context_3.exception.args[0] == exception_template.format(type_name='str')
        assert context_4.exception.args[0] == exception_template.format(type_name='int')

    def test__regression__mermaid__cast_issue_with_base_class__with_new_vars(self):

        new_node_1 = Mermaid().add_node(key='id')
        assert list_set(new_node_1.__kwargs__()) == ['attributes', 'config', 'key', 'label']
        assert type(new_node_1).__name__ == 'Mermaid__Node'

        new_node_2 = Mermaid().add_node(key='id')
        assert type(new_node_2).__name__ == 'Mermaid__Node'

        assert list_set(new_node_2.__dict__         ) == ['attributes', 'config', 'key', 'label']

        mermaid_node = Mermaid__Graph().add_node(key='id')
        assert type(mermaid_node).__name__ == 'Mermaid__Node'
        assert list_set(mermaid_node.__dict__) == ['attributes', 'config', 'key', 'label']

        mgraph_node = MGraph__Node(key='id')
        assert type(mgraph_node).__name__ == 'MGraph__Node'
        new_mermaid_node = Mermaid__Node()
        assert list_set(mgraph_node.__dict__     ) == ['attributes', 'key'   , 'label'       ]
        assert list_set(new_mermaid_node.__dict__) == ['attributes', 'config', 'key', 'label']

        new_mermaid_node.merge_with(mgraph_node)
        assert list_set(new_mermaid_node.__dict__) == ['attributes', 'config', 'key', 'label'          ]

    def test__regression__ctor_doest_allow_none_values(self):
        class An_Class(Kwargs_To_Self):
            an_int  : list
            an_list : list
            an_str  : str
        assert An_Class().__locals__() == {'an_int': [], 'an_list': [], 'an_str': ''}

        class An_Class(Kwargs_To_Self):
            an_int  : int  = None                                       # BUG: will raise exception
            an_str  : str  = None                                       # BUG: will raise exception
            an_list : list = None  # BUG: will raise exception

        an_class = An_Class()
        assert an_class.__locals__() == {'an_int': None, 'an_list': None, 'an_str': None}

        an_class.an_int  = 42                               # confirm that normal assignments are still ok
        an_class.an_str  = '42'
        an_class.an_list = [42, '42']
        assert an_class.__locals__() == {'an_int': 42, 'an_list': [42, '42'], 'an_str': '42'}

        with self.assertRaises(Exception) as context:       # confirm that type safety checks are still in place
            an_class.an_list = 'a'
        assert context.exception.args[0] == ("Invalid type for attribute 'an_list'. "
                                             "Expected '<class 'list'>' "
                                             "but got '<class 'str'>'"                )

    def test__regression__cache_on_self__shows_on_locals(self):
        class An_Class(Kwargs_To_Self):
            an_str: str

            def an_method(self):
                return 41

            @cache_on_self
            def an_method__cached(self):
                return 42

        an_class = An_Class()
        assert an_class.__locals__       () == {'an_str': ''}
        assert an_class.an_method        () == 41
        assert an_class.an_method__cached() == 42
        #assert an_class.__locals__       () == {'an_str': '', 'cache_on_self_an_method__cached__': 42}  # FIXED was BUG: cache method should not be here
        assert an_class.__locals__       () == {'an_str': ''}                                            # FIXED, cached value is not returned

    def test__regression___base_attrib_value_not_overwritten(self):
        class Base_Class(Kwargs_To_Self):
            an_str : str  = 'an_str__base'
            an_int : int  = 42
            an_bool: bool = True

        class An_Class(Base_Class):
            an_str : str = 'changed on an_class'                # FIXED: BUG: this is not being changed
            an_int : int = 84                                   # FIXED: BUG: this is not being changed
            an_bool: bool = False                               # FIXED: BUG: this is not being changed

        an_class = An_Class()

        expected_values = {'an_bool': False, 'an_int': 84, 'an_str': 'changed on an_class'}
        assert an_class.__locals__() == expected_values


    def test__regression__callable__not_supported(self):
        class An_Class(Kwargs_To_Self):
            an_callable: callable

        def an_local_function():
            pass

        # checking with a method
        assert An_Class(an_callable=self.test__regression__callable__not_supported).__locals__() == { 'an_callable': self.test__regression__callable__not_supported}
        # checking with a function
        assert An_Class(an_callable=an_local_function).__locals__()                              == { 'an_callable': an_local_function}

        # the assets below where failing before the fix
        # with self.assertRaises(Exception) as context:
        #     An_Class(an_callable=self.test__regression__callable__not_supported)
        # assert context.exception.args[0] == ("Invalid type for attribute 'an_callable'. Expected '<built-in function callable>' but got '<class 'method'>'")

        # with self.assertRaises(Exception) as context:
        #     An_Class(an_callable=an_local_function)
        # assert context.exception.args[0] == ("Invalid type for attribute 'an_callable'. Expected '<built-in function callable>' but got '<class 'function'>'")

    def test_regression__should_create_nested_objects_when_loading_dicts(self):                              # Test method to verify the creation of nested objects from dictionaries.
        class Class_A(Type_Safe):                                                                            # Define a nested class Class_A inheriting from Type_Safe.
            an_int: int                                                                                      # Define an attribute 'an_int' of type int.
            an_str: str                                                                                      # Define an attribute 'an_str' of type str.

        class Class_B(Type_Safe):                                                                            # Define another nested class Class_B inheriting from Type_Safe.
            an_bool: bool                                                                                    # Define an attribute 'an_bool' of type bool.
            an_bytes: bytes                                                                                  # Define an attribute 'an_bytes' of type bytes.

        class Class_C(Type_Safe):                                                                            # Define the main class Class_C inheriting from Type_Safe.
            an_class_a: Class_A                                                                              # Define an attribute 'an_class_a' of type Class_A.
            an_class_b: Class_B                                                                              # Define an attribute 'an_class_b' of type Class_B.

        class_c = Class_C()                                                                                  # Instantiate an object of Class_C.
        class_c_as_dict = { 'an_class_a': {'an_int' : 0    , 'an_str'  : '' },                               # Define a dictionary representing class_c with nested dictionaries.
                            'an_class_b': {'an_bool': False, 'an_bytes': b''}}                               # Define attributes for nested Class_B in the dictionary.

        assert class_c.json() == class_c_as_dict                                                              # Assert that the JSON representation of class_c matches the dictionary.
        assert Class_C(**class_c_as_dict).json() == class_c_as_dict                                           # FIXED: now exception is not raised

        class Class_D(Type_Safe):
            an_class_a: dict
            an_class_b: dict
        assert Class_D(**class_c_as_dict).json() == class_c_as_dict                                           # added use case of when both variables are dict

        class Class_F(Type_Safe):
            an_class_a: dict
            an_class_b: Class_B
        assert Class_F(**class_c_as_dict).json() == class_c_as_dict                                           # added use case of when we have a mix

        # with self.assertRaises(ValueError) as context:                                                      # Assert that ValueError is raised during class instantiation with invalid types.
        #     Class_C(**class_c_as_dict)                                                                      # BUG: Attempt to create a Class_C instance with the dictionary.
        #
        # assert context.exception.args[0] == ("Invalid type for attribute 'an_class_a'. Expected '<class "    # Verify the exception message for invalid type of 'an_class_a'.
        #                                      "'test_Type_Safe__bugs.test_Type_Safe__bugs."
        #                                      "test_bug__should_create_nested_objects_when_loading_dicts."
        #                                      "<locals>.Class_A'>' "
        #                                      "but got '<class 'dict'>'")                                     # Complete the verification of the exception message.

    def test_bug_decimal_and_random_guid_are_not_deserialised_ok(self):
        class An_Class(Type_Safe):
            an_decimal : Decimal
            an_guid    : Random_Guid

        an_class = An_Class(an_decimal= Decimal(1.1))

        an_class_str       = json_to_str(an_class.json())
        an_class_roundtrip = An_Class.from_json(str_to_json(an_class_str))
        assert type(an_class_roundtrip)  is An_Class                            # BUG: FIXED: was failing here
        assert an_class_roundtrip.json() == an_class.json()

        # this was the error before the fix
        # with self.assertRaises(ValueError) as context:
        #     An_Class.from_json(str_to_json(an_class_str))
        # assert context.exception.args[0] == ("Invalid type for attribute 'an_decimal'. Expected '<class "
        #                                      "'decimal.Decimal'>' but got '<class 'str'>'")

    def test__regression__json_is_trying_to_serialise__cache_on_self(self):
        class An_Class(Type_Safe):
            an_str : str
            @cache_on_self
            def cached_value(self):
                self.an_str = '42'
                return 42

        an_class = An_Class()
        assert an_class.json() == {'an_str': ''}
        an_class.cached_value()
        assert an_class.json() == {#'__cache_on_self___cached_value__': 42,  # BUG: FIXED: was this should have not been cached
                                   'an_str': '42'}

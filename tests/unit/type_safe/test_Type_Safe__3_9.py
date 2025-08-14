import sys
import pytest
from typing                                              import List, get_origin, get_args, Optional
from unittest                                            import TestCase
from osbot_utils.type_safe.Type_Safe                     import Type_Safe
from osbot_utils.helpers.python_compatibility.python_3_8 import Annotated

class test_Type_Safe__3_9(TestCase):

    @classmethod
    def setUpClass(cls):
        if sys.version_info < (3, 9):
            pytest.skip("Skipping tests that doesn't work on 3.8 or lower")

    def test_annotated_with_lists_with_types(self):

        class Length:
            def __init__(self, min_len: int):
                self.min_len = min_len

        class An_Class(Type_Safe):
            list_nums : Annotated[List[int], Length(1)]                 # List with constraint

        # with pytest.raises(TypeError, match= 'Subscripted generics cannot be used with class and instance checks'):
        #     An_Class(list_nums=[1,2,3])
        an_class = An_Class(list_nums=[1, 2, 3])

        assert an_class.list_nums == [1,2,3]


    def test_annotated_supports_attributes(self):
        class Min:
            def __init__(self, value: int):
                self.value = value

        class Max:
            def __init__(self, value: int):
                self.value = value

        class An_Class(Type_Safe):
            age: Annotated[int, Min(0), Max(150)]

        an_class = An_Class(age=123)
        age_annotation = an_class.__annotations__['age']
        age_origin     = get_origin(age_annotation)
        age_args       = get_args  (age_annotation)
        assert age_origin        is Annotated
        assert len(age_args)     == 3
        assert age_args[0]       is int
        assert type(age_args[1]) is Min
        assert type(age_args[2]) is Max
        assert age_args[1].value == 0
        assert age_args[2].value == 150
        assert an_class.age      == 123

    def test_annotated_with_different_types(self):                     # Test multiple base types with Annotated
        class Min:
            def __init__(self, value: int):
                self.value = value

        class Max:
            def __init__(self, value: int):
                self.value = value

        class Length:
            def __init__(self, min_len: int):
                self.min_len = min_len

        class Pattern:
            def __init__(self, regex: str):
                self.regex = regex

        class TestClass(Type_Safe):
            age       : Annotated[int          , Min(0), Max(150)]          # Multiple constraints
            name      : Annotated[str          , Length(3)]                 # Single constraint
            email     : Annotated[str          , Pattern(r'.*@.*\..*')]     # Different constraint
            price     : Annotated[float        , Min(0.0)]                  # Float with constraint
            nullable  : Annotated[Optional[int], Min(0)]                    # Optional with constraint
            list_nums : Annotated[List    [int], Length(1)]                 # List with constraint

        test = TestClass(age      = 42             ,
                        name      = "John"         ,
                        email     = "test@test.com",
                        price     = 10.5           ,
                        nullable  = None           ,
                        list_nums = [1,2,3]        )
        assert test.age      == 42
        assert test.name     == "John"
        assert test.email    == "test@test.com"
        assert test.price    == 10.5
        assert test.nullable is None
        assert test.list_nums == [1,2,3]

    def test_annotated_type_errors(self):
        class Min:
            def __init__(self, value: int):
                self.value = value

        class TestClass(Type_Safe):
            age: Annotated[int, Min(0)]

        with pytest.raises(ValueError, match="Expected.*but got.*str"):         # Test wrong type
            TestClass(age="42")

        with pytest.raises(ValueError, match="Expected.*but got.*float"):       # Test wrong type for numeric
            TestClass(age=42.0)

    def test_annotated_with_default_values(self):
        class Min:
            def __init__(self, value: int):
                self.value = value

        class Max:
            def __init__(self, value: int):
                self.value = value

        class Length:
            def __init__(self, min_len: int):
                self.min_len = min_len

        class TestClass(Type_Safe):
            age  : Annotated[int, Min(0), Max(150)]  #= 18
            name : Annotated[str, Length(2)]         #= "Anonymous"
            tags : Annotated[List[str], Length(1)]

        # Test with defaults
        test1 = TestClass()
        assert test1.age  == 0
        assert test1.name == ''
        assert test1.tags is None

        #Test overriding defaults
        test2 = TestClass(age=25, name="John", tags=["custom"])
        assert test2.age == 25
        assert test2.name == "John"
        assert test2.tags == ["custom"]
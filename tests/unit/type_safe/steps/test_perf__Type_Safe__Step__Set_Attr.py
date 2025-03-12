import pytest
from unittest                                                      import TestCase
from typing                                                        import List, Dict, Any, Union, Optional, Annotated
from osbot_utils.testing.performance.Performance_Measure__Session  import Performance_Measure__Session
from osbot_utils.type_safe.steps.Type_Safe__Step__Set_Attr         import type_safe_step_set_attr
from osbot_utils.utils.Env                                         import not_in_github_action
from tests.unit.type_safe.steps.test_perf__Type_Safe__Step__Init   import MinLengthValidator, StatusEnum


class test_perf__Type_Safe__Step__Set_Attr(TestCase):                              # Test attribute setting performance

    @classmethod
    def setUpClass(cls):                                                           # Define timing thresholds
        if not_in_github_action():
            pytest.skip("Only run on GitHub (too unstable locally due to local CPU load)")
        cls.time_100_ns  =    100
        cls.time_200_ns  =    200
        cls.time_500_ns  =    500
        cls.time_800_ns  =    800
        cls.time_1_kns   =  1_000
        cls.time_2_kns   =  2_000
        cls.time_3_kns   =  3_000
        cls.time_4_kns   =  4_000
        cls.time_5_kns   =  5_000
        cls.time_6_kns   =  6_000
        cls.time_7_kns   =  7_000
        cls.time_8_kns   =  8_000
        cls.time_9_kns   =  9_000
        cls.time_10_kns  = 10_000

    def test_simple_setattr(self):                                                 # Test simple attribute setting
        class SimpleClass:
            str_val : str
            int_val : int

        obj = SimpleClass()

        def set_str_attr():                                                        # Test setting string attribute
            type_safe_step_set_attr.setattr(obj, obj, "str_val", "test")

        def set_int_attr():                                                        # Test setting int attribute
            type_safe_step_set_attr.setattr(obj, obj, "int_val", 42)

        with Performance_Measure__Session() as session:
            session.measure(set_str_attr).assert_time__less_than(self.time_6_kns)
            session.measure(set_int_attr).assert_time__less_than(self.time_6_kns)

    def test_collection_setattr(self):                                             # Test collection attribute setting
        class CollectionClass:
            list_val : List[str]
            dict_val : Dict[str, Any]

        obj = CollectionClass()

        def set_list_attr():                                                       # Test setting list attribute
            type_safe_step_set_attr.setattr(obj, obj, "list_val", ["a", "b"])

        def set_dict_attr():                                                       # Test setting dict attribute
            type_safe_step_set_attr.setattr(obj, obj, "dict_val", {"key": "value"})

        with Performance_Measure__Session() as session:
            session.measure(set_list_attr).assert_time__less_than(self.time_9_kns )
            session.measure(set_dict_attr).assert_time__less_than(self.time_10_kns)

    def test_union_setattr(self):                                                  # Test union type attribute setting
        class UnionClass:
            union_val    : Union[str, int]
            optional_val : Optional[str]

        obj = UnionClass()

        def set_union_str():                                                       # Test setting union with string
            type_safe_step_set_attr.setattr(obj, obj, "union_val", "test")

        def set_union_int():                                                       # Test setting union with int
            type_safe_step_set_attr.setattr(obj, obj, "union_val", 42)

        def set_optional():                                                        # Test setting optional value
            type_safe_step_set_attr.setattr(obj, obj, "optional_val", "test")

        with Performance_Measure__Session() as session:
            session.measure(set_union_str ).assert_time__less_than(self.time_10_kns)
            session.measure(set_union_int ).assert_time__less_than(self.time_10_kns)
            session.measure(set_optional  ).assert_time__less_than(self.time_10_kns)

    def test_annotated_setattr(self):                                              # Test annotated attribute setting
        class AnnotatedClass:
            validated_str: Annotated[str, MinLengthValidator(3)]
            status: Annotated[str, StatusEnum]

        obj = AnnotatedClass()

        def set_validated_str():                                                    # Test setting validated string
            type_safe_step_set_attr.setattr(obj, obj, "validated_str", "test")

        def set_enum_status():                                                      # Test setting enum value
            type_safe_step_set_attr.setattr(obj, obj, "status", "active")

        with Performance_Measure__Session() as session:
            session.measure(set_validated_str).assert_time__less_than(self.time_10_kns)
            session.measure(set_enum_status  ).assert_time__less_than(self.time_10_kns)

    def test_type_conversion(self):                                                 # Test type conversion
        class ConversionClass:
            str_val : str
            int_val : int
            dict_val: Dict[str, Any]

        obj = ConversionClass()

        def set_str_from_int():                                                     # Test converting int to string
            type_safe_step_set_attr.setattr(obj, obj, "str_val", "42")

        def set_int_from_str():                                                     # Test converting string to int
            type_safe_step_set_attr.setattr(obj, obj, "int_val", 42)

        def set_dict_convert():                                                     # Test dict conversion
            type_safe_step_set_attr.setattr(obj, obj, "dict_val", {"key": 42})

        with Performance_Measure__Session() as session:
            session.measure(set_str_from_int ).assert_time__less_than(self.time_10_kns)
            session.measure(set_int_from_str ).assert_time__less_than(self.time_10_kns)
            session.measure(set_dict_convert ).assert_time__less_than(self.time_10_kns)

    def test_error_cases(self):                                                     # Test error handling performance
        class ErrorClass:
            str_val : str
            int_val : int
            required: str = "required"

        obj = ErrorClass()

        def set_wrong_type():                                                       # Test setting wrong type
            try:
                type_safe_step_set_attr.setattr(obj, obj, "str_val", 42)
            except ValueError:
                pass

        def set_none_value():                                                       # Test setting None
            try:
                type_safe_step_set_attr.setattr(obj, obj, "required", None)
            except ValueError:
                pass

        with Performance_Measure__Session() as session:
            session.measure(set_wrong_type ).assert_time__less_than(self.time_6_kns)
            session.measure(set_none_value ).assert_time__less_than(self.time_2_kns)
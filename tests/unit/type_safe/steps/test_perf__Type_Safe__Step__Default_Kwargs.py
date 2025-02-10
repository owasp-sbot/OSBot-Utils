from unittest                                                             import TestCase
from typing                                                               import List, Dict, Any, Union, Optional

import pytest

from osbot_utils.testing.performance.Performance_Measure__Session         import Performance_Measure__Session
from osbot_utils.type_safe.steps.Type_Safe__Step__Default_Kwargs          import type_safe_step_default_kwargs

class BaseClass:                                                                      # Base class for inheritance tests
    base_str   : str = "base"
    base_int   : int = 42

class test_perf__Type_Safe__Step__Default_Kwargs(TestCase):

    @classmethod
    def setUpClass(cls):                                                             # Define timing thresholds
        cls.time_100_ns  =    100
        cls.time_200_ns  =    200
        cls.time_300_ns  =    300
        cls.time_500_ns  =    500
        cls.time_800_ns  =    800
        cls.time_1_kns   =  1_000
        cls.time_2_kns   =  2_000
        cls.time_3_kns   =  3_000
        cls.time_4_kns   =  4_000
        cls.time_5_kns   =  5_000
        cls.time_6_kns   =  6_000
        cls.time_7_kns   =  7_000
        cls.time_9_kns   =  9_000
        cls.time_10_kns  = 10_000
        cls.time_15_kns  = 15_000

    def test_empty_class(self):                                                      # Test with empty class
        class EmptyClass: pass
        obj = EmptyClass()

        def get_default_kwargs():                                                    # Test default_kwargs()
            return type_safe_step_default_kwargs.default_kwargs(obj)

        def get_kwargs():                                                           # Test kwargs()
            return type_safe_step_default_kwargs.kwargs(obj)

        def get_locals():                                                           # Test locals()
            return type_safe_step_default_kwargs.locals(obj)

        with Performance_Measure__Session() as session:
            session.measure(get_default_kwargs).assert_time(self.time_1_kns)
            session.measure(get_kwargs        ).assert_time(self.time_1_kns)
            session.measure(get_locals        ).assert_time(self.time_2_kns)

    def test_simple_class(self):                                                    # Test with simple attributes
        class SimpleClass:
            str_val  : str = "test"
            int_val  : int = 42
            bool_val : bool = True

            def __init__(self):
                self.dynamic_val = "dynamic"

        obj = SimpleClass()

        def get_simple_default_kwargs():
            return type_safe_step_default_kwargs.default_kwargs(obj)

        def get_simple_kwargs():
            return type_safe_step_default_kwargs.kwargs(obj)

        def get_simple_locals():
            return type_safe_step_default_kwargs.locals(obj)

        with Performance_Measure__Session() as session:
            session.measure(get_simple_default_kwargs).assert_time(self.time_2_kns)
            session.measure(get_simple_kwargs        ).assert_time(self.time_3_kns)
            session.measure(get_simple_locals        ).assert_time(self.time_3_kns)

    def test_inheritance(self):                                                     # Test with inheritance
        class ChildClass(BaseClass):
            child_str : str = "child"
            child_int : int = 84

            def __init__(self):
                self.dynamic_child = "dynamic"

        obj = ChildClass()

        def get_inherited_default_kwargs():
            return type_safe_step_default_kwargs.default_kwargs(obj)

        def get_inherited_kwargs():
            return type_safe_step_default_kwargs.kwargs(obj)

        def get_inherited_locals():
            return type_safe_step_default_kwargs.locals(obj)

        with Performance_Measure__Session() as session:
            session.measure(get_inherited_default_kwargs).assert_time(self.time_3_kns)
            session.measure(get_inherited_kwargs        ).assert_time(self.time_4_kns)
            session.measure(get_inherited_locals        ).assert_time(self.time_4_kns)

    def test_complex_types(self):                                                   # Test with complex type annotations
        class ComplexClass:
            list_val     : List[str] = ["a", "b"]
            dict_val     : Dict[str, Any] = {"key": "value"}
            union_val    : Union[str, int] = "test"
            optional_val : Optional[float] = 3.14

            def __init__(self):
                self.list_val.append("c")
                self.dict_val["new"] = 42

        obj = ComplexClass()

        def get_complex_default_kwargs():
            return type_safe_step_default_kwargs.default_kwargs(obj)

        def get_complex_kwargs():
            return type_safe_step_default_kwargs.kwargs(obj)

        def get_complex_locals():
            return type_safe_step_default_kwargs.locals(obj)

        with Performance_Measure__Session() as session:
            session.measure(get_complex_default_kwargs).assert_time(self.time_2_kns, self.time_3_kns)
            session.measure(get_complex_kwargs        ).assert_time(self.time_3_kns)
            session.measure(get_complex_locals        ).assert_time(self.time_3_kns)

    def test_with_methods(self):                                                    # Test with instance and class methods
        class MethodClass:
            str_val : str = "value"

            def instance_method(self): pass
            @classmethod
            def class_method(cls): pass
            @property
            def prop_method(self): return self.str_val

            def __init__(self):
                self.dynamic_val = "dynamic"

        obj = MethodClass()

        def get_methods_default_kwargs():
            return type_safe_step_default_kwargs.default_kwargs(obj)

        def get_methods_kwargs():
            return type_safe_step_default_kwargs.kwargs(obj)

        def get_methods_locals():
            return type_safe_step_default_kwargs.locals(obj)

        with Performance_Measure__Session() as session:
            session.measure(get_methods_default_kwargs).assert_time(self.time_2_kns)
            session.measure(get_methods_kwargs        ).assert_time(self.time_2_kns, self.time_3_kns)
            session.measure(get_methods_locals        ).assert_time(self.time_3_kns)

    def test_deep_inheritance(self):                                                # Test with deep inheritance chain
        class Level1(BaseClass): level1_val: str = "1"
        class Level2(Level1)  : level2_val: str = "2"
        class Level3(Level2)  : level3_val: str = "3"
        class Level4(Level3)  :
            level4_val: str = "4"
            def __init__(self):
                self.dynamic_val = "dynamic"

        obj = Level4()

        def get_deep_default_kwargs():
            return type_safe_step_default_kwargs.default_kwargs(obj)

        def get_deep_kwargs():
            return type_safe_step_default_kwargs.kwargs(obj)

        def get_deep_locals():
            return type_safe_step_default_kwargs.locals(obj)

        with Performance_Measure__Session() as session:
            session.measure(get_deep_default_kwargs).assert_time(self.time_5_kns, self.time_6_kns)
            session.measure(get_deep_kwargs        ).assert_time(self.time_6_kns, self.time_7_kns)
            session.measure(get_deep_locals        ).assert_time(self.time_7_kns)

    def test_large_class(self):                                                     # Test with large number of attributes
        class LargeClass:
            attr_01: str = "1";  attr_02: int = 2;      attr_03: float = 3.0
            attr_04: str = "4";  attr_05: int = 5;      attr_06: float = 6.0
            attr_07: str = "7";  attr_08: int = 8;      attr_09: float = 9.0
            attr_10: str = "10"; attr_11: int = 11;     attr_12: float = 12.0
            attr_13: List[str] = ["a", "b"]; attr_14: Dict[str, int] = {"a": 1}
            attr_15: Optional[str] = "optional"

            def __init__(self):
                self.dynamic_01 = "d1"
                self.dynamic_02 = "d2"
                self.dynamic_03 = "d3"
                self.dynamic_04 = "d4"
                self.dynamic_05 = "d5"

        obj = LargeClass()

        def get_large_default_kwargs():
            return type_safe_step_default_kwargs.default_kwargs(obj)

        def get_large_kwargs():
            return type_safe_step_default_kwargs.kwargs(obj)

        def get_large_locals():
            return type_safe_step_default_kwargs.locals(obj)

        with Performance_Measure__Session() as session:
            session.measure(get_large_default_kwargs).assert_time(self.time_5_kns, self.time_6_kns )
            session.measure(get_large_kwargs        ).assert_time(self.time_7_kns )
            session.measure(get_large_locals        ).assert_time(self.time_9_kns)

    def test_dynamic_attributes(self):                                              # Test with dynamically added attributes
        class DynamicClass:
            static_val: str = "static"

            def __init__(self):
                self.dynamic_1 = "d1"
                for i in range(10):
                    setattr(self, f"dynamic_{i}", f"value_{i}")

        obj = DynamicClass()

        def get_dynamic_default_kwargs():
            return type_safe_step_default_kwargs.default_kwargs(obj)

        def get_dynamic_kwargs():
            return type_safe_step_default_kwargs.kwargs(obj)

        def get_dynamic_locals():
            return type_safe_step_default_kwargs.locals(obj)

        with Performance_Measure__Session() as session:
            session.measure(get_dynamic_default_kwargs).assert_time(self.time_2_kns)
            session.measure(get_dynamic_kwargs        ).assert_time(self.time_2_kns)
            session.measure(get_dynamic_locals        ).assert_time(self.time_4_kns)

    def test_mixed_class(self):                                                     # Test mix of static and dynamic
        class MixedClass:
            static_str    : str = "static"                                          # Static with annotation
            static_plain  = "plain"                                                 # Static without annotation

            def __init__(self):
                self.dynamic_typed: str = "typed"                                   # Dynamic with type hint
                self.dynamic_plain = "plain"                                        # Dynamic without type hint

        obj = MixedClass()

        def get_mixed_default_kwargs():
            return type_safe_step_default_kwargs.default_kwargs(obj)

        def get_mixed_kwargs():
            return type_safe_step_default_kwargs.kwargs(obj)

        def get_mixed_locals():
            return type_safe_step_default_kwargs.locals(obj)

        with Performance_Measure__Session() as session:
            session.measure(get_mixed_default_kwargs).assert_time(self.time_2_kns)
            session.measure(get_mixed_kwargs        ).assert_time(self.time_2_kns)
            session.measure(get_mixed_locals        ).assert_time(self.time_3_kns)
from unittest                                                     import TestCase
from typing                                                       import List, Dict, Any, Union, Optional, Type
from enum                                                         import Enum
from osbot_utils.testing.performance.Performance_Measure__Session import Performance_Measure__Session
from osbot_utils.type_safe.steps.Type_Safe__Step__Class_Kwargs    import type_safe_step_class_kwargs

class SimpleEnum(Enum):                                                               # Test enum for type checking
    A = 1
    B = 2

class BaseClass:                                                                      # Base class for inheritance tests
    base_str   : str = "base"
    base_int   : int = 42

class test_perf__Type_Safe__Step__Class_Kwargs(TestCase):

    @classmethod
    def setUpClass(cls):                                                             # Define timing thresholds
        cls.assert_enabled = False
        cls.session        = Performance_Measure__Session(assert_enabled=cls.assert_enabled)
        cls.time_100_ns    =    100
        cls.time_200_ns    =    200
        cls.time_300_ns    =    300
        cls.time_500_ns    =    500
        cls.time_700_ns    =    700
        cls.time_800_ns    =    800
        cls.time_1_kns     =  1_000
        cls.time_2_kns     =  2_000
        cls.time_3_kns     =  3_000
        cls.time_4_kns     =  4_000
        cls.time_5_kns     =  5_000
        cls.time_6_kns     =  6_000
        cls.time_9_kns     =  9_000
        cls.time_10_kns    = 10_000
        cls.time_20_kns    = 20_000


    def test_empty_class(self):                                                      # Test with empty class
        class EmptyClass: pass

        def get_empty_kwargs():                                                      # Get kwargs from empty class
            return type_safe_step_class_kwargs.get_cls_kwargs(EmptyClass)

        self.session.measure(get_empty_kwargs).assert_time(self.time_700_ns)

    def test_simple_annotations(self):                                               # Test with simple type annotations
        class SimpleClass:
            str_val  : str
            int_val  : int
            bool_val : bool

        def get_simple_kwargs():
            return type_safe_step_class_kwargs.get_cls_kwargs(SimpleClass)

        self.session.measure(get_simple_kwargs).assert_time(self.time_5_kns)

    def test_complex_annotations(self):                                              # Test with complex type annotations
        class ComplexClass:
            list_val     : List[str]
            dict_val     : Dict[str, Any]
            union_val    : Union[str, int]
            optional_val : Optional[float]
            type_val     : Type['ComplexClass']

        def get_complex_kwargs():
            return type_safe_step_class_kwargs.get_cls_kwargs(ComplexClass)

        self.session.measure(get_complex_kwargs).assert_time(self.time_9_kns)

    def test_inheritance(self):                                                      # Test with class inheritance
        class ChildClass(BaseClass):
            child_str : str = "child"
            child_int : int = 84

        def get_inherited_kwargs_with_base():                                        # Get kwargs including base class
            return type_safe_step_class_kwargs.get_cls_kwargs(ChildClass)

        self.session.measure(get_inherited_kwargs_with_base).assert_time(self.time_6_kns)

    def test_with_methods(self):                                                     # Test with instance and class methods
        class MethodClass:
            str_val : str = "value"

            def instance_method(self): pass
            @classmethod
            def class_method(cls): pass
            @property
            def prop_method(self): return self.str_val

        def get_methods_kwargs():
            return type_safe_step_class_kwargs.get_cls_kwargs(MethodClass)

        self.session.measure(get_methods_kwargs).assert_time(self.time_3_kns)

    def test_with_immutable_defaults(self):                                          # Test with immutable default values
        class DefaultsClass:
            str_val      : str       = "default"
            int_val      : int       = 42
            float_val    : float     = 3.14
            bool_val     : bool      = True
            bytes_val    : bytes     = b"bytes"
            enum_val     : SimpleEnum = SimpleEnum.A

        def get_defaults_kwargs():
            return type_safe_step_class_kwargs.get_cls_kwargs(DefaultsClass)

        self.session.measure(get_defaults_kwargs).assert_time(self.time_10_kns)

    def test_deep_inheritance(self):                                                 # Test with deep inheritance chain
        class Level1(BaseClass): level1_val: str = "1"
        class Level2(Level1)  : level2_val: str = "2"
        class Level3(Level2)  : level3_val: str = "3"
        class Level4(Level3)  : level4_val: str = "4"

        def get_deep_inheritance_kwargs():
            return type_safe_step_class_kwargs.get_cls_kwargs(Level4)

        self.session.measure(get_deep_inheritance_kwargs).assert_time(self.time_10_kns)

    def test_type_validation(self):                                                  # Test type validation performance
        class ValidatedClass:
            str_val : str = 42                                                       # Intentionally wrong type

        def get_invalid_type_kwargs():                                               # Should raise ValueError
            try:
                return type_safe_step_class_kwargs.get_cls_kwargs(ValidatedClass)
            except ValueError:
                pass

        self.session.measure(get_invalid_type_kwargs).assert_time(self.time_3_kns)

    def test_mixed_annotations(self):                                                # Test mix of annotated and non-annotated
        class MixedClass:
            annotated_str   : str = "annotated"                                      # Annotated with default
            annotated_int   : int                                                    # Annotated without default
            unannotated_str = "unannotated"                                          # Unannotated with value

        def get_mixed_kwargs():
            return type_safe_step_class_kwargs.get_cls_kwargs(MixedClass)

        self.session.measure(get_mixed_kwargs).assert_time(self.time_4_kns)

    def test_large_class(self):                                                      # Test with large number of attributes
        class LargeClass:
            attr_01: str = "1";  attr_02: int = 2;      attr_03: float = 3.0
            attr_04: str = "4";  attr_05: int = 5;      attr_06: float = 6.0
            attr_07: str = "7";  attr_08: int = 8;      attr_09: float = 9.0
            attr_10: str = "10"; attr_11: int = 11;     attr_12: float = 12.0
            attr_13: List[str]
            attr_14: Dict[str, int]
            attr_15: Optional[str] = None

        def get_large_kwargs():
            return type_safe_step_class_kwargs.get_cls_kwargs(LargeClass)

        self.session.measure(get_large_kwargs).assert_time(self.time_20_kns)
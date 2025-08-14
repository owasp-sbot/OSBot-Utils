from unittest                                                           import TestCase
from typing                                                             import List, Dict, Any, Union, Optional, Annotated
from enum                                                               import Enum
from osbot_utils.testing.performance.Performance_Measure__Session       import Performance_Measure__Session
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__Init   import type_safe_step_init
from osbot_utils.type_safe.validators.Type_Safe__Validator              import Type_Safe__Validator

class MinLengthValidator(Type_Safe__Validator):                                      # Sample validator for testing
    def __init__(self, min_length: int):
        self.min_length = min_length

    def validate(self, value, field_name, target_type):
        if len(value) < self.min_length:
            raise ValueError(f"{field_name} must be at least {self.min_length} characters")

class StatusEnum(Enum):                                                              # Sample enum for testing
    ACTIVE = "active"
    INACTIVE = "inactive"

class test_perf__Type_Safe__Step__Init(TestCase):                                   # Test initialization performance

    @classmethod
    def setUpClass(cls):                                                            # Define timing thresholds
        cls.time_100_ns  =    100
        cls.time_200_ns  =    200
        cls.time_500_ns  =    500
        cls.time_800_ns  =    800
        cls.time_1_kns   =  1_000
        cls.time_2_kns   =  2_000
        cls.time_3_kns   =  3_000
        cls.time_4_kns   =  4_000
        cls.time_5_kns   =  5_000
        cls.time_7_kns   =  7_000
        cls.time_8_kns   =  8_000
        cls.time_10_kns  = 10_000
        cls.time_20_kns  = 20_000

    def test_simple_init(self):                                                     # Test simple initialization
        class SimpleClass:
            str_val : str = "default"
            int_val : int = 42

        obj = SimpleClass()
        class_kwargs = {"str_val": "default", "int_val": 42}

        def init_no_kwargs():                                                       # Test init with no kwargs
            type_safe_step_init.init(obj, class_kwargs)

        def init_with_kwargs():                                                     # Test init with kwargs
            type_safe_step_init.init(obj, class_kwargs, str_val="new", int_val=100)

        with Performance_Measure__Session() as session:
            session.measure(init_no_kwargs   ).assert_time__less_than(self.time_4_kns)
            session.measure(init_with_kwargs ).assert_time__less_than(self.time_5_kns)

    def test_complex_init(self):                                                    # Test complex initialization
        class ComplexClass:
            list_val     : List[str] = []
            dict_val     : Dict[str, Any] = {}
            union_val    : Union[str, int] = "test"
            optional_val : Optional[float] = None

        obj = ComplexClass()
        class_kwargs = {
            "list_val": [],
            "dict_val": {},
            "union_val": "test",
            "optional_val": None
        }

        def init_complex_default():                                                 # Test init with defaults
            type_safe_step_init.init(obj, class_kwargs)

        def init_complex_kwargs():                                                  # Test init with complex kwargs
            type_safe_step_init.init(obj, class_kwargs,
                list_val=["a", "b"],
                dict_val={"key": "value"},
                union_val=42,
                optional_val=3.14
            )

        with Performance_Measure__Session() as session:
            session.measure(init_complex_default).assert_time__less_than(self.time_7_kns)
            session.measure(init_complex_kwargs ).assert_time__less_than(self.time_20_kns)

    def test_none_handling(self):                                                   # Test None value handling
        class NoneClass:
            required    : str
            optional   : Optional[str] = None
            with_value : str = "value"

        obj = NoneClass()
        class_kwargs = {
            "required": None,
            "optional": None,
            "with_value": "value"
        }

        def init_with_none():                                                       # Test init with None values
            type_safe_step_init.init(obj, class_kwargs)

        def init_override_none():                                                   # Test overriding None values
            type_safe_step_init.init(obj, class_kwargs,
                required="required",
                optional="optional",
                with_value=None
            )

        with Performance_Measure__Session() as session:
            session.measure(init_with_none    ).assert_time__less_than(self.time_2_kns)
            session.measure(init_override_none).assert_time__less_than(self.time_7_kns)


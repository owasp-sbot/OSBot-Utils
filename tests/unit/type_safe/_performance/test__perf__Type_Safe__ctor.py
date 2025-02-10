from dataclasses import dataclass
from unittest                                                         import TestCase
from typing                                                           import Optional, List, Dict, Union, Any
from enum                                                             import Enum, auto
from osbot_utils.testing.performance.Performance_Measure__Session     import Performance_Measure__Session
from osbot_utils.type_safe.Type_Safe                                  import Type_Safe
from osbot_utils.type_safe.shared.Type_Safe__Cache                    import type_safe_cache


class test__perf__Type_Safe__ctor(TestCase):

    @classmethod
    def setUpClass(cls):                                                            # Set up timing thresholds
        # import pytest
        # pytest.skip("skipping until refactoring of Type_Safe is complete")
        cls.time_200_ns  =     200
        cls.time_300_ns  =     300
        cls.time_700_ns  =     700
        cls.time_800_ns  =     800
        cls.time_1_kns   =   1_000
        cls.time_2_kns   =   2_000
        cls.time_3_kns   =   3_000
        cls.time_4_kns   =   4_000
        cls.time_5_kns   =   5_000
        cls.time_6_kns   =   6_000
        cls.time_7_kns   =   7_000
        cls.time_8_kns   =   8_000
        cls.time_9_kns   =   9_000
        cls.time_10_kns  =  10_000
        cls.time_20_kns  =  20_000
        cls.time_30_kns  =  30_000
        cls.time_40_kns  =  40_000
        cls.time_50_kns  =  50_000
        cls.time_60_kns  =  60_000
        cls.time_70_kns  =  70_000
        cls.time_80_kns  =  80_000
        cls.time_90_kns  =  90_000
        cls.time_100_kns = 100_000
        cls.time_200_kns = 200_000
        cls.time_300_kns = 300_000
        cls.time_400_kns = 400_000
        cls.time_600_kns = 600_000
        cls.time_800_kns = 800_000
        cls.assert_enabled = False
        cls.session        = Performance_Measure__Session(assert_enabled=cls.assert_enabled)


    def test_basic_class_instantiation(self):                                   # Test basic Type_Safe variations
        class EmptyClass(Type_Safe): pass                                       # Baseline empty class

        class SingleStr(Type_Safe):                                             # Test with string attribute
            value: str

        class SingleInt(Type_Safe):                                             # Test with integer attribute
            value: int

        class SingleDefault(Type_Safe):                                         # Test with default value
            value: str = "default"

        with self.session as session:
            session.measure(EmptyClass    ).assert_time(self.time_700_ns, self.time_800_ns,    self.time_6_kns , self.time_7_kns)
            session.measure(SingleStr     ).assert_time(self.time_2_kns,                      self.time_20_kns                 )
            session.measure(SingleInt     ).assert_time(self.time_2_kns,                      self.time_20_kns                 )
            session.measure(SingleDefault ).assert_time(self.time_2_kns,                      self.time_20_kns                 )

    def test_complex_types(self):                                               # Test complex type variations
        class ComplexTypes(Type_Safe):                                          # Multiple complex types
            optional_str : Optional[str     ]
            str_list     : List    [str     ]
            int_dict     : Dict    [str, int]
            union_field  : Union   [str, int]

        # class NestedType(Type_Safe):                                            # Basic nested type
        #     value: str
        #
        # class WithNested(Type_Safe):                                            # Complex nesting
        #     nested : NestedType
        #     items  : List[NestedType]

        #print()
        with self.session as session:
            session.measure(ComplexTypes ).print().assert_time(self.time_20_kns,  self.time_30_kns,   self.time_40_kns)
            # session.measure(NestedType   ).print().assert_time(self.time_2_kns ,  self.time_3_kns ,   self.time_20_kns)
            # session.measure(WithNested   ).print().assert_time(self.time_20_kns,                      self.time_40_kns)

        #type_safe_cache.print_cache_hits()

    def test_inheritance_depth(self):                                           # Test inheritance impact
        class Base(Type_Safe):                                                  # Base class
            base_value: str

        class Level1(Base):                                                     # First inheritance level
            level1_value: int

        class Level2(Level1):                                                   # Second inheritance level
            level2_value: float

        class Level3(Level2):                                                   # Third inheritance level
            level3_value: bool

        with self.session as session:
            session.measure(Base   ).assert_time(self.time_2_kns , self.time_3_kns ,    self.time_20_kns)
            session.measure(Level1 ).assert_time(self.time_4_kns ,                      self.time_30_kns)
            session.measure(Level2 ).assert_time(self.time_6_kns ,                      self.time_40_kns)
            session.measure(Level3 ).assert_time(self.time_8_kns , self.time_9_kns ,  self.time_50_kns)

    def test_enum_handling(self):                                               # Test Enum type handling
        class Status(Enum):                                                     # Define test enum
            ACTIVE   = auto()
            INACTIVE = auto()
            PENDING  = auto()

        class WithEnum(Type_Safe):                                              # Class with enum
            status: Status

        class WithEnumDefault(Type_Safe):                                       # Class with default enum
            status: Status = Status.ACTIVE

        with self.session as session:
            session.measure(WithEnum       ).assert_time(self.time_2_kns ,    self.time_10_kns)
            session.measure(WithEnumDefault).assert_time(self.time_9_kns ,    self.time_20_kns, self.time_30_kns)

    def test_initialization_with_values(self):                                  # Test initialization performance
        class ConfigClass(Type_Safe):                                           # Test configuration class
            name    : str
            count   : int
            enabled : bool

        def create_with_kwargs():                                               # Create with all values
            return ConfigClass(name    = "test",
                             count   = 42    ,
                             enabled = True  )

        def create_empty():                                                     # Create with defaults
            return ConfigClass()

        with self.session as session:
            session.measure(create_empty      ).assert_time(self.time_5_kns , self.time_6_kns ,   self.time_40_kns)
            session.measure(create_with_kwargs).assert_time(self.time_8_kns ,                     self.time_50_kns, self.time_60_kns)

    def test_type_validation_overhead(self):                                    # Test validation performance
        class WithValidation(Type_Safe):                                        # Class needing validation
            int_field : int
            str_field : str

        def create_valid():                                                     # Direct valid types
            return WithValidation(int_field = 42   ,
                                  str_field = "test")

        with self.session as session:
            session.measure(create_valid          ).assert_time(self.time_5_kns , self.time_6_kns ,     self.time_40_kns)

    def test_collection_types(self):                                            # Test collection performance
        class WithCollections(Type_Safe):                                       # Simple collections
            str_list    : List[str]
            int_dict    : Dict[str, int]
            mixed_list  : List[Union[str, int]]

        class NestedCollections(Type_Safe):                                     # Nested collections
            matrix      : List[List[int]]
            nested_dict : Dict[str, Dict[str, Any]]

        with self.session as session:
            session.measure(WithCollections   ).assert_time(self.time_30_kns,   self.time_40_kns)
            session.measure(NestedCollections ).assert_time(self.time_20_kns,   self.time_30_kns)

    def test_serialization_performance(self):                                   # Test serialization speeds
        class SerializedType(Type_Safe):                                       # Complex type for serialization
            name        : str = "test"
            values     : List[int]
            nested     : Dict[str, int]

        test_obj = SerializedType(values=[1, 2, 3], nested={"a": 1, "b": 2})

        def serialize_to_json():                                               # Test JSON serialization
            return test_obj.json()


        with self.session as session:
            session.measure(serialize_to_json    ).assert_time(self.time_5_kns  ,  self.time_9_kns  )

    def test_method_override_performance(self):                                # Test method overriding impact
        class BaseWithMethods(Type_Safe):                                      # Base with typed methods
            value: int = 0

            def increment(self, amount: int) -> int:
                self.value += amount
                return self.value

            def reset(self) -> None:
                self.value = 0

        class DerivedWithOverrides(BaseWithMethods):                          # Derived with overrides
            def increment(self, amount: int) -> int:
                self.value += amount * 2
                return self.value

        base    = BaseWithMethods()
        derived = DerivedWithOverrides()

        def call_base_method():                                               # Test base method call
            base.increment(1)
            base.reset()

        def call_derived_method():                                            # Test overridden method
            derived.increment(1)
            derived.reset()

        with self.session as session:
            session.measure(call_base_method   ).assert_time(self.time_1_kns  , self.time_10_kns)
            session.measure(call_derived_method).assert_time(self.time_1_kns  , self.time_10_kns)

    def test_property_access_performance(self):                               # Test property access speeds
        class WithProperties(Type_Safe):                                      # Class using properties
            def __init__(self):
                super().__init__()
                self._value = 0

            @property
            def value(self) -> int:
                return self._value

            @value.setter
            def value(self, val: int):
                self._value = val

        class WithDirectAccess(Type_Safe):                                    # Class with direct access
            value: int = 0

        props    = WithProperties()
        direct   = WithDirectAccess()

        def access_property():                                                # Test property access
            props.value = 42
            _ = props.value

        def access_direct():                                                  # Test direct access
            direct.value = 42
            _ = direct.value

        with self.session as session:
            session.measure(access_property).assert_time(self.time_3_kns    , self.time_4_kns)
            session.measure(access_direct  ).assert_time(self.time_700_ns   , self.time_6_kns, self.time_7_kns)

    def test_context_manager_performance(self):                               # Test context manager overhead
        class SimpleType(Type_Safe):                                          # Simple managed type
            value: int = 0

        def use_context_manager():                                           # Use with context manager
            with SimpleType() as obj:
                obj.value = 42

        def direct_usage():                                                  # Use without context manager
            obj = SimpleType()
            obj.value = 42

        with self.session as session:
            session.measure(use_context_manager).assert_time(self.time_3_kns,    self.time_20_kns)
            session.measure(direct_usage       ).assert_time(self.time_3_kns,    self.time_20_kns)

    def test_merge_performance(self):                                         # Test merge operation speed
        class SourceType(Type_Safe):                                         # Source for merge
            name    : str = "source"
            value  : int = 42

        class TargetType(Type_Safe):                                         # Target for merge
            name    : str = "target"
            value  : int = 0
            extra  : str = "extra"

        source = SourceType()
        target = TargetType()

        def perform_merge():                                                 # Test merge operation
            target.merge_with(source)

        with self.session as session:
            session.measure(perform_merge).assert_time(self.time_3_kns,   self.time_6_kns)

    @dataclass
    class ComplexDefault:                                                    # Helper for comparison
        name   : str = "test"
        value : int = 42

    def test_against_dataclass(self):                                       # Compare with dataclass
        class TypeSafeVersion(Type_Safe):                                   # Equivalent Type_Safe class
            name   : str = "test"
            value : int = 42

        def create_dataclass():                                            # Create dataclass instance
            return self.ComplexDefault()

        def create_type_safe():                                           # Create Type_Safe instance
            return TypeSafeVersion()

        with self.session as session:
            session.measure(create_dataclass).assert_time(self.time_200_ns    , self.time_300_ns)
            session.measure(create_type_safe).assert_time(self.time_4_kns     ,  self.time_20_kns, self.time_30_kns)

    def test_union_type_performance(self):              # Test performance of union type validation
        class WithUnion(Type_Safe):
            field: Union[str, int, float]
            nested: Union[List[str]]

        def test_first_type():
            return WithUnion(field="str", nested=["a", "b"])

        def test_last_type():
            return WithUnion(field=1.0, nested=["a", "b", "c", "d"])

        with self.session as session:
            session.measure(test_first_type).assert_time(self.time_20_kns,     self.time_30_kns, self.time_40_kns)
            session.measure(test_last_type ).assert_time(self.time_20_kns,     self.time_30_kns)

    def test_forward_ref_performance(self):                 # Test performance of forward reference resolution
        class Node(Type_Safe):
            value   : int
            next    : 'Node'
            children: List   ['Node']

        def create_chain():
            root      = Node(value=1)
            root.next = Node(value=2)
            return root

        def create_tree():
            root = Node(value=1)
            root.children = [Node(value=i) for i in range(2,5)]
            return root

        with self.session as session:
            session.measure(create_chain).assert_time(self.time_30_kns   , self.time_80_kns )
            session.measure(create_tree ).assert_time(self.time_60_kns   , self.time_200_kns, self.time_300_kns)

    def test_mixed_defaults_performance(self):               # Test performance of mixed default value handling
        class MixedDefaults(Type_Safe):
            explicit_str: str = "default"
            explicit_int: int = 42
            implicit_str: str
            implicit_int: int
            optional_str: Optional[str] = None

        def create_with_defaults():
            return MixedDefaults()

        def create_with_overrides():
            return MixedDefaults(
                explicit_str="override",
                explicit_int=100,
                implicit_str="set",
                implicit_int=200,
                optional_str="provided"
            )

        with self.session as session:
            session.measure(create_with_defaults ).assert_time(self.time_8_kns     , self.time_50_kns)
            session.measure(create_with_overrides).assert_time(self.time_20_kns    , self.time_80_kns, self.time_90_kns)

    def test_deep_nesting_performance(self):                    # Test performance of deeply nested type validation
        class Level3(Type_Safe):
            value: int

        class Level2(Type_Safe):
            nested: Level3
            values: List[Level3]

        class Level1(Type_Safe):
            nested: Level2
            mapping: Dict[str, Level2]

        def create_deep_nested():
            l3 = Level3(value=42)
            l2 = Level2(nested=l3, values=[l3, Level3(value=43)])
            return Level1(nested=l2, mapping={"test": l2})

        with self.session as session:
            session.measure(create_deep_nested).assert_time(self.time_80_kns        , self.time_200_kns)

    def test_large_object_instantiation(self):                  # Test performance with large object graphs
        class Item(Type_Safe):
            id: str
            value: int

        class Container(Type_Safe):
            items: List[Item]

        def create_medium_object():
            return Container(items=[Item(id=str(i), value=i) for i in range(10)])

        def create_larger_object():
            return Container(items=[Item(id=str(i), value=i)for i in range(20)])

        with self.session as session:
            session.measure(create_medium_object).assert_time(self.time_70_kns,   self.time_400_kns)
            session.measure(create_larger_object).assert_time(self.time_100_kns)
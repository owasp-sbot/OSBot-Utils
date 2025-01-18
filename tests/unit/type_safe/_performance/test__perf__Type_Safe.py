from unittest                                                         import TestCase
from typing                                                           import Optional, List, Dict, Union, Any
from enum                                                             import Enum, auto
from osbot_utils.testing.performance.Performance_Measure__Session     import Performance_Measure__Session
from osbot_utils.type_safe.Type_Safe                                  import Type_Safe


class test__perf__Type_Safe(TestCase):
    
    def setUp(self):                                                            # Set up timing thresholds
        self.time_6_kns  =  6_000
        self.time_7_kns  =  7_000
        self.time_10_kns = 10_000
        self.time_20_kns = 20_000
        self.time_30_kns = 30_000
        self.time_40_kns = 40_000
        self.time_50_kns = 50_000
        self.time_60_kns = 60_000

    def test_basic_class_instantiation(self):                                   # Test basic Type_Safe variations
        class EmptyClass(Type_Safe): pass                                       # Baseline empty class
            
        class SingleStr(Type_Safe):                                             # Test with string attribute
            value: str
            
        class SingleInt(Type_Safe):                                             # Test with integer attribute
            value: int
            
        class SingleDefault(Type_Safe):                                         # Test with default value
            value: str = "default"
            
        with Performance_Measure__Session() as session:
            session.measure(EmptyClass    ).assert_time(self.time_6_kns , self.time_7_kns)
            session.measure(SingleStr     ).assert_time(self.time_20_kns                 )
            session.measure(SingleInt     ).assert_time(self.time_20_kns                 )
            session.measure(SingleDefault ).assert_time(self.time_20_kns                 )

    def test_complex_types(self):                                               # Test complex type variations
        class ComplexTypes(Type_Safe):                                          # Multiple complex types
            optional_str : Optional[str]
            str_list    : List[str]
            int_dict    : Dict[str, int]
            union_field : Union[str, int]
            
        class NestedType(Type_Safe):                                            # Basic nested type
            value: str
            
        class WithNested(Type_Safe):                                            # Complex nesting
            nested : NestedType
            items  : List[NestedType]
            
        with Performance_Measure__Session() as session:
            session.measure(ComplexTypes ).assert_time(self.time_40_kns)
            session.measure(NestedType   ).assert_time(self.time_20_kns)
            session.measure(WithNested   ).assert_time(self.time_40_kns)

    def test_inheritance_depth(self):                                           # Test inheritance impact
        class Base(Type_Safe):                                                  # Base class
            base_value: str
            
        class Level1(Base):                                                     # First inheritance level
            level1_value: int
            
        class Level2(Level1):                                                   # Second inheritance level
            level2_value: float
            
        class Level3(Level2):                                                   # Third inheritance level
            level3_value: bool
            
        with Performance_Measure__Session() as session:
            print()
            session.measure(Base   ).print().assert_time(self.time_20_kns)
            session.measure(Level1 ).print().assert_time(self.time_30_kns)
            session.measure(Level2 ).print().assert_time(self.time_40_kns)
            session.measure(Level3 ).print().assert_time(self.time_50_kns)

    def test_enum_handling(self):                                               # Test Enum type handling
        class Status(Enum):                                                     # Define test enum
            ACTIVE   = auto()
            INACTIVE = auto()
            PENDING  = auto()
            
        class WithEnum(Type_Safe):                                              # Class with enum
            status: Status
            
        class WithEnumDefault(Type_Safe):                                       # Class with default enum
            status: Status = Status.ACTIVE
            
        with Performance_Measure__Session() as session:
            session.measure(WithEnum       ).assert_time(self.time_10_kns)
            session.measure(WithEnumDefault).assert_time(self.time_20_kns, self.time_30_kns)

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
            
        with Performance_Measure__Session() as session:
            session.measure(create_empty      ).assert_time(self.time_40_kns)
            session.measure(create_with_kwargs).assert_time(self.time_50_kns, self.time_60_kns)

    def test_type_validation_overhead(self):                                    # Test validation performance
        class WithValidation(Type_Safe):                                        # Class needing validation
            int_field : int
            str_field : str
            
        def create_valid():                                                     # Direct valid types
            return WithValidation(int_field = 42   ,
                                  str_field = "test")
            
        # def create_with_conversion():                                           # Types needing conversion
        #     return WithValidation(int_field = "42"  ,
        #                           str_field = "test")
            
        with Performance_Measure__Session() as session:
            session.measure(create_valid          ).assert_time(self.time_40_kns)
            #session.measure(create_with_conversion).assert_time(self.time_30kns)  # todo: fix this will raise an exception

    def test_collection_types(self):                                            # Test collection performance
        class WithCollections(Type_Safe):                                       # Simple collections
            str_list    : List[str]
            int_dict    : Dict[str, int]
            mixed_list  : List[Union[str, int]]
            
        class NestedCollections(Type_Safe):                                     # Nested collections
            matrix      : List[List[int]]
            nested_dict : Dict[str, Dict[str, Any]]
            
        with Performance_Measure__Session() as session:
            session.measure(WithCollections   ).assert_time(self.time_30_kns, self.time_40_kns)
            session.measure(NestedCollections ).assert_time(self.time_30_kns)
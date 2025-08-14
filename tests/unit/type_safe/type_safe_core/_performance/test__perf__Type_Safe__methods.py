import pytest
from unittest                                                         import TestCase
from typing                                                           import List, Dict, Any
from osbot_utils.testing.performance.Performance_Measure__Session     import Performance_Measure__Session
from osbot_utils.type_safe.Type_Safe                                  import Type_Safe
from osbot_utils.utils.Json                                           import json_to_str


class test__perf__Type_Safe__methods(TestCase):

    @classmethod
    def setUpClass(cls):                                                     # Set up timing thresholds

        pytest.skip("skipping until refactoring of Type_Safe is complete")

        cls.time_100_ns =      100
        cls.time_2_kns  =    2_000
        cls.time_3_kns  =    3_000
        cls.time_5_kns  =    5_000
        cls.time_6_kns   =   6_000
        cls.time_7_kns   =   7_000
        cls.time_8_kns   =   8_000
        cls.time_9_kns   =   9_000
        cls.time_10_kns  =  10_000
        cls.time_20_kns  =  20_000
        cls.time_30_kns  =  30_000
        cls.time_70_kns   = 70_000
        cls.time_100_kns = 100_000
        cls.time_200_kns = 200_000
        cls.time_300_kns = 300_000
        cls.time_400_kns = 400_000
        cls.time_600_kns = 600_000

    def test__setattr__(self):                                             # Test attribute assignment
        class Pure_Class            : pass                                  # Pure Python empty class
        class Empty_Class(Type_Safe): pass                                  # Baseline empty class

        empty_class = Empty_Class()
        pure_class  = Pure_Class()

        def test__empty_class__setattr__():                                # Test Type_Safe setattr
            empty_class.test = 1

        def test__pure_class__setattr__():                                 # Test pure Python setattr
            pure_class.test = 1

        with Performance_Measure__Session() as session:
            session.measure(test__empty_class__setattr__).assert_time(self.time_2_kns )
            session.measure(test__pure_class__setattr__ ).assert_time(self.time_100_ns)

    def test__cls_kwargs__(self):                                          # Test class kwargs retrieval
        class An_Class(Type_Safe):                                         # Test class with attributes
            attr_1  : str  = "value"
            attr_2  : int  = 42
            attr_3  : List

        def get_cls_kwargs():                                              # Get class kwargs
            return An_Class.__cls_kwargs__()

        with Performance_Measure__Session() as session:
            session.measure(get_cls_kwargs).assert_time(self.time_8_kns)

    def test__default_kwargs__(self):                                      # Test default kwargs
        class An_Class(Type_Safe):                                         # Test class with defaults
            attr_1 : str  = "value"
            attr_2 : int  = 42
            attr_3 : List

        an_class = An_Class()

        def get_default_kwargs():                                          # Get default kwargs
            return an_class.__default_kwargs__()

        with Performance_Measure__Session() as session:
            session.measure(get_default_kwargs).assert_time(self.time_5_kns)

    def test__kwargs__(self):                                             # Test kwargs retrieval
        class An_Class(Type_Safe):                                        # Test class with attributes
            attr_1 : str  = "value"
            attr_2 : int  = 42
            attr_3 : List

        an_class = An_Class()

        def get_kwargs():                                                 # Get instance kwargs
            return an_class.__kwargs__()

        with Performance_Measure__Session() as session:
            session.measure(get_kwargs).assert_time(self.time_5_kns, self.time_6_kns)

    def test__locals__(self):                                            # Test locals retrieval
        class An_Class(Type_Safe):                                       # Test class with locals
            attr_1 : str  = "value"
            attr_2 : int  = 42
            attr_3 : List

            def __init__(self):
                super().__init__()
                self.local_1 = "local"
                self.local_2 = 123

        an_class = An_Class()

        def get_locals():                                               # Get instance locals
            return an_class.__locals__()

        with Performance_Measure__Session() as session:
            session.measure(get_locals).assert_time(self.time_7_kns)

    def test_json_operations(self):                                     # Test JSON operations
        class An_Class(Type_Safe):                                     # Test class with nested data
            attr_1 : str           = "value"
            attr_2 : int           = 42
            attr_3 : List[int]
            attr_4 : Dict[str,Any]

        an_class = An_Class(attr_3=[1,2,3], attr_4={"a": 1, "b": 2})
        json_str = json_to_str(an_class.json())

        def to_json():                                                # Convert to JSON
            return an_class.json()

        def from_json():                                             # Create from JSON
            return An_Class.from_json(json_str)

        with Performance_Measure__Session() as session:
            session.measure(to_json  ).assert_time(self.time_8_kns, self.time_9_kns, self.time_10_kns)
            session.measure(from_json).assert_time(self.time_100_kns)

    def test_bytes_operations(self):                                  # Test bytes operations
        class An_Class(Type_Safe):                                   # Test class with data
            attr_1 : str = "value"
            attr_2 : int = 42

        an_class = An_Class()

        def to_bytes():                                             # Convert to bytes
            return an_class.bytes()

        def to_bytes_gz():                                         # Convert to gzipped bytes
            return an_class.bytes_gz()

        with Performance_Measure__Session() as session:
            session.measure(to_bytes   ).assert_time(self.time_8_kns , self.time_9_kns)
            session.measure(to_bytes_gz).assert_time(self.time_20_kns)

    def test_reset(self):                                          # Test reset operation
        class An_Class(Type_Safe):                                 # Test class with defaults
            attr_1 : str  = "value"
            attr_2 : int  = 42
            attr_3 : List

        an_class = An_Class()
        an_class.attr_1 = "changed"
        an_class.attr_2 = 123
        an_class.attr_3 = [1,2,3]

        def do_reset():                                           # Reset instance
            an_class.reset()

        with Performance_Measure__Session() as session:
            session.measure(do_reset).assert_time(self.time_30_kns)

    def test_obj_method(self):                                    # Test obj conversion
        class An_Class(Type_Safe):                               # Test class with data
            attr_1 : str = "value"
            attr_2 : int = 42

        an_class = An_Class()

        def get_obj():                                          # Get simple object
            return an_class.obj()

        with Performance_Measure__Session() as session:
            session.measure(get_obj).assert_time(self.time_5_kns, self.time_6_kns)

    def test_dynamic_access_performance(self):                      # Test performance of dynamic attribute access
        class Dynamic(Type_Safe):
            field_1: str = "value1"
            field_2: int = 42

        obj = Dynamic()

        def access_via_getattr():
            return getattr(obj, "field_1")

        def access_via_setattr():
            setattr(obj, "field_2", 100)

        with Performance_Measure__Session() as session:
            session.measure(access_via_getattr).assert_time(self.time_100_ns)
            session.measure(access_via_setattr).assert_time(self.time_7_kns)

    def test_error_handling_performance(self):                      # Test performance of error handling paths
        class Validated(Type_Safe):
            int_field: int
            str_field: str

        obj = Validated()

        def test_invalid_type():
            try:
                obj.int_field = "not an int"
            except ValueError:
                pass

        def test_none_assignment():
            try:
                obj.str_field = None
            except ValueError:
                pass

        with Performance_Measure__Session() as session:
            session.measure(test_invalid_type   ).assert_time(self.time_8_kns)
            session.measure(test_none_assignment).assert_time(self.time_3_kns)

    def test_circular_reference_performance(self):                  # Test performance with circular references
        class Node(Type_Safe):
            id        : str
            references: List['Node']

        def create_and_serialize_circular():
            n1 = Node(id="1")
            n2 = Node(id="2")
            n1.references.append(n2)
            n2.references.append(n1)


        with Performance_Measure__Session() as session:
            session.measure(create_and_serialize_circular).assert_time(self.time_70_kns)

    def test_large_serialization_performance(self):                 # Test performance of large object serialization"""
        class Item(Type_Safe):
            id: str
            value: int

        class Container(Type_Safe):
            items: List[Item]

        container = Container(items=[Item(id=str(i), value=i) for i in range(50)])

        def serialize_large():
            return container.json()

        def serialize_to_bytes():
            return container.bytes()

        with Performance_Measure__Session() as session:
            session.measure(serialize_large   ).assert_time(self.time_400_kns, self.time_200_kns)       # time_400_kns first due to github actions
            session.measure(serialize_to_bytes).assert_time(self.time_600_kns, self.time_300_kns)       # time_600_kns first due to github actions
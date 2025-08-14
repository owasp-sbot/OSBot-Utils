import pytest
from unittest                                                               import TestCase
from typing                                                                 import List, Dict, Any, Union, Optional, Type
from enum                                                                   import Enum
from decimal                                                                import Decimal
from osbot_utils.testing.performance.Performance_Measure__Session           import Performance_Measure__Session
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.primitives.safe_str.identifiers.Random_Guid      import Random_Guid
from osbot_utils.type_safe.primitives.safe_str.identifiers.Random_Guid_Short                                  import Random_Guid_Short
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id          import Safe_Id
from osbot_utils.type_safe.primitives.safe_int.Timestamp_Now                 import Timestamp_Now
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__From_Json  import type_safe_step_from_json
from osbot_utils.utils.Env                                                  import not_in_github_action


class StatusEnum(Enum):                                                            # Test enum for deserialization
    ACTIVE = "active"
    INACTIVE = "inactive"

class NestedType(Type_Safe):                                                      # Test nested type for deserialization
    value: str
    count: int

class ComplexType(Type_Safe):                                                     # Test complex type for deserialization
    nested: NestedType
    items: List[NestedType]
    mappings: Dict[str, NestedType]

class test_perf__Type_Safe__Step__From_Json(TestCase):

    @classmethod
    def setUpClass(cls):                                                          # Define timing thresholds
        if not_in_github_action():
            pytest.skip("Only run on GitHub (too unstable locally due to local CPU load)")
        cls.time_100_ns  =     100
        cls.time_200_ns  =     200
        cls.time_500_ns  =     500
        cls.time_800_ns  =     800
        cls.time_1_kns   =   1_000
        cls.time_2_kns   =   2_000
        cls.time_3_kns   =   3_000
        cls.time_5_kns   =   5_000
        cls.time_10_kns  =  10_000
        cls.time_20_kns  =  20_000
        cls.time_30_kns  =  30_000
        cls.time_40_kns  =  40_000
        cls.time_50_kns  =  50_000
        cls.time_70_kns  =  70_000
        cls.time_80_kns  =  80_000
        cls.time_90_kns  =  90_000
        cls.time_100_kns = 100_000
        cls.time_200_kns = 200_000
        cls.time_300_kns = 300_000

    def test_primitive_deserialization(self):                                     # Test primitive type deserialization
        class SimpleClass(Type_Safe):
            str_val  : str
            int_val  : int
            bool_val : bool
            float_val: float

        json_data = {
            "str_val": "test",
            "int_val": 42,
            "bool_val": True,
            "float_val": 3.14
        }

        def deserialize_primitives():                                            # Test basic deserialization
            return type_safe_step_from_json.from_json(SimpleClass, json_data)

        def deserialize_from_str():                                             # Test string JSON deserialization
            return type_safe_step_from_json.from_json(SimpleClass, str(json_data))

        with Performance_Measure__Session() as session:
            session.measure(deserialize_primitives).assert_time__less_than(self.time_70_kns)
            session.measure(deserialize_from_str  ).assert_time__less_than(self.time_30_kns)

    def test_collection_deserialization(self):                                   # Test collection deserialization
        class CollectionClass(Type_Safe):
            list_val    : List[str]
            dict_val    : Dict[str, int]
            #nested_list : List[List[str]]
            #nested_dict : Dict[str, Dict[str, int]]

        json_data = {
            "list_val": ["a", "b", "c"],
            "dict_val": {"key": 42},
            #"nested_list": [["x", "y"], ["z"]],
            #"nested_dict": {"outer": {"inner": 123}}
        }

        def deserialize_collections():                                          # Test collection deserialization
            return type_safe_step_from_json.from_json(CollectionClass, json_data)

        with Performance_Measure__Session() as session:
            session.measure(deserialize_collections).assert_time__less_than(self.time_70_kns)

    def test_special_types_deserialization(self):                               # Test special type deserialization
        class SpecialClass(Type_Safe):
            decimal_val : Decimal
            guid_val    : Random_Guid
            guid_short  : Random_Guid_Short
            safe_id     : Safe_Id
            timestamp   : Timestamp_Now
            enum_val    : StatusEnum

        json_data = {
            "decimal_val": "123.45",
            "guid_val": "12345678-1234-5678-1234-567812345678",
            "guid_short": "abcd1234",
            "safe_id": "test_id",
            "timestamp": "12345677",
            "enum_val": "ACTIVE"
        }

        def deserialize_special():                                             # Test special type deserialization
            return type_safe_step_from_json.from_json(SpecialClass, json_data)

        with Performance_Measure__Session() as session:
            session.measure(deserialize_special).assert_time__less_than(self.time_200_kns)

    def test_nested_type_deserialization(self):                                # Test nested type deserialization
        json_data = {
            "nested": {
                "value": "test",
                "count": 1
            },
            "items": [
                {"value": "item1", "count": 1},
                {"value": "item2", "count": 2}
            ],
            "mappings": {
                "key1": {"value": "map1", "count": 1},
                "key2": {"value": "map2", "count": 2}
            }
        }

        def deserialize_nested():                                             # Test nested structure deserialization
            return type_safe_step_from_json.from_json(ComplexType, json_data)

        with Performance_Measure__Session() as session:
            session.measure(deserialize_nested).assert_time__less_than(self.time_200_kns)

    def test_type_reconstruction(self):                                       # Test type reconstruction
        class TypeClass(Type_Safe):
            type_val: type
            typed_int: Type[int]

        json_data = {
            "type_val": "builtins.str",
            "optional_type": "builtins.int"
        }

        def deserialize_type():                                              # Test type deserialization
            return type_safe_step_from_json.from_json(TypeClass, json_data)

        def deserialize_none_type():                                         # Test NoneType deserialization
            return type_safe_step_from_json.deserialize_type__using_value("builtins.NoneType")

        with Performance_Measure__Session() as session:
            session.measure(deserialize_type     ).assert_time__less_than(self.time_20_kns )
            session.measure(deserialize_none_type).assert_time__less_than(self.time_500_ns)

    def test_dict_key_value_annotations(self):                               # Test dict with annotated keys/values
        class AnnotatedDict(Type_Safe):
            basic_dict    : Dict[str, int]
            complex_dict  : Dict[str, NestedType]
            any_dict      : Dict[str, Any]

        json_data = {
            "basic_dict": {"a": 1, "b": 2},
            "complex_dict": {
                "key1": {"value": "test1", "count": 1},
                "key2": {"value": "test2", "count": 2}
            },
            "any_dict": {"x": 1, "y": "string", "z": True}
        }

        def deserialize_annotated_dict():                                    # Test annotated dict deserialization
            return type_safe_step_from_json.from_json(AnnotatedDict, json_data)

        with Performance_Measure__Session() as session:
            session.measure(deserialize_annotated_dict).assert_time__less_than(self.time_200_kns)

    def test_error_handling(self):                                           # Test error handling
        class ErrorClass(Type_Safe):
            required: str
            typed_dict: Dict[str, int]

        invalid_json = {
            "missing": "value",                                              # Missing required field
            "typed_dict": {"key": "not_an_int"}                             # Wrong value type
        }

        def deserialize_with_errors():                                       # Test error handling
            try:
                return type_safe_step_from_json.from_json(
                    ErrorClass,
                    invalid_json,
                    raise_on_not_found=True
                )
            except ValueError:
                pass

        with Performance_Measure__Session() as session:
            session.measure(deserialize_with_errors).assert_time__less_than(self.time_20_kns)

    def test_large_structure(self):                                          # Test large structure deserialization
        class LargeItem(Type_Safe):
            id: str
            value: int
            data: Dict[str, Any]

        class LargeStructure(Type_Safe):
            items   : List[LargeItem]
            mappings: Dict[str, LargeItem]

        json_data = {
            "items": [
                {"id": f"item{i}", "value": i, "data": {"key": f"value{i}"}}
                for i in range(2)
            ],
            "mappings": {
                f"key{i}": {"id": f"map{i}", "value": i, "data": {"key": f"value{i}"}}
                for i in range(2)
            }
        }

        def deserialize_large():                                             # Test large structure deserialization
            return type_safe_step_from_json.from_json(LargeStructure, json_data)

        with Performance_Measure__Session() as session:
            session.measure(deserialize_large).assert_time__less_than(self.time_300_kns)
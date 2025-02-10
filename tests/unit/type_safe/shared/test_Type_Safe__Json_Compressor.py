from unittest                                                import TestCase
from typing                                                  import Type, Dict, List, Set
from osbot_utils.type_safe.Type_Safe                         import Type_Safe
from osbot_utils.type_safe.shared.Type_Safe__Json_Compressor import Type_Safe__Json_Compressor


class Simple_Config(Type_Safe):                                                      # Base test class
    name  : str = "an_name"
    value : int = 42

class Schema__First__Second__Third(Type_Safe):                                       # Test class with multiple parts
    id    : str = "an_id"
    value : int = 123

class Schema__Alpha__Beta(Type_Safe):                                                # Another multi-part class
    field_1: str = "field_1"
    field_2: int = 456

class Nested_Type_One(Type_Safe):                                                    # Class for nested type tests
    type_field: Type[Schema__First__Second__Third]
    values   : Dict[str, int]




class test_Type_Safe__Json_Compressor(TestCase):

    def setUp(self):
        self.compressor = Type_Safe__Json_Compressor()

    def test_basic_compression(self):
        class Type_Container(Type_Safe):
            type_field: Type[Simple_Config]
            name     : str = "container"

        container = Type_Container()
        compressed = self.compressor.compress(container)

        assert "_type_registry"          in compressed                                # Registry included
        assert compressed["type_field"].startswith("@")                              # Type field compressed
        assert compressed["name"]         == "container"                              # Regular field unchanged

        decompressed = self.compressor.decompress(compressed)
        assert decompressed == container.json()                                                   # Round trip works


    def test_nested_objects(self):
        nested        = Nested_Type_One()
        nested.values = {"key": 123}
        compressed    = self.compressor.compress(nested)

        assert compressed["type_field"].startswith("@")                              # Type field compressed
        assert compressed["values"]["key"] == 123                                    # Dict values preserved

        decompressed = self.compressor.decompress(compressed)
        assert decompressed == nested.json()                                                  # Round trip works

    def test_edge_cases(self):
        assert self.compressor.compress({})    == {}                               # Empty dict unchanged
        assert self.compressor.compress(None)  is None                             # None unchanged
        assert self.compressor.decompress({})  == {}                               # Empty dict unchanged
        assert self.compressor.decompress(None) is None                            # None unchanged
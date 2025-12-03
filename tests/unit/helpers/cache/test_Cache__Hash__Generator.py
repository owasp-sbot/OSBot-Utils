import pytest
from unittest                                                                            import TestCase
from osbot_utils.helpers.cache.Cache__Hash__Generator                                    import Cache__Hash__Generator
from osbot_utils.helpers.cache.schemas.Schema__Cache__Hash__Config                       import Schema__Cache__Hash__Config
from osbot_utils.type_safe.primitives.domains.cryptography.enums.Enum__Hash__Algorithm   import Enum__Hash__Algorithm
from osbot_utils.utils.Objects                                                           import base_classes
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash import Safe_Str__Cache_Hash
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe

class test_Cache__Hash__Generator(TestCase):

    @classmethod
    def setUpClass(cls):                                                          # ONE-TIME setup
        cls.test_data_string = "test data for hashing"
        cls.test_data_bytes  = b"test binary data"
        cls.test_data_json   = {"key": "value", "number": 123}

    def test__init__(self):                                                       # Test auto-initialization
        with Cache__Hash__Generator() as _:
            assert type(_)         is Cache__Hash__Generator
            assert base_classes(_) == [Type_Safe, object]
            assert type(_.config)  is Schema__Cache__Hash__Config

    def test_calculate(self):                                                     # Test hash calculation from bytes
        config = Schema__Cache__Hash__Config(algorithm=Enum__Hash__Algorithm.SHA256, length=16)

        with Cache__Hash__Generator(config=config) as _:
            hash_value = _.calculate(self.test_data_bytes)

            assert type(hash_value) is Safe_Str__Cache_Hash
            assert len(str(hash_value)) == 16                                     # Respects configured length
            assert str(hash_value)      == '16abf9af4643ff1e'                         # Deterministic hash

    def test_calculate__different_algorithms(self):                               # Test different hash algorithms
        test_bytes = b"consistent test data"

        # MD5
        with Cache__Hash__Generator(config=Schema__Cache__Hash__Config(algorithm=Enum__Hash__Algorithm.MD5, length=16)) as _:
            md5_hash = _.calculate(test_bytes)
            assert str(md5_hash) == '3a5cc7ecc54391c1'

        # SHA256
        with Cache__Hash__Generator(config=Schema__Cache__Hash__Config(algorithm=Enum__Hash__Algorithm.SHA256, length=16)) as _:
            sha256_hash = _.calculate(test_bytes)
            assert str(sha256_hash) == 'e43f79d59675519b'

        # SHA384
        with Cache__Hash__Generator(config=Schema__Cache__Hash__Config(algorithm=Enum__Hash__Algorithm.SHA384, length=16)) as _:
            sha384_hash = _.calculate(test_bytes)
            assert str(sha384_hash) == '3a96372953d9062f'

        # Different algorithms produce different hashes
        assert md5_hash != sha256_hash != sha384_hash

    def test_calculate__different_lengths(self):                                  # Test configurable hash lengths
        config_10 = Schema__Cache__Hash__Config(length=10)
        config_32 = Schema__Cache__Hash__Config(length=32)
        config_64 = Schema__Cache__Hash__Config(length=64)

        with Cache__Hash__Generator(config=config_10) as gen_10:
            hash_10 = gen_10.calculate(self.test_data_bytes)
            assert len(str(hash_10)) == 10

        with Cache__Hash__Generator(config=config_32) as gen_32:
            hash_32 = gen_32.calculate(self.test_data_bytes)
            assert len(str(hash_32)) == 32

        with Cache__Hash__Generator(config=config_64) as gen_64:
            hash_64 = gen_64.calculate(self.test_data_bytes)
            assert len(str(hash_64)) == 64

    def test_from_string(self):                                                   # Test hash from string
        with Cache__Hash__Generator(config=Schema__Cache__Hash__Config(length=16)) as _:
            hash_value = _.from_string(self.test_data_string)

            assert type(hash_value) is Safe_Str__Cache_Hash
            assert str(hash_value) == 'f7eb7961d8a233e6'                         # Deterministic

    def test_from_bytes(self):                                                    # Test hash from bytes
        with Cache__Hash__Generator(config=Schema__Cache__Hash__Config(length=16)) as _:
            hash_value = _.from_bytes(self.test_data_bytes)

            assert type(hash_value) is Safe_Str__Cache_Hash
            assert str(hash_value) == '16abf9af4643ff1e'

    def test_from_json(self):                                                     # Test hash from JSON
        with Cache__Hash__Generator(config=Schema__Cache__Hash__Config(length=16)) as _:
            hash_value = _.from_json(self.test_data_json)

            assert type(hash_value) is Safe_Str__Cache_Hash
            assert len(str(hash_value)) == 16

            # Same JSON produces same hash
            hash_value_2 = _.from_json({"number": 123, "key": "value"})             # Different order
            assert hash_value == hash_value_2                                       # But same hash (sorted)

    def test_from_json__with_exclusions(self):                                      # Test field exclusion
        data_with_timestamp = {"key": "value", "timestamp": "2024-01-01", "id": "123"}

        with Cache__Hash__Generator(config=Schema__Cache__Hash__Config(length=16)) as _:
            # Hash without exclusions
            hash_full = _.from_json(data_with_timestamp)

            # Hash with timestamp excluded
            hash_no_timestamp = _.from_json(data_with_timestamp, exclude_fields=["timestamp"])

            # Hash with both timestamp and id excluded
            hash_minimal = _.from_json(data_with_timestamp, exclude_fields=["timestamp", "id"])

            # All different hashes
            assert hash_full != hash_no_timestamp != hash_minimal

            # Excluding non-existent field doesn't affect hash
            hash_same = _.from_json(data_with_timestamp, exclude_fields=["nonexistent"])
            assert hash_same == hash_full

    def test_from_type_safe(self):                                                # Test hash from Type_Safe object
        class TestSchema(Type_Safe):
            field1: str = "value1"
            field2: int = 42

        test_obj = TestSchema()

        with Cache__Hash__Generator(config=Schema__Cache__Hash__Config(length=16)) as _:
            hash_value = _.from_type_safe(test_obj)

            assert type(hash_value) is Safe_Str__Cache_Hash

            # Same object produces same hash
            test_obj_2 = TestSchema()
            hash_value_2 = _.from_type_safe(test_obj_2)
            assert hash_value == hash_value_2

    def test_from_type_safe__with_exclusions(self):                              # Test Type_Safe with field exclusion
        class TestSchema(Type_Safe):
            id       : str = "unique-id"
            data     : str = "important"
            timestamp: str = "2024-01-01"

        test_obj = TestSchema()

        with Cache__Hash__Generator(config=Schema__Cache__Hash__Config(length=16)) as _:
            hash_full = _.from_type_safe(test_obj)
            hash_no_id = _.from_type_safe(test_obj, exclude_fields=["id", "timestamp"])

            assert hash_full != hash_no_id                                          # Different hashes

    def test_from_json_field__simple_field(self):                                   # Test hashing from a simple string field.
        generator = Cache__Hash__Generator(config=Schema__Cache__Hash__Config())

        data = { "url": "https://example.com",
                 "name": "Example Site"      }

        hash_from_field = generator.from_json_field(data, json_field="url")         # Hash from URL field

        hash_from_string = generator.from_string("https://example.com")             # Hash from URL string directly

        assert hash_from_field == hash_from_string                                  # Should match

    def test_from_json_field__nested_field(self):                                   # Test hashing from nested field using dot notation.
        generator = Cache__Hash__Generator(config=Schema__Cache__Hash__Config())

        data = {    "metadata": { "version": "1.0.0",
                                   "author": "test" } }

        hash_result = generator.from_json_field(data, json_field="metadata.version")
        expected = generator.from_string("1.0.0")

        assert hash_result == expected

    def test_from_json_field__missing_field(self):                                  # Test error handling for missing field.
        generator = Cache__Hash__Generator(config=Schema__Cache__Hash__Config())

        data = {"name": "Example"}

        with pytest.raises(ValueError, match="Field 'url' not found"):
            generator.from_json_field(data, json_field="url")

    def test_from_json__values_consistency(self):
        with Cache__Hash__Generator() as _:
            data_1 = {"Answer": 42 }
            data_2 = {"Answer": 43 }
            assert _.from_json      (data_1)                      == 'a67c5a4568211ec5'
            assert _.from_json_field(data_1, json_field='Answer') == '73475cb40a568e8d'
            assert _.from_json      (data_2)                      == 'e92ec70711870c51'
            assert _.from_json_field(data_2, json_field='Answer') == '44cb730c420480a0'


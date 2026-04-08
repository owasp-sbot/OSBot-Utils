# ═══════════════════════════════════════════════════════════════════════════════
# Tests: Type_Safe__Fast_Create__Cache - Schema Generation and Caching
# Verify schema generation, field classification, and cache behavior
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                  import Dict, List
from unittest                                import TestCase
from Type_Safe__Hypothesis_G                 import Type_Safe__Hypothesis_G
from Type_Safe__Fast_Create__Cache           import type_safe_fast_create_cache
from schemas.Field__Schema                   import FIELD_MODE__STATIC
from schemas.Field__Schema                   import FIELD_MODE__NESTED


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Simple(Type_Safe__Hypothesis_G):
    name   : str  = ''
    count  : int  = 0
    active : bool = False


class TS__With_Collections(Type_Safe__Hypothesis_G):
    name  : str = ''
    items : List[str]
    data  : Dict[str, int]


class TS__Inner(Type_Safe__Hypothesis_G):
    value : str = ''
    count : int = 0


class TS__With_Nested(Type_Safe__Hypothesis_G):
    inner : TS__Inner
    name  : str = ''


class TS__Deep_Level2(Type_Safe__Hypothesis_G):
    data : str = ''


class TS__Deep_Level1(Type_Safe__Hypothesis_G):
    level2 : TS__Deep_Level2
    name   : str = ''


class TS__Deep(Type_Safe__Hypothesis_G):
    level1 : TS__Deep_Level1
    count  : int = 0


# ═══════════════════════════════════════════════════════════════════════════════
# Immutability Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_is_immutable(TestCase):

    def test__immutable_types(self):
        cache = type_safe_fast_create_cache

        assert cache.is_immutable('')        is True
        assert cache.is_immutable('hello')   is True
        assert cache.is_immutable(0)         is True
        assert cache.is_immutable(42)        is True
        assert cache.is_immutable(3.14)      is True
        assert cache.is_immutable(True)      is True
        assert cache.is_immutable(False)     is True
        assert cache.is_immutable(None)      is True
        assert cache.is_immutable(b'bytes')  is True
        assert cache.is_immutable((1, 2, 3)) is True

    def test__mutable_types(self):
        cache = type_safe_fast_create_cache

        assert cache.is_immutable([])        is False
        assert cache.is_immutable({})        is False
        assert cache.is_immutable(set())     is False
        assert cache.is_immutable([1, 2, 3]) is False


# ═══════════════════════════════════════════════════════════════════════════════
# Schema Generation Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_generate_schema(TestCase):

    def setUp(self):
        type_safe_fast_create_cache.clear_cache()

    def test__simple_class__all_static(self):
        schema = type_safe_fast_create_cache.generate_schema(TS__Simple)

        assert schema.target_class is TS__Simple
        assert len(schema.fields)  == 3

        for field in schema.fields:
            assert field.mode == FIELD_MODE__STATIC

        assert schema.static_dict['name']   == ''
        assert schema.static_dict['count']  == 0
        assert schema.static_dict['active'] == False

    def test__class_with_collections__factory_fields(self):
        schema = type_safe_fast_create_cache.generate_schema(TS__With_Collections)

        assert 'name' in schema.static_dict                                       # Static field

        assert len(schema.factory_fields) == 2                                    # items and data
        factory_names = {f.name for f in schema.factory_fields}
        assert factory_names == {'items', 'data'}

    def test__class_with_nested__nested_fields(self):
        schema = type_safe_fast_create_cache.generate_schema(TS__With_Nested)

        assert len(schema.nested_fields)    == 1
        assert schema.nested_fields[0].name == 'inner'
        assert schema.nested_fields[0].mode == FIELD_MODE__NESTED
        assert schema.nested_fields[0].nested_class is TS__Inner

    def test__deep_nested_class(self):
        schema = type_safe_fast_create_cache.generate_schema(TS__Deep)

        assert len(schema.nested_fields)                == 1
        assert schema.nested_fields[0].name             == 'level1'
        assert schema.nested_fields[0].nested_class is TS__Deep_Level1


# ═══════════════════════════════════════════════════════════════════════════════
# Cache Behavior Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_schema_cache(TestCase):

    def setUp(self):
        type_safe_fast_create_cache.clear_cache()

    def test__schema_is_cached(self):
        schema1 = type_safe_fast_create_cache.get_schema(TS__Simple)
        schema2 = type_safe_fast_create_cache.get_schema(TS__Simple)

        assert schema1 is schema2                                                 # Same instance

    def test__warm_cache__recursive(self):
        type_safe_fast_create_cache.clear_cache()
        type_safe_fast_create_cache.warm_cache(TS__Deep)

        assert TS__Deep        in type_safe_fast_create_cache.schema_cache
        assert TS__Deep_Level1 in type_safe_fast_create_cache.schema_cache
        assert TS__Deep_Level2 in type_safe_fast_create_cache.schema_cache

    def test__clear_cache(self):
        type_safe_fast_create_cache.get_schema(TS__Simple)
        assert len(type_safe_fast_create_cache.schema_cache) > 0

        type_safe_fast_create_cache.clear_cache()
        assert len(type_safe_fast_create_cache.schema_cache) == 0


# ═══════════════════════════════════════════════════════════════════════════════
# Factory Function Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_factory_functions(TestCase):

    def setUp(self):
        type_safe_fast_create_cache.clear_cache()

    def test__factory_creates_fresh_instances(self):
        schema = type_safe_fast_create_cache.get_schema(TS__With_Collections)

        items_field = next(f for f in schema.factory_fields if f.name == 'items')

        instance1 = items_field.factory_func()
        instance2 = items_field.factory_func()

        assert instance1 is not instance2                                         # Different instances

    def test__type_safe_list_preserves_expected_type(self):
        schema = type_safe_fast_create_cache.get_schema(TS__With_Collections)

        items_field = next(f for f in schema.factory_fields if f.name == 'items')
        items       = items_field.factory_func()

        assert items.expected_type is str
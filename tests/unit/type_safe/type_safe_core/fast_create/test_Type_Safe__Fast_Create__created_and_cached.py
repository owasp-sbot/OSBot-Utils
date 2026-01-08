# ═══════════════════════════════════════════════════════════════════════════════
# Tests: Type_Safe Fast Create - Created and Cached
# These tests verify MECHANISM - they FAIL without Type_Safe wiring in place
# ═══════════════════════════════════════════════════════════════════════════════
#
# PURPOSE: Verify that fast_create is ACTUALLY BEING USED by checking:
#   - Schema cache is populated after creation
#   - Schema cache is NOT populated when fast_create=False
#   - Cache warming works via creation
#   - Nested class schemas are cached recursively
#
# REQUIRES: Type_Safe wiring in place:
#   - Type_Safe.__init__ checks config.fast_create and delegates to fast_create
#   - Type_Safe.__setattr__ checks config.skip_validation
#
# WITHOUT WIRING: All tests in this file should FAIL (cache never populated)
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                         import Dict, List
from unittest                                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                                  import Type_Safe__Config
from osbot_utils.type_safe.type_safe_core.fast_create.Type_Safe__Fast_Create__Cache                 import type_safe_fast_create_cache


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Simple(Type_Safe):
    name   : str  = ''
    count  : int  = 0
    active : bool = False


class TS__With_Collections(Type_Safe):
    name  : str = ''
    items : List[str]
    data  : Dict[str, int]


class TS__Inner(Type_Safe):
    value : str = ''
    count : int = 0


class TS__With_Nested(Type_Safe):
    inner : TS__Inner
    name  : str = ''


class TS__Deep_Level3(Type_Safe):
    data : str = ''


class TS__Deep_Level2(Type_Safe):
    level3 : TS__Deep_Level3
    value  : int = 0


class TS__Deep_Level1(Type_Safe):
    level2 : TS__Deep_Level2
    name   : str = ''


class TS__Deep(Type_Safe):
    level1 : TS__Deep_Level1
    count  : int = 0


# ═══════════════════════════════════════════════════════════════════════════════
# Test: Created and Cached (Mechanism Verification)
# ═══════════════════════════════════════════════════════════════════════════════

class test_Type_Safe__Fast_Create__created_and_cached(TestCase):
    """
    These tests verify that fast_create mechanism is actually being invoked.
    They check cache state which only changes when fast_create path is used.

    WITHOUT WIRING: All these tests FAIL because cache is never populated.
    WITH WIRING:    All these tests PASS.
    """

    def setUp(self):
        type_safe_fast_create_cache.clear_cache()

    # ───────────────────────────────────────────────────────────────────────────
    # Basic Cache Population
    # ───────────────────────────────────────────────────────────────────────────

    def test__fast_create__populates_cache_for_simple_class(self):                # Schema cached on first use
        assert TS__Simple not in type_safe_fast_create_cache.schema_cache         # Empty before

        with Type_Safe__Config(fast_create=True):
            _ = TS__Simple()

        assert TS__Simple in type_safe_fast_create_cache.schema_cache             # Cached after

    def test__fast_create__populates_cache_for_collections_class(self):           # Collections class cached
        assert TS__With_Collections not in type_safe_fast_create_cache.schema_cache

        with Type_Safe__Config(fast_create=True):
            _ = TS__With_Collections()

        assert TS__With_Collections in type_safe_fast_create_cache.schema_cache

    def test__fast_create__populates_cache_for_nested_class(self):                # Parent class cached
        assert TS__With_Nested not in type_safe_fast_create_cache.schema_cache

        with Type_Safe__Config(fast_create=True):
            _ = TS__With_Nested()

        assert TS__With_Nested in type_safe_fast_create_cache.schema_cache

    # ───────────────────────────────────────────────────────────────────────────
    # Recursive Cache Population (Nested Classes)
    # ───────────────────────────────────────────────────────────────────────────

    def test__fast_create__caches_nested_class_recursively(self):                 # Inner class also cached
        assert TS__With_Nested not in type_safe_fast_create_cache.schema_cache
        assert TS__Inner       not in type_safe_fast_create_cache.schema_cache

        with Type_Safe__Config(fast_create=True):
            _ = TS__With_Nested()

        assert TS__With_Nested in type_safe_fast_create_cache.schema_cache
        assert TS__Inner       in type_safe_fast_create_cache.schema_cache        # Also cached!

    def test__fast_create__caches_deep_nested_classes_recursively(self):          # All levels cached
        assert TS__Deep        not in type_safe_fast_create_cache.schema_cache
        assert TS__Deep_Level1 not in type_safe_fast_create_cache.schema_cache
        assert TS__Deep_Level2 not in type_safe_fast_create_cache.schema_cache
        assert TS__Deep_Level3 not in type_safe_fast_create_cache.schema_cache

        with Type_Safe__Config(fast_create=True):
            _ = TS__Deep()

        assert TS__Deep        in type_safe_fast_create_cache.schema_cache        # Level 0
        assert TS__Deep_Level1 in type_safe_fast_create_cache.schema_cache        # Level 1
        assert TS__Deep_Level2 in type_safe_fast_create_cache.schema_cache        # Level 2
        assert TS__Deep_Level3 in type_safe_fast_create_cache.schema_cache        # Level 3

    # ───────────────────────────────────────────────────────────────────────────
    # Cache NOT Populated Without fast_create
    # ───────────────────────────────────────────────────────────────────────────

    def test__normal_mode__does_not_populate_cache(self):                         # Normal creation skips cache
        assert TS__Simple not in type_safe_fast_create_cache.schema_cache

        _ = TS__Simple()                                                          # Normal creation (no config)

        assert TS__Simple not in type_safe_fast_create_cache.schema_cache         # Still empty!

    def test__fast_create_false__does_not_populate_cache(self):                   # Explicit False skips cache
        assert TS__Simple not in type_safe_fast_create_cache.schema_cache

        with Type_Safe__Config(fast_create=False):
            _ = TS__Simple()

        assert TS__Simple not in type_safe_fast_create_cache.schema_cache         # Still empty!

    # ───────────────────────────────────────────────────────────────────────────
    # Multiple Creations Use Same Cached Schema
    # ───────────────────────────────────────────────────────────────────────────

    def test__fast_create__second_creation_uses_cached_schema(self):              # Cache hit on second create
        with Type_Safe__Config(fast_create=True):
            _ = TS__Simple()

        schema_after_first = type_safe_fast_create_cache.schema_cache.get(TS__Simple)
        assert schema_after_first is not None

        with Type_Safe__Config(fast_create=True):
            _ = TS__Simple()

        schema_after_second = type_safe_fast_create_cache.schema_cache.get(TS__Simple)
        assert schema_after_second is schema_after_first                          # Same instance!

    def test__fast_create__batch_creation_uses_same_schema(self):                 # All batch objects use same schema
        with Type_Safe__Config(fast_create=True):
            _ = TS__Simple()

        schema = type_safe_fast_create_cache.schema_cache.get(TS__Simple)
        assert schema is not None

        cache_size_after_one = len(type_safe_fast_create_cache.schema_cache)

        with Type_Safe__Config(fast_create=True):
            for _ in range(100):
                _ = TS__Simple()

        # Cache size unchanged - all used same schema
        assert len(type_safe_fast_create_cache.schema_cache) == cache_size_after_one
        assert type_safe_fast_create_cache.schema_cache.get(TS__Simple) is schema

    # ───────────────────────────────────────────────────────────────────────────
    # Schema Content Verification
    # ───────────────────────────────────────────────────────────────────────────

    def test__fast_create__cached_schema_has_correct_target_class(self):          # Schema points to right class
        with Type_Safe__Config(fast_create=True):
            _ = TS__Simple()

        schema = type_safe_fast_create_cache.schema_cache.get(TS__Simple)
        assert schema.target_class is TS__Simple

    def test__fast_create__cached_schema_has_correct_fields(self):                # Schema has all fields
        with Type_Safe__Config(fast_create=True):
            _ = TS__Simple()

        schema = type_safe_fast_create_cache.schema_cache.get(TS__Simple)
        field_names = {f.name for f in schema.fields}

        assert 'name'   in field_names
        assert 'count'  in field_names
        assert 'active' in field_names

    def test__fast_create__cached_schema_has_static_dict(self):                   # Schema has pre-built static_dict
        with Type_Safe__Config(fast_create=True):
            _ = TS__Simple()

        schema = type_safe_fast_create_cache.schema_cache.get(TS__Simple)

        assert 'name'   in schema.static_dict
        assert 'count'  in schema.static_dict
        assert 'active' in schema.static_dict
        assert schema.static_dict['name']   == ''
        assert schema.static_dict['count']  == 0
        assert schema.static_dict['active'] is False

    def test__fast_create__cached_schema_has_factory_fields(self):                # Collections have factory funcs
        with Type_Safe__Config(fast_create=True):
            _ = TS__With_Collections()

        schema = type_safe_fast_create_cache.schema_cache.get(TS__With_Collections)

        factory_names = {f.name for f in schema.factory_fields}
        assert 'items' in factory_names
        assert 'data'  in factory_names

    def test__fast_create__cached_schema_has_nested_fields(self):                 # Nested fields identified
        with Type_Safe__Config(fast_create=True):
            _ = TS__With_Nested()

        schema = type_safe_fast_create_cache.schema_cache.get(TS__With_Nested)

        assert len(schema.nested_fields)    == 1
        assert schema.nested_fields[0].name == 'inner'
        assert schema.nested_fields[0].nested_class is TS__Inner

    # ───────────────────────────────────────────────────────────────────────────
    # Cache State After Context Exit
    # ───────────────────────────────────────────────────────────────────────────

    def test__fast_create__cache_persists_after_context_exit(self):               # Cache survives context
        with Type_Safe__Config(fast_create=True):
            _ = TS__Simple()

        # Outside context - cache still has schema
        assert TS__Simple in type_safe_fast_create_cache.schema_cache

    def test__fast_create__cache_persists_across_multiple_contexts(self):         # Cache shared across contexts
        with Type_Safe__Config(fast_create=True):
            _ = TS__Simple()

        schema_from_first = type_safe_fast_create_cache.schema_cache.get(TS__Simple)

        with Type_Safe__Config(fast_create=True):
            _ = TS__Simple()

        schema_from_second = type_safe_fast_create_cache.schema_cache.get(TS__Simple)

        assert schema_from_first is schema_from_second                            # Same schema object

    # ───────────────────────────────────────────────────────────────────────────
    # Mixed Usage: Some With fast_create, Some Without
    # ───────────────────────────────────────────────────────────────────────────

    def test__mixed_usage__fast_create_populates_normal_does_not(self):           # Only fast path caches
        # Normal creation - no cache
        _ = TS__Simple()
        assert TS__Simple not in type_safe_fast_create_cache.schema_cache

        # Fast creation - populates cache
        with Type_Safe__Config(fast_create=True):
            _ = TS__With_Collections()

        assert TS__Simple           not in type_safe_fast_create_cache.schema_cache  # Still not cached
        assert TS__With_Collections in     type_safe_fast_create_cache.schema_cache  # Now cached

    def test__mixed_usage__different_classes_cached_independently(self):          # Each class cached separately
        with Type_Safe__Config(fast_create=True):
            _ = TS__Simple()

        assert TS__Simple           in     type_safe_fast_create_cache.schema_cache
        assert TS__With_Collections not in type_safe_fast_create_cache.schema_cache

        with Type_Safe__Config(fast_create=True):
            _ = TS__With_Collections()

        assert TS__Simple           in type_safe_fast_create_cache.schema_cache
        assert TS__With_Collections in type_safe_fast_create_cache.schema_cache
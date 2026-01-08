# ═══════════════════════════════════════════════════════════════════════════════
# Tests: Type_Safe Fast Create - Created With No Side Effects
# These tests verify CORRECTNESS - they pass regardless of which code path is used
# ═══════════════════════════════════════════════════════════════════════════════
#
# PURPOSE: Verify that objects created with fast_create=True have correct:
#   - Field values (defaults and kwargs)
#   - Object types (isinstance, type)
#   - Behavior (json, attribute access)
#   - Independence (collections, nested objects not shared)
#
# NOTE: These tests pass even WITHOUT wiring because they verify behavior,
#       not mechanism. The normal Type_Safe path produces identical results.
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                         import Dict, List, Optional
from unittest                                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                                  import Type_Safe__Config
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                                  import get_active_config
from osbot_utils.type_safe.type_safe_core.fast_create.Type_Safe__Fast_Create__Cache                 import type_safe_fast_create_cache


# ═══════════════════════════════════════════════════════════════════════════════
# Test: Created With No Side Effects
# ═══════════════════════════════════════════════════════════════════════════════

class test_Type_Safe__Fast_Create__created_with_no_side_effects(TestCase):

    def setUp(self):
        type_safe_fast_create_cache.clear_cache()

    # ───────────────────────────────────────────────────────────────────────────
    # Normal Mode (Baseline)
    # ───────────────────────────────────────────────────────────────────────────

    def test__normal_mode__creates_with_defaults(self):                           # Default behavior unchanged
        with TS__Simple() as _:
            assert type(_)   is TS__Simple
            assert _.name    == ''
            assert _.count   == 0
            assert _.active  is False

    def test__normal_mode__creates_with_kwargs(self):                             # kwargs work normally
        with TS__Simple(name='test', count=42) as _:
            assert _.name  == 'test'
            assert _.count == 42

    def test__normal_mode__nested_created(self):                                  # Nested objects created
        with TS__With_Nested() as _:
            assert _.inner        is not None
            assert type(_.inner)  is TS__Inner

    # ───────────────────────────────────────────────────────────────────────────
    # Fast Create Mode - Basic Creation
    # ───────────────────────────────────────────────────────────────────────────

    def test__fast_create__empty_class(self):                                     # Edge case: no fields
        with Type_Safe__Config(fast_create=True):
            with TS__Empty() as _:
                assert type(_) is TS__Empty

    def test__fast_create__simple_class(self):                                    # Static fields only
        with Type_Safe__Config(fast_create=True):
            with TS__Simple() as _:
                assert type(_)   is TS__Simple
                assert _.name    == ''
                assert _.count   == 0
                assert _.active  is False
                assert _.value   == 0.0

    def test__fast_create__with_non_empty_defaults(self):                         # Non-empty defaults preserved
        with Type_Safe__Config(fast_create=True):
            with TS__With_Defaults() as _:
                assert _.name    == 'default_name'
                assert _.count   == 42
                assert _.enabled is True

    def test__fast_create__with_optional_none(self):                              # Optional fields work
        with Type_Safe__Config(fast_create=True):
            with TS__With_Optional() as _:
                assert _.required == ''
                assert _.optional is None

    # ───────────────────────────────────────────────────────────────────────────
    # Fast Create Mode - kwargs Override
    # ───────────────────────────────────────────────────────────────────────────

    def test__fast_create__kwargs_applied(self):                                  # kwargs override defaults
        with Type_Safe__Config(fast_create=True):
            with TS__Simple(name='fast', count=99) as _:
                assert _.name   == 'fast'
                assert _.count  == 99
                assert _.active is False                                          # Default kept

    def test__fast_create__kwargs_all_fields(self):                               # Override all fields
        with Type_Safe__Config(fast_create=True):
            with TS__Simple(name='a', count=1, active=True, value=3.14) as _:
                assert _.name   == 'a'
                assert _.count  == 1
                assert _.active is True
                assert _.value  == 3.14

    # ───────────────────────────────────────────────────────────────────────────
    # Fast Create Mode - Collections
    # ───────────────────────────────────────────────────────────────────────────

    def test__fast_create__list_created(self):                                    # List field created
        with Type_Safe__Config(fast_create=True):
            with TS__With_List() as _:
                assert _.items is not None
                assert len(_.items) == 0

    def test__fast_create__dict_created(self):                                    # Dict field created
        with Type_Safe__Config(fast_create=True):
            with TS__With_Dict() as _:
                assert _.data is not None
                assert len(_.data) == 0

    def test__fast_create__collections_independent(self):                         # Each instance gets fresh collections
        with Type_Safe__Config(fast_create=True):
            obj1 = TS__With_Collections()
            obj2 = TS__With_Collections()

        obj1.items.append('item1')
        obj1.data['key'] = 42

        assert len(obj1.items)   == 1
        assert len(obj2.items)   == 0                                             # Independent!
        assert len(obj1.data)    == 1
        assert len(obj2.data)    == 0                                             # Independent!

    # ───────────────────────────────────────────────────────────────────────────
    # Fast Create Mode - Nested Objects
    # ───────────────────────────────────────────────────────────────────────────

    def test__fast_create__nested_created(self):                                  # Nested object created
        with Type_Safe__Config(fast_create=True):
            with TS__With_Nested() as _:
                assert _.inner        is not None
                assert type(_.inner)  is TS__Inner
                assert _.inner.value  == ''
                assert _.inner.count  == 0

    def test__fast_create__multiple_nested_created(self):                         # All nested objects created
        with Type_Safe__Config(fast_create=True):
            with TS__With_Multiple_Nested() as _:
                assert type(_.child1) is TS__Inner
                assert type(_.child2) is TS__Inner
                assert type(_.child3) is TS__Inner

    def test__fast_create__nested_independent(self):                              # Each instance gets fresh nested
        with Type_Safe__Config(fast_create=True):
            obj1 = TS__With_Nested()
            obj2 = TS__With_Nested()

        obj1.inner.value = 'modified'

        assert obj1.inner.value == 'modified'
        assert obj2.inner.value == ''                                             # Independent!

    def test__fast_create__multiple_nested_independent_within_instance(self):     # Nested within same instance independent
        with Type_Safe__Config(fast_create=True):
            with TS__With_Multiple_Nested() as _:
                _.child1.value = 'child1_value'

                assert _.child1.value == 'child1_value'
                assert _.child2.value == ''                                       # Independent!
                assert _.child3.value == ''                                       # Independent!

    # ───────────────────────────────────────────────────────────────────────────
    # Fast Create Mode - Deep Nesting
    # ───────────────────────────────────────────────────────────────────────────

    def test__fast_create__deep_nested_created(self):                             # 3 levels of nesting
        with Type_Safe__Config(fast_create=True):
            with TS__Deep() as _:
                assert _.level1                      is not None
                assert _.level1.level2               is not None
                assert _.level1.level2.level3        is not None
                assert type(_.level1)                is TS__Deep_Level1
                assert type(_.level1.level2)         is TS__Deep_Level2
                assert type(_.level1.level2.level3)  is TS__Deep_Level3

    def test__fast_create__deep_nested_values_initialized(self):                  # All levels have correct defaults
        with Type_Safe__Config(fast_create=True):
            with TS__Deep() as _:
                assert _.count                      == 0
                assert _.level1.name                == ''
                assert _.level1.level2.value        == 0
                assert _.level1.level2.level3.data  == ''

    # ───────────────────────────────────────────────────────────────────────────
    # Fast Create Mode - Mixed Field Types
    # ───────────────────────────────────────────────────────────────────────────

    def test__fast_create__mixed_all_fields_created(self):                        # Static + Factory + Nested
        with Type_Safe__Config(fast_create=True):
            with TS__Mixed() as _:
                assert _.name         == ''                                       # Static
                assert len(_.items)   == 0                                        # Factory (list)
                assert len(_.data)    == 0                                        # Factory (dict)
                assert type(_.inner)  is TS__Inner                                # Nested

    def test__fast_create__complex_real_world(self):                              # Simulates real usage
        with Type_Safe__Config(fast_create=True):
            with TS__Complex(node_id='node_001', value=100) as _:
                assert _.node_id      == 'node_001'
                assert _.value        == 100
                assert len(_.tags)    == 0
                assert len(_.meta)    == 0
                assert type(_.child)  is TS__Inner

    # ───────────────────────────────────────────────────────────────────────────
    # Object Usability After Fast Create
    # ───────────────────────────────────────────────────────────────────────────

    def test__fast_create__isinstance_works(self):                                # isinstance() returns True
        with Type_Safe__Config(fast_create=True):
            obj = TS__Simple()

        assert isinstance(obj, TS__Simple)
        assert isinstance(obj, Type_Safe)

    def test__fast_create__type_check_works(self):                                # type() returns correct class
        with Type_Safe__Config(fast_create=True):
            obj = TS__Simple()

        assert type(obj) is TS__Simple

    def test__fast_create__attribute_read_works(self):                            # Can read attributes
        with Type_Safe__Config(fast_create=True):
            obj = TS__Simple(name='readable')

        assert obj.name == 'readable'

    def test__fast_create__attribute_write_works(self):                           # Can write attributes
        with Type_Safe__Config(fast_create=True):
            obj = TS__Simple()

        obj.name = 'written'
        assert obj.name == 'written'

    def test__fast_create__json_works(self):                                      # json() method works
        with Type_Safe__Config(fast_create=True):
            obj = TS__Simple(name='json_test', count=42)

        json_data = obj.json()

        assert json_data['name']   == 'json_test'
        assert json_data['count']  == 42
        assert json_data['active'] is False
        assert json_data['value']  == 0.0

    def test__fast_create__json_nested_works(self):                               # Nested objects serialize
        with Type_Safe__Config(fast_create=True):
            obj = TS__With_Nested(name='parent')

        obj.inner.value = 'inner_value'
        json_data = obj.json()

        assert json_data['name']           == 'parent'
        assert json_data['inner']['value'] == 'inner_value'
        assert json_data['inner']['count'] == 0

    def test__fast_create__json_deep_nested_works(self):                          # Deep nesting serializes
        with Type_Safe__Config(fast_create=True):
            obj = TS__Deep()

        obj.level1.level2.level3.data = 'deep_value'
        json_data = obj.json()

        assert json_data['level1']['level2']['level3']['data'] == 'deep_value'

    # ───────────────────────────────────────────────────────────────────────────
    # Skip Validation
    # ───────────────────────────────────────────────────────────────────────────

    def test__skip_validation__setattr_works(self):                               # Can set attributes with skip
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj      = TS__Simple()
            obj.name = 'updated'

        assert obj.name == 'updated'

    def test__skip_validation__multiple_setattr(self):                            # Multiple assignments work
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj        = TS__Simple()
            obj.name   = 'first'
            obj.name   = 'second'
            obj.count  = 100
            obj.active = True

        assert obj.name   == 'second'
        assert obj.count  == 100
        assert obj.active is True

    def test__without_skip_validation__setattr_still_works(self):                 # Normal validation path
        with Type_Safe__Config(fast_create=True, skip_validation=False):
            obj      = TS__Simple()
            obj.name = 'validated'

        assert obj.name == 'validated'

    # ───────────────────────────────────────────────────────────────────────────
    # Config Context Behavior
    # ───────────────────────────────────────────────────────────────────────────

    def test__config__only_active_in_context(self):                               # Config scoped to context
        assert get_active_config() is None                                        # No config outside

        with Type_Safe__Config(fast_create=True):
            config = get_active_config()
            assert config is not None
            assert config.fast_create is True

        assert get_active_config() is None                                        # Restored to None

    def test__config__nested_contexts(self):                                      # Inner context takes precedence
        with Type_Safe__Config(fast_create=True, skip_validation=False):
            outer_config = get_active_config()
            assert outer_config.skip_validation is False

            with Type_Safe__Config(fast_create=True, skip_validation=True):
                inner_config = get_active_config()
                assert inner_config.skip_validation is True                       # Inner overrides

            restored_config = get_active_config()
            assert restored_config.skip_validation is False                       # Outer restored

    def test__config__exception_still_restores(self):                             # Config restored on exception
        try:
            with Type_Safe__Config(fast_create=True):
                assert get_active_config() is not None
                raise ValueError("test exception")
        except ValueError:
            pass

        assert get_active_config() is None                                        # Restored despite exception

    # ───────────────────────────────────────────────────────────────────────────
    # Equivalence: Normal vs Fast Create
    # ───────────────────────────────────────────────────────────────────────────

    def test__equivalence__simple_class(self):                                    # Same result both paths
        normal_obj = TS__Simple(name='test', count=42)

        with Type_Safe__Config(fast_create=True):
            fast_obj = TS__Simple(name='test', count=42)

        assert normal_obj.name   == fast_obj.name
        assert normal_obj.count  == fast_obj.count
        assert normal_obj.active == fast_obj.active
        assert normal_obj.value  == fast_obj.value

    def test__equivalence__with_defaults(self):                                   # Defaults same both paths
        normal_obj = TS__With_Defaults()

        with Type_Safe__Config(fast_create=True):
            fast_obj = TS__With_Defaults()

        assert normal_obj.name    == fast_obj.name
        assert normal_obj.count   == fast_obj.count
        assert normal_obj.enabled == fast_obj.enabled

    def test__equivalence__nested_structure(self):                                # Nested structure same
        normal_obj = TS__With_Nested(name='parent')

        with Type_Safe__Config(fast_create=True):
            fast_obj = TS__With_Nested(name='parent')

        assert type(normal_obj.inner) is type(fast_obj.inner)
        assert normal_obj.inner.value == fast_obj.inner.value
        assert normal_obj.inner.count == fast_obj.inner.count

    def test__equivalence__deep_nested_structure(self):                           # Deep nesting same
        normal_obj = TS__Deep()

        with Type_Safe__Config(fast_create=True):
            fast_obj = TS__Deep()

        assert type(normal_obj.level1)                is type(fast_obj.level1)
        assert type(normal_obj.level1.level2)         is type(fast_obj.level1.level2)
        assert type(normal_obj.level1.level2.level3)  is type(fast_obj.level1.level2.level3)

    def test__equivalence__json_output(self):                                     # JSON output identical
        normal_obj = TS__Simple(name='json', count=99)

        with Type_Safe__Config(fast_create=True):
            fast_obj = TS__Simple(name='json', count=99)

        assert normal_obj.json() == fast_obj.json()

    def test__equivalence__json_nested(self):                                     # Nested JSON identical
        normal_obj = TS__With_Nested(name='parent')
        normal_obj.inner.value = 'inner_val'

        with Type_Safe__Config(fast_create=True):
            fast_obj = TS__With_Nested(name='parent')
            fast_obj.inner.value = 'inner_val'

        assert normal_obj.json() == fast_obj.json()

    # ───────────────────────────────────────────────────────────────────────────
    # Batch Operations
    # ───────────────────────────────────────────────────────────────────────────

    def test__batch__create_simple(self):                                         # Create many objects
        with Type_Safe__Config(fast_create=True):
            objects = [TS__Simple(name=f'obj_{i}', count=i) for i in range(100)]

        assert len(objects) == 100
        assert objects[0].name   == 'obj_0'
        assert objects[0].count  == 0
        assert objects[99].name  == 'obj_99'
        assert objects[99].count == 99

    def test__batch__nested_all_independent(self):                                # All nested objects independent
        with Type_Safe__Config(fast_create=True):
            objects = [TS__With_Nested() for _ in range(10)]

        objects[0].inner.value = 'modified'

        for obj in objects[1:]:
            assert obj.inner.value == ''

    def test__batch__collections_all_independent(self):                           # All collections independent
        with Type_Safe__Config(fast_create=True):
            objects = [TS__With_Collections() for _ in range(10)]

        objects[0].items.append('item')
        objects[0].data['key'] = 42

        for obj in objects[1:]:
            assert len(obj.items) == 0
            assert len(obj.data)  == 0

# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes - Simple
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Empty(Type_Safe):                                                       # Edge case: no fields
    pass


class TS__Simple(Type_Safe):                                                      # Basic static fields
    name   : str   = ''
    count  : int   = 0
    active : bool  = False
    value  : float = 0.0


class TS__With_Defaults(Type_Safe):                                               # Non-empty defaults
    name    : str  = 'default_name'
    count   : int  = 42
    enabled : bool = True


class TS__With_Optional(Type_Safe):                                               # Optional field with None
    required : str           = ''
    optional : Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes - Collections
# ═══════════════════════════════════════════════════════════════════════════════

class TS__With_List(Type_Safe):
    name  : str = ''
    items : List[str]


class TS__With_Dict(Type_Safe):
    name : str = ''
    data : Dict[str, int]


class TS__With_Collections(Type_Safe):                                            # Multiple collections
    name  : str = ''
    items : List[str]
    data  : Dict[str, int]


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes - Nested
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Inner(Type_Safe):                                                       # Simple inner class
    value : str = ''
    count : int = 0


class TS__With_Nested(Type_Safe):                                                 # Single nested
    inner : TS__Inner
    name  : str = ''


class TS__With_Multiple_Nested(Type_Safe):                                        # Multiple nested
    child1 : TS__Inner
    child2 : TS__Inner
    child3 : TS__Inner
    name   : str = ''


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes - Deep Nesting
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Deep_Level3(Type_Safe):
    data : str = ''


class TS__Deep_Level2(Type_Safe):
    level3 : TS__Deep_Level3
    value  : int = 0


class TS__Deep_Level1(Type_Safe):
    level2 : TS__Deep_Level2
    name   : str = ''


class TS__Deep(Type_Safe):                                                        # 3 levels of nesting
    level1 : TS__Deep_Level1
    count  : int = 0


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes - Mixed (All Field Types)
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Mixed(Type_Safe):                                                       # Static + Factory + Nested
    name   : str = ''
    items  : List[str]
    data   : Dict[str, int]
    inner  : TS__Inner


class TS__Complex(Type_Safe):                                                     # Simulates real-world usage
    node_id : str = ''
    value   : int = 0
    tags    : List[str]
    meta    : Dict[str, str]
    child   : TS__Inner


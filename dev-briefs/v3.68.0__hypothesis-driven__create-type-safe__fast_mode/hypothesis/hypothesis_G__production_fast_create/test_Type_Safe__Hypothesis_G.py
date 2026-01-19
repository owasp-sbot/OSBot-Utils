# ═══════════════════════════════════════════════════════════════════════════════
# Tests: Type_Safe__Hypothesis_G - Functional Tests for Fast Object Creation
# Verify fast_create produces correct, fully functional objects
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                  import Dict, List
from unittest                                import TestCase
from Type_Safe__Config                       import Type_Safe__Config
from Type_Safe__Hypothesis_G                 import Type_Safe__Hypothesis_G
from Type_Safe__Fast_Create__Cache           import type_safe_fast_create_cache


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
# Normal Mode Tests (fast_create=False)
# ═══════════════════════════════════════════════════════════════════════════════

class test_normal_mode(TestCase):

    def setUp(self):
        type_safe_fast_create_cache.clear_cache()

    def test__creates_object_with_defaults(self):
        obj = TS__Simple()

        assert type(obj) is TS__Simple
        assert obj.name   == ''
        assert obj.count  == 0
        assert obj.active == False

    def test__creates_object_with_kwargs(self):
        obj = TS__Simple(name='test', count=42)

        assert obj.name   == 'test'
        assert obj.count  == 42
        assert obj.active == False

    def test__creates_nested_objects(self):
        obj = TS__With_Nested()

        assert obj.inner        is not None
        assert type(obj.inner)  is TS__Inner
        assert obj.inner.value  == ''
        assert obj.inner.count  == 0


# ═══════════════════════════════════════════════════════════════════════════════
# Fast Create Mode Tests (fast_create=True)
# ═══════════════════════════════════════════════════════════════════════════════

class test_fast_create_mode(TestCase):

    def setUp(self):
        type_safe_fast_create_cache.clear_cache()

    def test__creates_object_with_defaults(self):
        with Type_Safe__Config(fast_create=True):
            obj = TS__Simple()

        assert type(obj) is TS__Simple
        assert obj.name   == ''
        assert obj.count  == 0
        assert obj.active == False

    def test__creates_object_with_kwargs(self):
        with Type_Safe__Config(fast_create=True):
            obj = TS__Simple(name='fast', count=99)

        assert obj.name   == 'fast'
        assert obj.count  == 99
        assert obj.active == False

    def test__collections_not_shared(self):
        with Type_Safe__Config(fast_create=True):
            obj1 = TS__With_Collections()
            obj2 = TS__With_Collections()

        obj1.items.append('item1')

        assert len(obj1.items) == 1
        assert len(obj2.items) == 0                                               # Not shared!

    def test__nested_objects_created(self):
        with Type_Safe__Config(fast_create=True):
            obj = TS__With_Nested()

        assert obj.inner        is not None
        assert type(obj.inner)  is TS__Inner
        assert obj.inner.value  == ''
        assert obj.inner.count  == 0

    def test__nested_objects_not_shared(self):
        with Type_Safe__Config(fast_create=True):
            obj1 = TS__With_Nested()
            obj2 = TS__With_Nested()

        obj1.inner.value = 'modified'

        assert obj1.inner.value == 'modified'
        assert obj2.inner.value == ''                                             # Not shared!

    def test__deep_nested_created(self):
        with Type_Safe__Config(fast_create=True):
            obj = TS__Deep()

        assert obj.level1              is not None
        assert obj.level1.level2       is not None
        assert obj.level1.level2.data  == ''

    def test__json_works(self):
        with Type_Safe__Config(fast_create=True):
            obj = TS__Simple(name='json_test', count=42)

        json_data = obj.json()

        assert json_data['name']   == 'json_test'
        assert json_data['count']  == 42
        assert json_data['active'] == False

    def test__isinstance_works(self):
        with Type_Safe__Config(fast_create=True):
            obj = TS__Simple()

        assert isinstance(obj, TS__Simple)
        assert isinstance(obj, Type_Safe__Hypothesis_G)


# ═══════════════════════════════════════════════════════════════════════════════
# Skip Validation Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_skip_validation(TestCase):

    def setUp(self):
        type_safe_fast_create_cache.clear_cache()

    def test__setattr_works_with_skip_validation(self):
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj      = TS__Simple()
            obj.name = 'updated'

        assert obj.name == 'updated'

    def test__setattr_validates_without_skip_validation(self):
        with Type_Safe__Config(fast_create=True, skip_validation=False):
            obj      = TS__Simple()
            obj.name = 'validated'                                                # Should still work

        assert obj.name == 'validated'


# ═══════════════════════════════════════════════════════════════════════════════
# Config Context Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_config_context(TestCase):

    def setUp(self):
        type_safe_fast_create_cache.clear_cache()

    def test__config_only_active_in_context(self):
        # Outside context - normal mode
        obj1 = TS__Simple()

        with Type_Safe__Config(fast_create=True):
            # Inside context - fast mode
            obj2 = TS__Simple()

        # Outside context again - normal mode
        obj3 = TS__Simple()

        assert type(obj1) is TS__Simple
        assert type(obj2) is TS__Simple
        assert type(obj3) is TS__Simple

    def test__nested_contexts(self):
        with Type_Safe__Config(fast_create=True):
            obj1 = TS__Simple()

            with Type_Safe__Config(fast_create=True, skip_validation=True):
                obj2      = TS__Simple()
                obj2.name = 'nested'

            obj3 = TS__Simple()

        assert type(obj1) is TS__Simple
        assert type(obj2) is TS__Simple
        assert type(obj3) is TS__Simple
        assert obj2.name  == 'nested'
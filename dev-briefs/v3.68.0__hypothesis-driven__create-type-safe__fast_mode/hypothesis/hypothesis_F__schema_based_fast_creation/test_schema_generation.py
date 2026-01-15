# ═══════════════════════════════════════════════════════════════════════════════
# Functional Tests: Type_Safe__Hypothesis_F - Schema-Based Fast Create
# Verify fast_create produces correct, fully functional objects
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                   import Dict, List
from unittest                                                                                 import TestCase
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                            import Type_Safe__Config

from Type_Safe__Fast_Create__Schema                                                           import (
    clear_schema_cache,
    get_or_create_schema,
    generate_schema,
    is_immutable,
    is_nested_type_safe,
    FIELD_MODE__STATIC,
    FIELD_MODE__FACTORY,
    FIELD_MODE__NESTED,
)
from Type_Safe__Hypothesis_F                                                                  import (
    Type_Safe__Hypothesis_F,
    fast_create,
    warm_schema_cache,
)


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Simple(Type_Safe__Hypothesis_F):
    name   : str  = ''
    count  : int  = 0
    active : bool = False

class TS__With_Collections(Type_Safe__Hypothesis_F):
    name   : str = ''
    items  : List[str]
    data   : Dict[str, int]

class TS__Inner(Type_Safe__Hypothesis_F):
    value : str = ''
    count : int = 0

class TS__With_Nested(Type_Safe__Hypothesis_F):
    inner : TS__Inner
    name  : str = ''

class TS__Deep_Level2(Type_Safe__Hypothesis_F):
    data : str = ''

class TS__Deep_Level1(Type_Safe__Hypothesis_F):
    level2 : TS__Deep_Level2
    name   : str = ''

class TS__Deep(Type_Safe__Hypothesis_F):
    level1 : TS__Deep_Level1
    count  : int = 0


# ═══════════════════════════════════════════════════════════════════════════════
# Schema Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_schema_generation(TestCase):

    def setUp(self):
        clear_schema_cache()

    def test__is_immutable(self):
        """Test immutability detection"""
        assert is_immutable('') == True
        assert is_immutable('hello') == True
        assert is_immutable(0) == True
        assert is_immutable(42) == True
        assert is_immutable(3.14) == True
        assert is_immutable(True) == True
        assert is_immutable(False) == True
        assert is_immutable(None) == True

        assert is_immutable([]) == False
        assert is_immutable({}) == False
        assert is_immutable(set()) == False

    def test__generate_schema__simple(self):
        """Test schema generation for simple class"""
        schema = generate_schema(TS__Simple)

        assert schema.target_class is TS__Simple
        assert len(schema.fields) == 3

        # All should be static
        for field in schema.fields:
            assert field.mode == FIELD_MODE__STATIC, f"{field.name} should be static"

        assert schema.static_dict['name'] == ''
        assert schema.static_dict['count'] == 0
        assert schema.static_dict['active'] == False

    def test__generate_schema__with_collections(self):
        """Test schema for class with collections"""
        schema = generate_schema(TS__With_Collections)

        # name is static
        assert 'name' in schema.static_dict

        # items and data are factory
        assert len(schema.factory_fields) == 2
        factory_names = {f.name for f in schema.factory_fields}
        assert factory_names == {'items', 'data'}

    def test__generate_schema__with_nested(self):
        """Test schema for class with nested Type_Safe"""
        schema = generate_schema(TS__With_Nested)

        assert len(schema.nested_fields) == 1
        nested_field = schema.nested_fields[0]
        assert nested_field.name == 'inner'
        assert nested_field.mode == FIELD_MODE__NESTED
        assert nested_field.nested_class is TS__Inner


# ═══════════════════════════════════════════════════════════════════════════════
# Fast Create Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_fast_create(TestCase):

    def setUp(self):
        clear_schema_cache()

    def test__fast_create__simple(self):
        """Test fast_create with simple class"""
        obj = fast_create(TS__Simple)

        assert type(obj) is TS__Simple
        assert obj.name == ''
        assert obj.count == 0
        assert obj.active == False

    def test__fast_create__with_kwargs(self):
        """Test fast_create with kwargs"""
        obj = fast_create(TS__Simple, name='test', count=42)

        assert obj.name == 'test'
        assert obj.count == 42
        assert obj.active == False  # Default

    def test__fast_create__collections_not_shared(self):
        """Test that collections are fresh instances"""
        obj1 = fast_create(TS__With_Collections)
        obj2 = fast_create(TS__With_Collections)

        obj1.items.append('item1')

        assert len(obj1.items) == 1
        assert len(obj2.items) == 0, "Collections should not be shared"

    def test__fast_create__nested(self):
        """Test fast_create with nested Type_Safe"""
        obj = fast_create(TS__With_Nested)

        assert obj.inner is not None
        assert type(obj.inner) is TS__Inner
        assert obj.inner.value == ''
        assert obj.inner.count == 0

    def test__fast_create__deep_nested(self):
        """Test fast_create with deep nesting"""
        obj = fast_create(TS__Deep)

        assert obj.level1 is not None
        assert obj.level1.level2 is not None
        assert obj.level1.level2.data == ''

    def test__fast_create__nested_not_shared(self):
        """Test that nested objects are not shared"""
        obj1 = fast_create(TS__With_Nested)
        obj2 = fast_create(TS__With_Nested)

        obj1.inner.value = 'modified'

        assert obj1.inner.value == 'modified'
        assert obj2.inner.value == '', "Nested objects should not be shared"

    def test__fast_create__json_works(self):
        """Test that json() works on fast_created objects"""
        obj = fast_create(TS__Simple, name='json_test', count=99)

        json_data = obj.json()

        assert json_data['name'] == 'json_test'
        assert json_data['count'] == 99
        assert json_data['active'] == False

    def test__fast_create__isinstance_works(self):
        """Test isinstance checks on fast_created objects"""
        obj = fast_create(TS__Simple)

        assert isinstance(obj, TS__Simple)
        assert isinstance(obj, Type_Safe__Hypothesis_F)


# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Hypothesis_F Class Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_Type_Safe__Hypothesis_F(TestCase):

    def setUp(self):
        clear_schema_cache()

    def test__normal_mode(self):
        """Test normal creation (fast_create=False)"""
        with Type_Safe__Config(fast_create=False):
            obj = TS__Simple(name='normal', count=1)

            assert obj.name == 'normal'
            assert obj.count == 1

    def test__fast_create_mode(self):
        """Test fast_create mode via config"""
        with Type_Safe__Config(fast_create=True):
            obj = TS__Simple(name='fast', count=2)

            assert obj.name == 'fast'
            assert obj.count == 2

    def test__setattr_validation_after_fast_create(self):
        """Test that __setattr__ validation works after fast_create"""
        with Type_Safe__Config(fast_create=True):
            obj = TS__Simple()

            # Valid assignment should work
            obj.name = 'valid'
            assert obj.name == 'valid'

            obj.count = 100
            assert obj.count == 100


# ═══════════════════════════════════════════════════════════════════════════════
# Schema Cache Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_schema_cache(TestCase):

    def setUp(self):
        clear_schema_cache()

    def test__schema_is_cached(self):
        """Test that schema is cached and reused"""
        schema1 = get_or_create_schema(TS__Simple)
        schema2 = get_or_create_schema(TS__Simple)

        assert schema1 is schema2, "Schema should be cached"

    def test__warm_schema_cache(self):
        """Test pre-warming the schema cache"""
        clear_schema_cache()

        warm_schema_cache(TS__Deep)

        # All nested classes should be cached
        from Type_Safe__Fast_Create__Schema import _schema_cache

        assert TS__Deep in _schema_cache
        assert TS__Deep_Level1 in _schema_cache
        assert TS__Deep_Level2 in _schema_cache

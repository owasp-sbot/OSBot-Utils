# ═══════════════════════════════════════════════════════════════════════════════
# Tests: Type_Safe__Fast_Create__Cache - Schema Generation and Caching
# Verify schema generation, field classification, and cache behavior
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                         import Dict, List, Optional
from unittest                                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                                     import Type_Safe__Primitive
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                               import Type_Safe__List
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                               import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set                                import Type_Safe__Set
from osbot_utils.type_safe.type_safe_core.fast_create.Type_Safe__Fast_Create__Cache                 import type_safe_fast_create_cache, Type_Safe__Fast_Create__Cache, IMMUTABLE_TYPES
from osbot_utils.type_safe.type_safe_core.fast_create.schemas.Schema__Type_Safe__Fast_Create__Field import FIELD_MODE__STATIC, FIELD_MODE__FACTORY, FIELD_MODE__NESTED
from osbot_utils.type_safe.type_safe_core.fast_create.schemas.Schema__Type_Safe__Fast_Create__Class import Schema__Type_Safe__Fast_Create__Class


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Empty(Type_Safe):                                                       # Empty class - edge case
    pass


class TS__Simple(Type_Safe):
    name   : str  = ''
    count  : int  = 0
    active : bool = False


class TS__With_Collections(Type_Safe):
    name  : str = ''
    items : List[str]
    data  : Dict[str, int]


class TS__With_Set(Type_Safe):                                                    # Test Set collection
    tags : set


class TS__Inner(Type_Safe):
    value : str = ''
    count : int = 0


class TS__With_Nested(Type_Safe):
    inner : TS__Inner
    name  : str = ''


class TS__Deep_Level2(Type_Safe):
    data : str = ''


class TS__Deep_Level1(Type_Safe):
    level2 : TS__Deep_Level2
    name   : str = ''


class TS__Deep(Type_Safe):
    level1 : TS__Deep_Level1
    count  : int = 0


class TS__With_Optional(Type_Safe):                                               # Test Optional fields
    required : str = ''
    optional : Optional[str] = None


class TS__With_Private(Type_Safe):                                                # Test private attribute filtering
    public_field  : str = ''
    _private_field: str = 'should_be_skipped'


class TS__All_Immutable_Types(Type_Safe):                                         # Test all immutable types
    str_field       : str        = ''
    int_field       : int        = 0
    float_field     : float      = 0.0
    bool_field      : bool       = False
    none_field      : str        = None
    bytes_field     : bytes      = b''
    tuple_field     : tuple      = ()
    frozenset_field : frozenset  = frozenset()


class TS__Custom_Primitive(Type_Safe__Primitive, str):                            # Custom primitive for testing
    pass


class TS__With_Primitive(Type_Safe):                                              # Test Type_Safe__Primitive handling
    custom : TS__Custom_Primitive


# ═══════════════════════════════════════════════════════════════════════════════
# Main Test Class
# ═══════════════════════════════════════════════════════════════════════════════

class test_Type_Safe__Fast_Create__Cache(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.cache = Type_Safe__Fast_Create__Cache()

    def setUp(self):
        self.cache.clear_cache()                                                  # Fresh cache for each test

    # ═══════════════════════════════════════════════════════════════════════════
    # Module Singleton Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__module_singleton(self):                                             # Verify singleton is available
        assert type(type_safe_fast_create_cache) is Type_Safe__Fast_Create__Cache
        assert type_safe_fast_create_cache       is not self.cache                # Different instance from test

    def test__init__(self):                                                       # Test initialization state
        with Type_Safe__Fast_Create__Cache() as _:
            assert type(_.schema_cache) is dict
            assert type(_.generating)   is set
            assert len(_.schema_cache)  == 0
            assert len(_.generating)    == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # is_immutable Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__is_immutable__with_immutable_types(self):                           # Test all IMMUTABLE_TYPES
        assert self.cache.is_immutable(None)          is True                     # NoneType
        assert self.cache.is_immutable('')            is True                     # str
        assert self.cache.is_immutable('hello')       is True
        assert self.cache.is_immutable(0)             is True                     # int
        assert self.cache.is_immutable(42)            is True
        assert self.cache.is_immutable(-1)            is True
        assert self.cache.is_immutable(3.14)          is True                     # float
        assert self.cache.is_immutable(0.0)           is True
        assert self.cache.is_immutable(True)          is True                     # bool
        assert self.cache.is_immutable(False)         is True
        assert self.cache.is_immutable(b'')           is True                     # bytes
        assert self.cache.is_immutable(b'bytes')      is True
        assert self.cache.is_immutable(())            is True                     # tuple
        assert self.cache.is_immutable((1, 2, 3))     is True
        assert self.cache.is_immutable(frozenset())   is True                     # frozenset
        assert self.cache.is_immutable(frozenset({1})) is True

    def test__is_immutable__with_mutable_types(self):                             # Test mutable types return False
        assert self.cache.is_immutable([])            is False                    # list
        assert self.cache.is_immutable([1, 2, 3])     is False
        assert self.cache.is_immutable({})            is False                    # dict
        assert self.cache.is_immutable({'a': 1})      is False
        assert self.cache.is_immutable(set())         is False                    # set
        assert self.cache.is_immutable({1, 2, 3})     is False

    def test__is_immutable__with_type_safe_objects(self):                         # Type_Safe objects are mutable
        assert self.cache.is_immutable(TS__Simple())  is False
        assert self.cache.is_immutable(TS__Inner())   is False

    # ═══════════════════════════════════════════════════════════════════════════
    # is_type_safe_collection Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__is_type_safe_collection__with_type_safe_collections(self):
        assert self.cache.is_type_safe_collection(Type_Safe__List(expected_type     = str                            )) is True
        assert self.cache.is_type_safe_collection(Type_Safe__Dict(expected_key_type = str, expected_value_type = str )) is True
        assert self.cache.is_type_safe_collection(Type_Safe__Set(expected_type      = str                            )) is True

    def test__is_type_safe_collection__with_builtin_collections(self):
        assert self.cache.is_type_safe_collection([])    is True
        assert self.cache.is_type_safe_collection({})    is True
        assert self.cache.is_type_safe_collection(set()) is True

    def test__is_type_safe_collection__with_non_collections(self):
        assert self.cache.is_type_safe_collection('')           is False
        assert self.cache.is_type_safe_collection(42)           is False
        assert self.cache.is_type_safe_collection(None)         is False
        assert self.cache.is_type_safe_collection(TS__Simple()) is False

    # ═══════════════════════════════════════════════════════════════════════════
    # is_nested_type_safe Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__is_nested_type_safe__with_type_safe_objects(self):                  # Regular Type_Safe is nested
        assert self.cache.is_nested_type_safe(TS__Simple()) is True
        assert self.cache.is_nested_type_safe(TS__Inner())  is True

    def test__is_nested_type_safe__with_primitives(self):                         # Primitives are NOT nested
        primitive = TS__Custom_Primitive('test')
        assert self.cache.is_nested_type_safe(primitive) is False

    def test__is_nested_type_safe__with_collections(self):                        # Collections are NOT nested
        assert self.cache.is_nested_type_safe(Type_Safe__List(expected_type     = str                            )) is False
        assert self.cache.is_nested_type_safe(Type_Safe__Dict(expected_key_type = str, expected_value_type = str )) is False
        assert self.cache.is_nested_type_safe(Type_Safe__Set(expected_type      = str                            ))  is False

    def test__is_nested_type_safe__with_non_type_safe(self):                      # Non-Type_Safe is NOT nested
        assert self.cache.is_nested_type_safe('')       is False
        assert self.cache.is_nested_type_safe(42)       is False
        assert self.cache.is_nested_type_safe([])       is False
        assert self.cache.is_nested_type_safe(None)     is False
        assert self.cache.is_nested_type_safe(object()) is False

    # ═══════════════════════════════════════════════════════════════════════════
    # classify_field Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__classify_field__static(self):                                       # Immutable values -> static
        field = self.cache.classify_field('name', '')
        assert field.name         == 'name'
        assert field.mode         == FIELD_MODE__STATIC
        assert field.static_value == ''

        field = self.cache.classify_field('count', 42)
        assert field.mode         == FIELD_MODE__STATIC
        assert field.static_value == 42

    def test__classify_field__factory(self):                                      # Mutable collections -> factory
        field = self.cache.classify_field('items', [])
        assert field.name         == 'items'
        assert field.mode         == FIELD_MODE__FACTORY
        assert field.factory_func is not None
        assert field.factory_func() == []                                         # Creates fresh list

        field = self.cache.classify_field('data', {})
        assert field.mode         == FIELD_MODE__FACTORY
        assert field.factory_func() == {}                                         # Creates fresh dict

    def test__classify_field__nested(self):                                       # Type_Safe objects -> nested
        inner = TS__Inner()
        field = self.cache.classify_field('inner', inner)
        assert field.name         == 'inner'
        assert field.mode         == FIELD_MODE__NESTED
        assert field.nested_class is TS__Inner

    # ═══════════════════════════════════════════════════════════════════════════
    # get_factory_func Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_factory_func__type_safe_list(self):                             # Preserves expected_type
        ts_list = Type_Safe__List(expected_type=str)
        factory = self.cache.get_factory_func(ts_list)
        result  = factory()

        assert type(result)        is Type_Safe__List
        assert result.expected_type is str

    def test__get_factory_func__type_safe_dict(self):                             # Preserves key/value types
        ts_dict = Type_Safe__Dict(expected_key_type=str, expected_value_type=int)
        factory = self.cache.get_factory_func(ts_dict)
        result  = factory()

        assert type(result)              is Type_Safe__Dict
        assert result.expected_key_type   is str
        assert result.expected_value_type is int

    def test__get_factory_func__type_safe_set(self):                              # Preserves expected_type
        ts_set  = Type_Safe__Set(expected_type=str)
        factory = self.cache.get_factory_func(ts_set)
        result  = factory()

        assert type(result)        is Type_Safe__Set
        assert result.expected_type is str

    def test__get_factory_func__builtin_collections(self):                        # Returns type constructor
        assert self.cache.get_factory_func([])    is list
        assert self.cache.get_factory_func({})    is dict
        assert self.cache.get_factory_func(set()) is set

    def test__get_factory_func__creates_independent_instances(self):              # Each call returns new instance
        factory   = self.cache.get_factory_func([])
        instance1 = factory()
        instance2 = factory()

        instance1.append('item')
        assert len(instance1) == 1
        assert len(instance2) == 0                                                # Independent!

    # ═══════════════════════════════════════════════════════════════════════════
    # generate_schema Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__generate_schema__empty_class(self):                                 # Edge case: no fields
        schema = self.cache.generate_schema(TS__Empty)

        assert schema.target_class   is TS__Empty
        assert len(schema.fields)    == 0
        assert len(schema.static_dict)    == 0
        assert len(schema.factory_fields) == 0
        assert len(schema.nested_fields)  == 0

    def test__generate_schema__simple_class(self):                                # All static fields
        schema = self.cache.generate_schema(TS__Simple)

        assert schema.target_class is TS__Simple
        assert len(schema.fields)  == 3

        for field in schema.fields:
            assert field.mode == FIELD_MODE__STATIC

        assert schema.static_dict['name']   == ''
        assert schema.static_dict['count']  == 0
        assert schema.static_dict['active'] is False

    def test__generate_schema__with_collections(self):                            # Factory fields for collections
        schema = self.cache.generate_schema(TS__With_Collections)

        assert 'name' in schema.static_dict
        assert len(schema.factory_fields) == 2

        factory_names = {f.name for f in schema.factory_fields}
        assert factory_names == {'items', 'data'}

    def test__generate_schema__with_nested(self):                                 # Nested Type_Safe fields
        schema = self.cache.generate_schema(TS__With_Nested)

        assert len(schema.nested_fields)          == 1
        assert schema.nested_fields[0].name       == 'inner'
        assert schema.nested_fields[0].mode       == FIELD_MODE__NESTED
        assert schema.nested_fields[0].nested_class is TS__Inner

    def test__generate_schema__deep_nested(self):                                 # Multi-level nesting
        schema = self.cache.generate_schema(TS__Deep)

        assert len(schema.nested_fields)    == 1
        assert schema.nested_fields[0].name == 'level1'
        assert schema.nested_fields[0].nested_class is TS__Deep_Level1

    def test__generate_schema__skips_private_fields(self):                        # Private attrs filtered out
        schema = self.cache.generate_schema(TS__With_Private)

        field_names = {f.name for f in schema.fields}
        assert 'public_field'   in field_names
        assert '_private_field' not in field_names                                # Skipped!

    def test__generate_schema__with_optional(self):                               # Optional fields with None default
        schema = self.cache.generate_schema(TS__With_Optional)

        assert schema.static_dict['required'] == ''
        assert schema.static_dict['optional'] is None                             # None is static (immutable)

    def test__generate_schema__returns_correct_type(self):                        # Type check on return
        schema = self.cache.generate_schema(TS__Simple)
        assert type(schema) is Schema__Type_Safe__Fast_Create__Class

    # ═══════════════════════════════════════════════════════════════════════════
    # is_generating / Recursion Guard Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__is_generating__before_generation(self):                             # Not generating initially
        assert self.cache.is_generating(TS__Simple) is False

    def test__is_generating__during_generation(self):                             # Manual test of guard
        self.cache.generating.add(TS__Simple)
        assert self.cache.is_generating(TS__Simple) is True

        self.cache.generating.discard(TS__Simple)
        assert self.cache.is_generating(TS__Simple) is False

    def test__is_generating__cleared_after_generation(self):                      # Guard removed after schema gen
        self.cache.generate_schema(TS__Simple)
        assert self.cache.is_generating(TS__Simple) is False                      # Cleaned up

    # ═══════════════════════════════════════════════════════════════════════════
    # get_schema / Cache Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_schema__creates_on_first_access(self):                          # Lazy creation
        assert TS__Simple not in self.cache.schema_cache

        schema = self.cache.get_schema(TS__Simple)

        assert TS__Simple in self.cache.schema_cache
        assert schema is self.cache.schema_cache[TS__Simple]

    def test__get_schema__returns_cached_instance(self):                          # Same object returned
        schema1 = self.cache.get_schema(TS__Simple)
        schema2 = self.cache.get_schema(TS__Simple)

        assert schema1 is schema2                                                 # Same instance!

    def test__get_schema__different_classes_different_schemas(self):              # Separate schemas per class
        schema1 = self.cache.get_schema(TS__Simple)
        schema2 = self.cache.get_schema(TS__Inner)

        assert schema1 is not schema2
        assert schema1.target_class is TS__Simple
        assert schema2.target_class is TS__Inner

    # ═══════════════════════════════════════════════════════════════════════════
    # warm_cache Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__warm_cache__single_class(self):                                     # Warms target class
        assert TS__Simple not in self.cache.schema_cache

        self.cache.warm_cache(TS__Simple)

        assert TS__Simple in self.cache.schema_cache

    def test__warm_cache__recursive_nested(self):                                 # Warms all nested classes
        self.cache.warm_cache(TS__Deep)

        assert TS__Deep        in self.cache.schema_cache
        assert TS__Deep_Level1 in self.cache.schema_cache
        assert TS__Deep_Level2 in self.cache.schema_cache

    def test__warm_cache__idempotent(self):                                       # Multiple calls are safe
        self.cache.warm_cache(TS__Simple)
        schema1 = self.cache.schema_cache[TS__Simple]

        self.cache.warm_cache(TS__Simple)
        schema2 = self.cache.schema_cache[TS__Simple]

        assert schema1 is schema2                                                 # Same instance

    # ═══════════════════════════════════════════════════════════════════════════
    # clear_cache Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__clear_cache__empties_schema_cache(self):
        self.cache.get_schema(TS__Simple)
        self.cache.get_schema(TS__Inner)
        assert len(self.cache.schema_cache) >= 2

        self.cache.clear_cache()

        assert len(self.cache.schema_cache) == 0

    def test__clear_cache__empties_generating_set(self):
        self.cache.generating.add(TS__Simple)                                     # Simulate stuck state
        assert len(self.cache.generating) == 1

        self.cache.clear_cache()

        assert len(self.cache.generating) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Static Dict Sharing Tests (Immutability Verification)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__static_dict__values_are_shared_references(self):                    # Verify immutable sharing works
        schema = self.cache.get_schema(TS__Simple)

        dict1 = schema.static_dict.copy()
        dict2 = schema.static_dict.copy()

        # String/int/bool are immutable - sharing is safe
        assert dict1['name']   is dict2['name']                                   # Same string object
        assert dict1['count']  is dict2['count']                                  # Same int object (for small ints)
        assert dict1['active'] is dict2['active']                                 # Same bool object

    # ═══════════════════════════════════════════════════════════════════════════
    # IMMUTABLE_TYPES Constant Test
    # ═══════════════════════════════════════════════════════════════════════════

    def test__IMMUTABLE_TYPES__contains_expected_types(self):                     # Verify constant is correct
        expected = (str, int, float, bool, type(None), bytes, tuple, frozenset)
        assert IMMUTABLE_TYPES == expected
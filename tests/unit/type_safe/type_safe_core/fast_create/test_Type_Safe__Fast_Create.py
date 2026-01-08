# ═══════════════════════════════════════════════════════════════════════════════
# Tests: Type_Safe__Fast_Create - Fast Object Creation Using Pre-Computed Schema
# Verify object creation, field population, and recursive nested creation
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                         import Dict, List
from unittest                                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.type_safe_core.fast_create.Type_Safe__Fast_Create                        import type_safe_fast_create, Type_Safe__Fast_Create
from osbot_utils.type_safe.type_safe_core.fast_create.Type_Safe__Fast_Create__Cache                 import type_safe_fast_create_cache


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Empty(Type_Safe):                                                       # Edge case: no fields
    pass


class TS__Static_Only(Type_Safe):                                                 # Only immutable fields
    name   : str   = ''
    count  : int   = 0
    active : bool  = False
    value  : float = 0.0


class TS__Factory_Only(Type_Safe):                                                # Only collection fields
    items : List[str]
    data  : Dict[str, int]
    tags  : set


class TS__Inner(Type_Safe):                                                       # Simple nested class
    value : str = ''
    count : int = 0


class TS__Nested_Only(Type_Safe):                                                 # Only nested Type_Safe fields
    inner1 : TS__Inner
    inner2 : TS__Inner


class TS__Mixed(Type_Safe):                                                       # All field types combined
    name   : str = ''
    items  : List[str]
    inner  : TS__Inner


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


class TS__With_Defaults(Type_Safe):                                               # Non-empty defaults
    name    : str  = 'default_name'
    count   : int  = 42
    enabled : bool = True


# ═══════════════════════════════════════════════════════════════════════════════
# Main Test Class
# ═══════════════════════════════════════════════════════════════════════════════

class test_Type_Safe__Fast_Create(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.fast_create = Type_Safe__Fast_Create()

    def setUp(self):
        type_safe_fast_create_cache.clear_cache()                                 # Fresh cache for each test

    # ═══════════════════════════════════════════════════════════════════════════
    # Module Singleton Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__module_singleton(self):                                             # Verify singleton is available
        assert type(type_safe_fast_create) is Type_Safe__Fast_Create
        assert type_safe_fast_create       is not self.fast_create                # Different from test instance

    # ═══════════════════════════════════════════════════════════════════════════
    # create() - Basic Functionality
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create__empty_class(self):                                          # Edge case: no fields
        target = object.__new__(TS__Empty)
        self.fast_create.create(target)

        assert type(target)   is TS__Empty
        assert target.__dict__ == {}                                              # No fields to populate

    def test__create__static_only(self):                                          # All static fields populated
        target = object.__new__(TS__Static_Only)
        self.fast_create.create(target)

        assert type(target)  is TS__Static_Only
        assert target.name   == ''
        assert target.count  == 0
        assert target.active is False
        assert target.value  == 0.0

    def test__create__factory_only(self):                                         # All factory fields populated
        target = object.__new__(TS__Factory_Only)
        self.fast_create.create(target)

        assert type(target)       is TS__Factory_Only
        assert type(target.items) is list or hasattr(target.items, 'expected_type')  # List or Type_Safe__List
        assert type(target.data)  is dict or hasattr(target.data, 'expected_key_type')
        assert type(target.tags)  is set or hasattr(target.tags, 'expected_type')

    def test__create__nested_only(self):                                          # All nested fields populated
        target = object.__new__(TS__Nested_Only)
        self.fast_create.create(target)

        assert type(target)        is TS__Nested_Only
        assert type(target.inner1) is TS__Inner
        assert type(target.inner2) is TS__Inner
        assert target.inner1.value == ''
        assert target.inner2.count == 0

    def test__create__mixed_fields(self):                                         # All field types combined
        target = object.__new__(TS__Mixed)
        self.fast_create.create(target)

        assert type(target)       is TS__Mixed
        assert target.name        == ''                                           # Static
        assert len(target.items)  == 0                                            # Factory (empty list)
        assert type(target.inner) is TS__Inner                                    # Nested
        assert target.inner.value == ''

    def test__create__with_non_empty_defaults(self):                              # Non-empty default values
        target = object.__new__(TS__With_Defaults)
        self.fast_create.create(target)

        assert target.name    == 'default_name'
        assert target.count   == 42
        assert target.enabled is True

    # ═══════════════════════════════════════════════════════════════════════════
    # create() - Deep Nesting
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create__deep_nested(self):                                          # 3 levels of nesting
        target = object.__new__(TS__Deep)
        self.fast_create.create(target)

        assert type(target)                      is TS__Deep
        assert type(target.level1)               is TS__Deep_Level1
        assert type(target.level1.level2)        is TS__Deep_Level2
        assert type(target.level1.level2.level3) is TS__Deep_Level3
        assert target.level1.level2.level3.data  == ''                            # Deep access works

    def test__create__deep_nested__all_fields_initialized(self):                  # All fields at all levels
        target = object.__new__(TS__Deep)
        self.fast_create.create(target)

        assert target.count               == 0                                    # Level 0
        assert target.level1.name         == ''                                   # Level 1
        assert target.level1.level2.value == 0                                    # Level 2
        assert target.level1.level2.level3.data == ''                             # Level 3

    # ═══════════════════════════════════════════════════════════════════════════
    # create() - kwargs Override
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create__kwargs_override_static(self):                               # kwargs override static defaults
        target = object.__new__(TS__Static_Only)
        self.fast_create.create(target, name='custom', count=99)

        assert target.name   == 'custom'                                          # Overridden
        assert target.count  == 99                                                # Overridden
        assert target.active is False                                             # Default
        assert target.value  == 0.0                                               # Default

    def test__create__kwargs_override_factory(self):                              # kwargs skip factory creation
        custom_items = ['a', 'b', 'c']
        target = object.__new__(TS__Factory_Only)
        self.fast_create.create(target, items=custom_items)

        assert target.items is custom_items                                       # Exact same object
        assert target.items == ['a', 'b', 'c']

    def test__create__kwargs_override_nested(self):                               # kwargs skip nested creation
        custom_inner = TS__Inner()
        custom_inner.value = 'custom_value'
        custom_inner.count = 999

        target = object.__new__(TS__Nested_Only)
        self.fast_create.create(target, inner1=custom_inner)

        assert target.inner1 is custom_inner                                      # Exact same object
        assert target.inner1.value == 'custom_value'
        assert type(target.inner2) is TS__Inner                                   # Default created
        assert target.inner2.value == ''                                          # Default value

    def test__create__kwargs_all_fields(self):                                    # Override all fields
        target = object.__new__(TS__Mixed)
        self.fast_create.create(target, name   = 'full_override',
                                        items  = [1, 2, 3]      ,
                                        inner  = TS__Inner()    )

        assert target.name  == 'full_override'
        assert target.items == [1, 2, 3]
        assert type(target.inner) is TS__Inner

    # ═══════════════════════════════════════════════════════════════════════════
    # create() - Instance Independence
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create__factory_fields_independent(self):                           # Each instance gets fresh collections
        target1 = object.__new__(TS__Factory_Only)
        target2 = object.__new__(TS__Factory_Only)
        self.fast_create.create(target1)
        self.fast_create.create(target2)

        target1.items.append('item1')

        assert len(target1.items) == 1
        assert len(target2.items) == 0                                            # Independent!
        assert target1.items is not target2.items

    def test__create__nested_fields_independent(self):                            # Each instance gets fresh nested objects
        target1 = object.__new__(TS__Nested_Only)
        target2 = object.__new__(TS__Nested_Only)
        self.fast_create.create(target1)
        self.fast_create.create(target2)

        target1.inner1.value = 'modified'

        assert target1.inner1.value == 'modified'
        assert target2.inner1.value == ''                                         # Independent!
        assert target1.inner1 is not target2.inner1

    def test__create__static_fields_can_share_references(self):                   # Immutable values shared (optimization)
        target1 = object.__new__(TS__Static_Only)
        target2 = object.__new__(TS__Static_Only)
        self.fast_create.create(target1)
        self.fast_create.create(target2)

        # Immutable values can safely share references
        assert target1.name   is target2.name                                     # Same '' string object
        assert target1.active is target2.active                                   # Same False object

    # ═══════════════════════════════════════════════════════════════════════════
    # create() - Object Usability After Creation
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create__object_is_instance_of_class(self):                          # isinstance() works
        target = object.__new__(TS__Static_Only)
        self.fast_create.create(target)

        assert isinstance(target, TS__Static_Only)
        assert isinstance(target, Type_Safe)

    def test__create__object_supports_attribute_access(self):                     # Can read/write attributes
        target = object.__new__(TS__Static_Only)
        self.fast_create.create(target)

        assert target.name == ''
        target.name = 'updated'                                                   # Write works
        assert target.name == 'updated'

    def test__create__object_supports_json(self):                                 # json() method works
        target = object.__new__(TS__Static_Only)
        self.fast_create.create(target, name='json_test', count=42)

        json_data = target.json()

        assert json_data['name']   == 'json_test'
        assert json_data['count']  == 42
        assert json_data['active'] is False
        assert json_data['value']  == 0.0

    def test__create__nested_object_supports_json(self):                          # Nested objects serialize
        target = object.__new__(TS__Mixed)
        self.fast_create.create(target, name='nested_json')

        json_data = target.json()

        assert json_data['name']         == 'nested_json'
        assert json_data['items']        == []
        assert type(json_data['inner'])  is dict
        assert json_data['inner']['value'] == ''
        assert json_data['inner']['count'] == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # create() - Direct __dict__ Assignment Verification
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create__sets_dict_directly(self):                                   # __dict__ is set, not individual attrs
        target = object.__new__(TS__Static_Only)

        assert not hasattr(target, '__dict__') or target.__dict__ == {}           # Empty before create

        self.fast_create.create(target)

        assert hasattr(target, '__dict__')
        assert 'name'   in target.__dict__
        assert 'count'  in target.__dict__
        assert 'active' in target.__dict__
        assert 'value'  in target.__dict__

    # ═══════════════════════════════════════════════════════════════════════════
    # create() - Batch Creation Performance Pattern
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create__batch_creation(self):                                       # Pattern for bulk operations
        targets = []
        for i in range(10):
            target = object.__new__(TS__Static_Only)
            self.fast_create.create(target, name=f'item_{i}', count=i)
            targets.append(target)

        assert len(targets) == 10
        assert targets[0].name  == 'item_0'
        assert targets[0].count == 0
        assert targets[9].name  == 'item_9'
        assert targets[9].count == 9

        # All are independent
        for i, target in enumerate(targets):
            assert target.name == f'item_{i}'

    def test__create__batch_nested_independent(self):                             # Batch nested objects independent
        targets = []
        for _ in range(5):
            target = object.__new__(TS__Mixed)
            self.fast_create.create(target)
            targets.append(target)

        # Modify first target's nested object
        targets[0].inner.value = 'modified'
        targets[0].items.append('item')

        # Others unchanged
        for target in targets[1:]:
            assert target.inner.value == ''
            assert len(target.items)  == 0
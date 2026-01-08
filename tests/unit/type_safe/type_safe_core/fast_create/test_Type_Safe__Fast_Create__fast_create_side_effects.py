# ═══════════════════════════════════════════════════════════════════════════════
# Tests: Type_Safe Fast Create - Fast Create Side Effects
# Documents the INTENTIONAL TRADE-OFFS when using fast_create=True
# ═══════════════════════════════════════════════════════════════════════════════
#
# PURPOSE: Document what happens when objects are created with fast_create=True.
#          These are NOT BUGS - they are documented consequences of choosing
#          to bypass validation for performance.
#
# KEY DIFFERENCE FROM skip_validation:
#   - fast_create:     Affects __init__ (kwargs bypass validation)
#   - skip_validation: Affects __setattr__ (post-creation assignments bypass validation)
#
# WHEN TO USE fast_create=True:
#   - Bulk loading from trusted sources (database, serialized data)
#   - Performance-critical object creation
#   - Data already validated elsewhere
#
# WHEN NOT TO USE fast_create=True:
#   - User input in constructor
#   - Untrusted external data
#   - When type safety during construction is critical
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

class TS__Person(Type_Safe):
    name : str = ''
    age  : int = 0


class TS__With_List(Type_Safe):
    name  : str = ''
    items : List[str]


class TS__With_Dict(Type_Safe):
    name : str = ''
    data : Dict[str, int]


class TS__Nested_Inner(Type_Safe):
    value : str = ''


class TS__With_Nested(Type_Safe):
    inner : TS__Nested_Inner
    name  : str = ''


class TS__With_Defaults(Type_Safe):
    name    : str  = 'default_name'
    count   : int  = 42
    enabled : bool = True


# ═══════════════════════════════════════════════════════════════════════════════
# Test: Fast Create Side Effects (Documented Trade-offs)
# ═══════════════════════════════════════════════════════════════════════════════

class test_Type_Safe__Fast_Create__fast_create_side_effects(TestCase):
    """
    These tests document the EXPECTED CONSEQUENCES of using fast_create=True.
    All tests PASS - they document behavior, not bugs.

    Key insight: fast_create affects CONSTRUCTOR (kwargs), not post-creation setattr.
    """

    def setUp(self):
        type_safe_fast_create_cache.clear_cache()

    # ───────────────────────────────────────────────────────────────────────────
    # Side Effect: kwargs Not Validated During Construction
    # ───────────────────────────────────────────────────────────────────────────

    def test__side_effect__kwargs_wrong_type_accepted(self):                      # Constructor accepts wrong types
        with Type_Safe__Config(fast_create=True):
            obj = TS__Person(name=12345, age='twenty')                            # Wrong types in kwargs!

        assert obj.name == 12345                                                  # int instead of str
        assert obj.age  == 'twenty'                                               # str instead of int

    def test__side_effect__kwargs_none_to_non_optional(self):                     # None accepted for required fields
        with Type_Safe__Config(fast_create=True):
            obj = TS__Person(name=None, age=None)

        assert obj.name is None
        assert obj.age  is None

    def test__side_effect__kwargs_complex_types_accepted(self):                   # Any object accepted
        with Type_Safe__Config(fast_create=True):
            obj = TS__Person(name={'complex': 'dict'}, age=[1, 2, 3])

        assert obj.name == {'complex': 'dict'}
        assert obj.age  == [1, 2, 3]

    # ───────────────────────────────────────────────────────────────────────────
    # Side Effect: kwargs Not Converted During Construction
    # ───────────────────────────────────────────────────────────────────────────

    def test__side_effect__kwargs_not_auto_converted(self):                       # No type coercion
        # In normal mode, some conversions might happen
        # In fast_create mode, values are used as-is

        with Type_Safe__Config(fast_create=True):
            obj = TS__Person(name=12345)                                          # int, not converted to '12345'

        assert obj.name == 12345                                                  # Still int!
        assert type(obj.name) is int                                              # Not converted to str

    # ───────────────────────────────────────────────────────────────────────────
    # Side Effect: Collections in kwargs Used As-Is
    # ───────────────────────────────────────────────────────────────────────────

    def test__side_effect__list_kwarg_wrong_element_types(self):                  # List elements not validated
        with Type_Safe__Config(fast_create=True):
            obj = TS__With_List(items=[1, 2, 3, {'key': 'val'}])                  # Not List[str]!

        assert obj.items == [1, 2, 3, {'key': 'val'}]

    def test__side_effect__list_kwarg_not_a_list(self):                           # Can pass non-list to list field
        with Type_Safe__Config(fast_create=True):
            obj = TS__With_List(items='not_a_list')

        assert obj.items == 'not_a_list'
        assert type(obj.items) is str

    def test__side_effect__dict_kwarg_wrong_types(self):                          # Dict types not validated
        with Type_Safe__Config(fast_create=True):
            obj = TS__With_Dict(data={123: 'wrong', 'key': [1, 2, 3]})            # Wrong key and value types

        assert obj.data == {123: 'wrong', 'key': [1, 2, 3]}

    # ───────────────────────────────────────────────────────────────────────────
    # Side Effect: Nested Object kwargs Not Validated
    # ───────────────────────────────────────────────────────────────────────────

    def test__side_effect__nested_kwarg_can_be_dict(self):                        # Dict instead of Type_Safe object
        with Type_Safe__Config(fast_create=True):
            obj = TS__With_Nested(inner={'value': 'from_dict'})                   # Dict, not TS__Nested_Inner

        assert obj.inner == {'value': 'from_dict'}
        assert type(obj.inner) is dict                                            # Not TS__Nested_Inner!

    def test__side_effect__nested_kwarg_can_be_string(self):                      # String instead of Type_Safe object
        with Type_Safe__Config(fast_create=True):
            obj = TS__With_Nested(inner='just_a_string')

        assert obj.inner == 'just_a_string'
        assert type(obj.inner) is str

    def test__side_effect__nested_kwarg_can_be_none(self):                        # None instead of Type_Safe object
        with Type_Safe__Config(fast_create=True):
            obj = TS__With_Nested(inner=None)

        assert obj.inner is None

    # ───────────────────────────────────────────────────────────────────────────
    # Side Effect: Defaults Still Work When No kwarg Provided
    # ───────────────────────────────────────────────────────────────────────────

    def test__side_effect__defaults_used_when_no_kwarg(self):                     # Defaults still apply
        with Type_Safe__Config(fast_create=True):
            obj = TS__With_Defaults()                                             # No kwargs

        assert obj.name    == 'default_name'                                      # Default applied
        assert obj.count   == 42                                                  # Default applied
        assert obj.enabled is True                                                # Default applied

    def test__side_effect__partial_kwargs_mixed_with_defaults(self):              # Some kwargs, some defaults
        with Type_Safe__Config(fast_create=True):
            obj = TS__With_Defaults(name='custom')                                # Only override name

        assert obj.name    == 'custom'                                            # From kwargs
        assert obj.count   == 42                                                  # From default
        assert obj.enabled is True                                                # From default

    # ───────────────────────────────────────────────────────────────────────────
    # Side Effect: Unknown kwargs May Be Accepted
    # ───────────────────────────────────────────────────────────────────────────

    def test__side_effect__unknown_kwargs_accepted(self):                         # Extra fields added to __dict__
        with Type_Safe__Config(fast_create=True):
            obj = TS__Person(name='test', age=30, unknown_field='extra')

        assert obj.name == 'test'
        assert obj.age  == 30
        assert obj.unknown_field == 'extra'                                       # Extra field exists!
        assert 'unknown_field' in obj.__dict__

    def test__side_effect__unknown_kwargs_not_in_schema(self):                    # But not in json() if not annotated
        with Type_Safe__Config(fast_create=True):
            obj = TS__Person(name='test', extra='field')

        # Extra field is in __dict__ but json() only serializes annotated fields
        assert obj.extra == 'field'
        json_data = obj.json()
        # Note: behavior depends on json() implementation - it may or may not include extra

    # ───────────────────────────────────────────────────────────────────────────
    # Side Effect: Post-Creation Validation Still Works (Without skip_validation)
    # ───────────────────────────────────────────────────────────────────────────

    def test__side_effect__setattr_still_validates_after_fast_create(self):       # Only __init__ bypassed
        with Type_Safe__Config(fast_create=True):                                 # Note: skip_validation=False (default)
            obj = TS__Person(name=12345)                                          # This works (fast_create)

        # Object has invalid state from construction
        assert obj.name == 12345

        # But __setattr__ still validates (skip_validation not set)
        try:
            obj.name = 67890                                                      # Another invalid value
            raised_error = False
        except (TypeError, ValueError):
            raised_error = True

        assert raised_error is True                                               # Validation active on setattr!

    def test__side_effect__can_fix_via_setattr(self):                             # Can repair invalid state
        with Type_Safe__Config(fast_create=True):
            obj = TS__Person(name=12345)                                          # Invalid from constructor

        # Fix by setting valid value (validation allows valid values)
        obj.name = 'now_valid'

        assert obj.name == 'now_valid'
        assert type(obj.name) is str

    # ───────────────────────────────────────────────────────────────────────────
    # Side Effect: json() With Invalid Constructor Data
    # ───────────────────────────────────────────────────────────────────────────

    def test__side_effect__json_serializes_invalid_kwargs(self):                  # json() includes whatever is there
        with Type_Safe__Config(fast_create=True):
            obj = TS__Person(name=12345, age='twenty')

        json_data = obj.json()

        assert json_data['name'] == 12345                                         # int in JSON
        assert json_data['age']  == 'twenty'                                      # str in JSON

    def test__side_effect__json_handles_non_serializable(self):                   # Non-serializable becomes None
        with Type_Safe__Config(fast_create=True):
            obj = TS__Person(name=object())                                       # object() not JSON serializable

        json_data = obj.json()
        assert json_data == {'age': 0, 'name': None}                              # object() becomes None

    # ───────────────────────────────────────────────────────────────────────────
    # Comparison: Normal Mode vs Fast Create Mode
    # ───────────────────────────────────────────────────────────────────────────

    def test__comparison__normal_mode_validates_kwargs(self):                     # Normal mode rejects bad kwargs
        try:
            obj = TS__Person(name=12345)                                          # No fast_create context
            raised_error = False
        except (TypeError, ValueError):
            raised_error = True

        assert raised_error is True                                               # Normal mode validates!

    def test__comparison__fast_create_accepts_same_kwargs(self):                  # Fast create accepts bad kwargs
        with Type_Safe__Config(fast_create=True):
            obj = TS__Person(name=12345)                                          # Same kwargs

        assert obj.name == 12345                                                  # Accepted in fast_create

    # ───────────────────────────────────────────────────────────────────────────
    # Documented Safe Pattern: Trusted Data Loading
    # ───────────────────────────────────────────────────────────────────────────

    def test__safe_pattern__constructor_with_trusted_data(self):                  # Intended use case
        # Simulate data from trusted source
        trusted_records = [
            {'name': 'Alice', 'age': 30},
            {'name': 'Bob',   'age': 25},
        ]

        with Type_Safe__Config(fast_create=True):
            people = [TS__Person(**record) for record in trusted_records]

        assert len(people) == 2
        assert people[0].name == 'Alice'
        assert people[0].age  == 30
        assert type(people[0].name) is str                                        # Correct because source was valid
        assert type(people[0].age)  is int

    def test__safe_pattern__from_json_roundtrip(self):                            # Deserializing own data
        # Create and serialize valid object
        original = TS__Person(name='Test', age=42)
        json_data = original.json()

        # Fast reconstruct from JSON
        with Type_Safe__Config(fast_create=True):
            loaded = TS__Person(**json_data)

        assert loaded.name == original.name
        assert loaded.age  == original.age
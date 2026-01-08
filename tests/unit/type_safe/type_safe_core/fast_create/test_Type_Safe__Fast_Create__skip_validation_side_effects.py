# ═══════════════════════════════════════════════════════════════════════════════
# Tests: Type_Safe Fast Create - Skip Validation Side Effects
# Documents the INTENTIONAL TRADE-OFFS when using skip_validation=True
# ═══════════════════════════════════════════════════════════════════════════════
#
# PURPOSE: Document what happens when objects have invalid type values.
#          These are NOT BUGS - they are documented consequences of choosing
#          to bypass validation for performance.
#
# WHEN TO USE skip_validation=True:
#   - Bulk loading from trusted sources (database, serialized data)
#   - Performance-critical inner loops
#   - Data already validated elsewhere
#
# WHEN NOT TO USE skip_validation=True:
#   - User input
#   - Untrusted external data
#   - When type safety is critical
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


# ═══════════════════════════════════════════════════════════════════════════════
# Test: Skip Validation Side Effects (Documented Trade-offs)
# ═══════════════════════════════════════════════════════════════════════════════

class test_Type_Safe__Fast_Create__skip_validation_side_effects(TestCase):
    """
    These tests document the EXPECTED CONSEQUENCES of using skip_validation=True.
    All tests PASS - they document behavior, not bugs.

    The philosophy: "You asked for speed, you got speed. Type safety is your responsibility."
    """

    def setUp(self):
        type_safe_fast_create_cache.clear_cache()

    # ───────────────────────────────────────────────────────────────────────────
    # Side Effect: Object State Inconsistency
    # ───────────────────────────────────────────────────────────────────────────

    def test__side_effect__type_hints_not_enforced(self):                         # Type hints become documentation only
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Person()
            obj.name = 12345                                                      # int instead of str
            obj.age  = 'twenty'                                                   # str instead of int

        # Object exists with "wrong" types - this is the trade-off
        assert obj.name == 12345                                                  # Not a string!
        assert obj.age  == 'twenty'                                               # Not an int!
        assert type(obj.name) is int                                              # Type hint says str
        assert type(obj.age)  is str                                              # Type hint says int

    def test__side_effect__isinstance_still_works(self):                          # Object is still correct class
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Person()
            obj.name = {'not': 'a string'}

        # Despite invalid field, object identity is preserved
        assert isinstance(obj, TS__Person)
        assert isinstance(obj, Type_Safe)
        assert type(obj) is TS__Person

    # ───────────────────────────────────────────────────────────────────────────
    # Side Effect: json() Behavior With Invalid Types
    # ───────────────────────────────────────────────────────────────────────────

    def test__side_effect__json_serializes_wrong_types(self):                     # json() includes whatever is there
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Person()
            obj.name = 12345
            obj.age  = 'twenty'

        json_data = obj.json()

        # json() doesn't validate - it serializes what's there
        assert json_data['name'] == 12345                                         # int in JSON
        assert json_data['age']  == 'twenty'                                      # str in JSON

    def test__side_effect__json_with_assigned_object(self):
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Person()
            obj.name = object()


        assert obj.json() == {'age': 0, 'name': None}

    # ───────────────────────────────────────────────────────────────────────────
    # Side Effect: Collection Type Safety Bypassed
    # ───────────────────────────────────────────────────────────────────────────

    def test__side_effect__list_can_hold_wrong_types(self):                       # List[str] can hold anything
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__With_List()
            obj.items = [1, 2, 3, {'key': 'value'}, None]                         # Not List[str]!

        # The list contains non-strings
        assert obj.items == [1, 2, 3, {'key': 'value'}, None]
        assert type(obj.items[0]) is int                                          # Type hint said str

    def test__side_effect__list_replaced_entirely(self):                          # Can replace with non-list
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__With_List()
            obj.items = 'not_a_list'                                              # str instead of List

        assert obj.items == 'not_a_list'
        assert type(obj.items) is str                                             # Type hint said List[str]

    def test__side_effect__dict_can_hold_wrong_types(self):                       # Dict[str,int] can hold anything
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__With_Dict()
            obj.data = {123: 'wrong', 'key': 'also_wrong'}                        # Wrong key and value types

        assert obj.data == {123: 'wrong', 'key': 'also_wrong'}

    # ───────────────────────────────────────────────────────────────────────────
    # Side Effect: Nested Object Replacement
    # ───────────────────────────────────────────────────────────────────────────

    def test__side_effect__nested_object_can_be_replaced(self):                   # Nested Type_Safe replaceable
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__With_Nested()
            obj.inner = 'not_an_object'                                           # str instead of TS__Nested_Inner

        assert obj.inner == 'not_an_object'
        assert type(obj.inner) is str                                             # Type hint said TS__Nested_Inner

    def test__side_effect__nested_replaced_with_dict(self):                       # Common pattern: dict instead of object
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__With_Nested()
            obj.inner = {'value': 'from_dict'}                                    # Dict instead of Type_Safe

        # This might happen when loading from JSON without conversion
        assert obj.inner == {'value': 'from_dict'}
        assert type(obj.inner) is dict

    # ───────────────────────────────────────────────────────────────────────────
    # Side Effect: Validation Restored After Context
    # ───────────────────────────────────────────────────────────────────────────

    def test__side_effect__validation_restored_but_state_invalid(self):           # Object keeps invalid state
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Person()
            obj.age = 'not_an_int'                                                # Set invalid value

        # Outside context: validation is active again
        # But object ALREADY has invalid state - that's not fixed

        assert obj.age == 'not_an_int'                                            # Still there!

        # New assignments ARE validated
        try:
            obj.age = 'another_string'                                            # Now this fails
            raised_error = False
        except (TypeError, ValueError):
            raised_error = True

        assert raised_error is True                                               # Validation active
        assert obj.age == 'not_an_int'                                            # Original invalid value preserved

    def test__side_effect__can_fix_invalid_state_with_valid_value(self):          # Can repair object
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Person()
            obj.age = 'not_an_int'

        assert obj.age == 'not_an_int'                                            # Invalid state

        # Outside context - can set valid value to "fix" the object
        obj.age = 42                                                              # Valid int

        assert obj.age == 42                                                      # Now valid!

    # ───────────────────────────────────────────────────────────────────────────
    # Side Effect: Reading Invalid Values
    # ───────────────────────────────────────────────────────────────────────────

    def test__side_effect__reading_invalid_values_works(self):                    # Can always read
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Person()
            obj.name = ['a', 'list']
            obj.age  = {'a': 'dict'}

        # Reading doesn't validate - you get what's stored
        assert obj.name == ['a', 'list']
        assert obj.age  == {'a': 'dict'}

    def test__side_effect__operations_may_fail_on_wrong_types(self):              # Code expecting types may break
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Person()
            obj.name = 12345                                                      # int instead of str

        # String operations will fail
        try:
            result = obj.name.upper()                                             # int has no .upper()
            raised_error = False
        except AttributeError:
            raised_error = True

        assert raised_error is True                                               # int doesn't have upper()

    def test__side_effect__arithmetic_on_wrong_type_fails(self):                  # Math on non-numbers fails
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Person()
            obj.age = 'twenty'                                                    # str instead of int

        # Arithmetic will fail
        try:
            result = obj.age + 1                                                  # Can't add int to str
            raised_error = False
        except TypeError:
            raised_error = True

        assert raised_error is True                                               # str + int fails

    # ───────────────────────────────────────────────────────────────────────────
    # Documented Safe Pattern: Trusted Data Loading
    # ───────────────────────────────────────────────────────────────────────────

    def test__safe_pattern__loading_pre_validated_data(self):                     # Intended use case
        # Simulate data from trusted source (database, cache, etc.)
        trusted_data = [
            {'name': 'Alice', 'age': 30},
            {'name': 'Bob',   'age': 25},
            {'name': 'Carol', 'age': 35},
        ]

        # Fast bulk loading - data already validated at source
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            people = []
            for record in trusted_data:
                person = TS__Person()
                person.name = record['name']
                person.age  = record['age']
                people.append(person)

        # Objects are valid because source data was valid
        assert len(people) == 3
        assert people[0].name == 'Alice'
        assert people[0].age  == 30
        assert type(people[0].name) is str                                        # Correct type!
        assert type(people[0].age)  is int                                        # Correct type!

    def test__safe_pattern__json_roundtrip(self):                                 # Safe if data was valid
        # Create valid object
        original = TS__Person(name='Test', age=42)
        json_data = original.json()

        # Fast loading from json (which was valid)
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            loaded = TS__Person()
            loaded.name = json_data['name']
            loaded.age  = json_data['age']

        # Loaded object matches original
        assert loaded.name == original.name
        assert loaded.age  == original.age
        assert loaded.json() == original.json()
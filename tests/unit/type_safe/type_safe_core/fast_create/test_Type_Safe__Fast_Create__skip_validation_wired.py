# ═══════════════════════════════════════════════════════════════════════════════
# Tests: Type_Safe Fast Create - Skip Validation Wiring
# These tests verify skip_validation is ACTUALLY BYPASSING validation
# ═══════════════════════════════════════════════════════════════════════════════
#
# PURPOSE: Verify that skip_validation=True actually skips validation by:
#   - Setting invalid values that would normally raise errors
#   - Confirming no error is raised when skip_validation=True
#
# REQUIRES: Type_Safe.__setattr__ wiring:
#   config = get_active_config()
#   if config and config.skip_validation:
#       object.__setattr__(self, name, value)
#       return
#
# WITHOUT WIRING: Tests that set invalid values will FAIL (validation runs)
# WITH WIRING:    Tests that set invalid values will PASS (validation skipped)
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                         import List
from unittest                                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                                  import Type_Safe__Config
from osbot_utils.type_safe.type_safe_core.fast_create.Type_Safe__Fast_Create__Cache                 import type_safe_fast_create_cache


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Typed_Fields(Type_Safe):
    str_field   : str   = ''
    int_field   : int   = 0
    float_field : float = 0.0
    bool_field  : bool  = False
    list_field  : List[str]


# ═══════════════════════════════════════════════════════════════════════════════
# Test: Skip Validation Actually Skips (Mechanism Verification)
# ═══════════════════════════════════════════════════════════════════════════════

class test_Type_Safe__Fast_Create__skip_validation_wired(TestCase):
    """
    These tests verify that skip_validation mechanism is actually being invoked.
    They attempt to set INVALID values which would normally raise errors.

    WITHOUT WIRING: These tests FAIL because validation raises TypeError/ValueError
    WITH WIRING:    These tests PASS because validation is skipped
    """

    def setUp(self):
        type_safe_fast_create_cache.clear_cache()

    # ───────────────────────────────────────────────────────────────────────────
    # Invalid Value Assignment - Should ONLY work with skip_validation wired
    # ───────────────────────────────────────────────────────────────────────────

    def test__skip_validation__allows_wrong_type_str_to_int(self):                # String to int field
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Typed_Fields()
            obj.int_field = 'not_an_int'                                          # Would normally fail!

        assert obj.int_field == 'not_an_int'                                      # Value was set

    def test__skip_validation__allows_wrong_type_int_to_str(self):                # Int to str field
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Typed_Fields()
            obj.str_field = 12345                                                 # Would normally fail!

        assert obj.str_field == 12345                                             # Value was set (not converted)

    def test__skip_validation__allows_wrong_type_str_to_float(self):              # String to float field
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Typed_Fields()
            obj.float_field = 'not_a_float'                                       # Would normally fail!

        assert obj.float_field == 'not_a_float'                                   # Value was set

    def test__skip_validation__allows_wrong_type_str_to_bool(self):               # String to bool field
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Typed_Fields()
            obj.bool_field = 'not_a_bool'                                         # Would normally fail!

        assert obj.bool_field == 'not_a_bool'                                     # Value was set

    def test__skip_validation__allows_wrong_type_to_list(self):                   # String to list field
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Typed_Fields()
            obj.list_field = 'not_a_list'                                         # Would normally fail!

        assert obj.list_field == 'not_a_list'                                     # Value was set

    def test__skip_validation__allows_none_to_non_optional(self):                 # None to non-optional field
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Typed_Fields()
            obj.str_field = None                                                  # Would normally fail!

        assert obj.str_field is None                                              # Value was set

    def test__skip_validation__allows_dict_to_int(self):                          # Dict to int field
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Typed_Fields()
            obj.int_field = {'key': 'value'}                                      # Would normally fail!

        assert obj.int_field == {'key': 'value'}                                  # Value was set

    def test__skip_validation__allows_object_to_str(self):                        # Object to str field
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Typed_Fields()
            custom_obj = object()
            obj.str_field = custom_obj                                            # Would normally fail!

        assert obj.str_field is custom_obj                                        # Exact same object

    # ───────────────────────────────────────────────────────────────────────────
    # Multiple Invalid Assignments in Sequence
    # ───────────────────────────────────────────────────────────────────────────

    def test__skip_validation__multiple_invalid_assignments(self):                # Multiple fields, all wrong types
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Typed_Fields()
            obj.str_field   = 123
            obj.int_field   = 'abc'
            obj.float_field = [1, 2, 3]
            obj.bool_field  = {'key': 'val'}

        assert obj.str_field   == 123
        assert obj.int_field   == 'abc'
        assert obj.float_field == [1, 2, 3]
        assert obj.bool_field  == {'key': 'val'}

    # ───────────────────────────────────────────────────────────────────────────
    # Verify Validation Still Works WITHOUT skip_validation
    # ───────────────────────────────────────────────────────────────────────────

    def test__without_skip_validation__rejects_wrong_type(self):                  # Validation still enforced
        with Type_Safe__Config(fast_create=True, skip_validation=False):
            obj = TS__Typed_Fields()

            try:
                obj.int_field = 'not_an_int'
                validation_raised = False
            except (TypeError, ValueError):
                validation_raised = True

        assert validation_raised is True                                          # Validation DID run

    def test__no_config__rejects_wrong_type(self):                                # Default behavior validates
        obj = TS__Typed_Fields()

        try:
            obj.int_field = 'not_an_int'
            validation_raised = False
        except (TypeError, ValueError):
            validation_raised = True

        assert validation_raised is True                                          # Validation DID run

    # ───────────────────────────────────────────────────────────────────────────
    # Skip Validation Only Active In Context
    # ───────────────────────────────────────────────────────────────────────────

    def test__skip_validation__only_in_context(self):                             # Outside context validates
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Typed_Fields()
            obj.int_field = 'inside_context'                                      # Works - skip active

        assert obj.int_field == 'inside_context'

        # Outside context - validation should be active again
        try:
            obj.int_field = 'outside_context'                                     # Should fail now!
            validation_raised = False
        except (TypeError, ValueError):
            validation_raised = True

        assert validation_raised is True                                          # Validation restored

    # ───────────────────────────────────────────────────────────────────────────
    # Valid Values Still Work With skip_validation
    # ───────────────────────────────────────────────────────────────────────────

    def test__skip_validation__valid_values_still_work(self):                     # Valid values unaffected
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            obj = TS__Typed_Fields()
            obj.str_field   = 'valid_string'
            obj.int_field   = 42
            obj.float_field = 3.14
            obj.bool_field  = True

        assert obj.str_field   == 'valid_string'
        assert obj.int_field   == 42
        assert obj.float_field == 3.14
        assert obj.bool_field  is True
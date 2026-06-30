# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Hypothesis_C - Skip Validation Implementation
# Tests the performance gain from skipping validation in Type_Safe
# ═══════════════════════════════════════════════════════════════════════════════
#
# This hypothesis tests: Can we recover the ~350ns config lookup overhead
# by skipping expensive validation operations?
#
# Expected savings per attribute: ~600 ns
# Break-even: 1 attribute
# Expected win: Significant for any class with attributes
#
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                            import get_active_config
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__Set_Attr import type_safe_step_set_attr

find_type_safe_config = get_active_config                                                     # Alias for clarity


class Type_Safe__Hypothesis_C(Type_Safe):                                                     # Skip validation when config says so
    """
    HYPOTHESIS C: skip_validation Flag in __setattr__

    Change: When skip_validation=True, bypass type_safe_step_set_attr entirely
    Expected: Significant savings (validation costs ~600 ns per attribute)

    This is a SURGICAL change - only __setattr__ is modified, everything else
    uses the standard Type_Safe machinery.
    """

    def __setattr__(self, name, value):
        config = find_type_safe_config()
        if config and config.skip_validation:
            object.__setattr__(self, name, value)                   # Direct bypass
        else:
            type_safe_step_set_attr.setattr(super(), self, name, value)